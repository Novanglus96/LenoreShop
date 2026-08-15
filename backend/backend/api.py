from ninja import NinjaAPI, Schema, Query, File
from ninja.files import UploadedFile
from api.models import (
    Store,
    Aisle,
    Item,
    ListItem,
    ShoppingList,
    Freezer,
    FreezerItem,
)
from api.broadcast import broadcast_invalidate
from api.images import ImageUploadError, build_renditions, delete_renditions
from typing import List, Optional
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.core.management import call_command
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.db.models import F, Count, Prefetch, Q

api = NinjaAPI()
api.title = "LenoreShop API"
api.version = "1.9.0-alpha.2"
api.description = "API documentation for LenoreShop"

# Number of items previewed as ruled lines on a shopping list card.
LIST_PREVIEW_ITEM_COUNT = 4

# Number of items previewed on a freezer card.
FREEZER_PREVIEW_ITEM_COUNT = 4

# How far ahead counts as "expiring soon" for a freezer. Shared with the
# /freezeritemsexpiring endpoint so the dashboard and that list agree on what
# is urgent.
FREEZER_SOON_DAYS = 14


def image_path(stored):
    """
    Returns the media path of an ImageField, or None when nothing is stored.

    The path is left relative (`/media/...`) rather than made absolute: Vite
    proxies /media in dev and nginx serves it in prod, so a relative path is the
    one form that works in both without the backend knowing its own hostname.

    Args:
        stored (ImageFieldFile): The field to read.

    Returns:
        (str): The media path, or None.
    """
    # An unset ImageField is falsy but still has a .url that raises.
    return stored.url if stored else None


def freezer_queryset():
    """
    Returns the base Freezer queryset used by every endpoint that responds with
    `FreezerOut`, so freezer cards get their counts and preview lines without an
    extra query per freezer.

    Expired and expiring are kept separate rather than lumped together the way
    /freezeritemsexpiring does it, because a card needs to distinguish "throw
    this out now" from "use this up soon".

    Returns:
        (QuerySet): Freezers annotated with `totalitems`, `totalexpired` and
            `totalexpiring`, with the preview items prefetched.
    """
    today = date.today()
    soon = today + timedelta(days=FREEZER_SOON_DAYS)
    return Freezer.objects.annotate(
        totalitems=Count("freezeritem", distinct=True),
        totalexpired=Count(
            "freezeritem",
            filter=Q(freezeritem__discard_date__lt=today),
            distinct=True,
        ),
        totalexpiring=Count(
            "freezeritem",
            filter=Q(
                freezeritem__discard_date__gte=today,
                freezeritem__discard_date__lte=soon,
            ),
            distinct=True,
        ),
    ).prefetch_related(
        Prefetch(
            "freezeritem_set",
            # Soonest to go off first, undated last — the same order the
            # freezer detail view uses.
            queryset=FreezerItem.objects.order_by(
                F("discard_date").asc(nulls_last=True), "name"
            ),
        )
    )


def shoppinglist_queryset():
    """
    Returns the base ShoppingList queryset used by every endpoint that responds with
    `ShoppingListOut`, so cards get their progress counts and preview lines without
    an extra query per list.

    Returns:
        (QuerySet): ShoppingLists annotated with `totalitems` and `totalpurchased`,
            with the store and the preview list items prefetched.
    """
    return (
        ShoppingList.objects.select_related("store")
        .annotate(
            totalitems=Count("listitem", distinct=True),
            totalpurchased=Count(
                "listitem", filter=Q(listitem__purchased=True), distinct=True
            ),
        )
        .prefetch_related(
            Prefetch(
                "listitem_set",
                queryset=ListItem.objects.select_related("item").order_by(
                    "purchased", "aisle__order", "id"
                ),
            )
        )
    )


# The class VersionOut is a scheam for representing Version information.
class VersionOut(Schema):
    """
    Schema to represent a Version.

    Attributes:
        version_number (str): The version of the app.
    """

    version_number: str


class UserSchema(Schema):
    """
    Schema to validate a User

    Attributes:
        username (str): The user's username.
        is_authenticated (bool): Wether or not the use is authenticated.
        email (str): The user's email address.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
    """

    username: str
    is_authenticated: bool
    email: str = None
    first_name: str = None
    last_name: str = None


class StoreIn(Schema):
    """
    Schema to validate a Store.

    Attributes:
        name (str): The name of the store.
    """

    name: str


class StoreOut(Schema):
    """
    Schema to represent a Store.

    Attributes:
        id (int): ID integer. Unique.
        name (str): The name of the store.
    """

    id: int
    name: str


class AisleIn(Schema):
    """
    Schema to validate an Aisle.

    Attributes:
        name (str): The name of the aisle.
        order (int): The order of the aisle. Default = 1.
        store_id (int): The ID of a Store object.
    """

    name: str
    order: int = 1
    store_id: int


class AisleOut(Schema):
    """
    Schema to represent an Aisle.

    Attributes:
        id (int): ID integer. Unique.
        name (str): The name of the Aisle.
        order (int): The order of the Aisle. Default = 1.
        store_id (int): The ID of the store.
        store (StoreOut): The Store object.
    """

    id: int
    name: str
    order: int = 1
    store_id: int
    store: StoreOut


class ItemIn(Schema):
    """
    Schema to validate an Item.

    Attributes:
        name (str): The name of the item.
        matches (str): Names that match this item.
        aisle (AisleOut): Last aisle used for this item.
    """

    name: str
    matches: str = None
    aisle: Optional[AisleOut]


class ItemOut(Schema):
    """
    Schema to represent an Item.

    Attributes:
        id (int): ID integer. Unique.
        name (str): The name of the item.
        matches (str): Names that macth this item.
        aisle (AisleOut): Last aisle used for this item. Optional.
        image_url (str): Path to the full photo, for tap-to-enlarge. None when
            the item has no photo.
        thumbnail_url (str): Path to the thumbnail shown on rows. None when the
            item has no photo.
    """

    id: int
    name: str
    matches: str = None
    aisle: Optional[AisleOut]
    image_url: str = None
    thumbnail_url: str = None

    @staticmethod
    def resolve_image_url(obj):
        """
        Returns:
            (str): The media path of the full photo, or None.
        """
        return image_path(obj.image)

    @staticmethod
    def resolve_thumbnail_url(obj):
        """
        Returns:
            (str): The media path of the thumbnail, or None.
        """
        return image_path(obj.thumbnail)


class PaginatedItems(Schema):
    """
    Schema to represent a paginated list of Items.

    Attributes:
        items (List[ItemOut]): A paginated list of items.
        current_page (int): The current page of the list.
        total_pages (int): The total number of pages of items.
        total_records (int): The total count of items.
    """

    items: List[ItemOut]
    current_page: int
    total_pages: int
    total_records: int


class ListItemIn(Schema):
    """
    Schema to validate a ListItem.

    Attributes:
        qty (int): The quantity of list items. Default = 1.
        purchased (bool): Wether the list item has been purchsaed. Default = False.
        notes (str): Notes for the list item. Default = None.
        purch_date (date): Last aisle used for this item. Default = None.
        item_id (int): ID of the item.
        aisle_id (int): ID of the aisle.
        shopping_list_id (int): ID of the shopping list.
    """

    qty: int = 1
    purchased: bool = False
    notes: str = None
    purch_date: date = None
    item_id: int
    aisle_id: int
    shopping_list_id: int


class ListItemOut(Schema):
    """
    Schema to represent a ListItem.

    Attributes:
        id (int): The ID of the list item.
        qty (int): The quantity of list items. Default = 1.
        purchased (bool): Wether the list item has been purchsaed. Default = False.
        notes (str): Notes for the list item. Default = None.
        purch_date (date): Last aisle used for this item. Default = None.
        item_id (int): ID of the item.
        aisle_id (int): ID of the aisle.
        shopping_list_id (int): ID of the shopping list.
        item (ItemOut): Object representing the item for the list item.
    """

    id: int
    qty: int = 1
    purchased: bool = False
    notes: str = None
    purch_date: date = None
    item_id: int
    aisle_id: int
    shopping_list_id: int
    item: ItemOut


class ShoppingListIn(Schema):
    """
    Schema to validate a ShoppingList.

    Attributes:
        name (str): The name of the shopping list.
        store_id (int): The ID of the store for the shopping list.
    """

    name: str
    store_id: int


class ListPreviewItem(Schema):
    """
    Schema to represent a single ruled line previewed on a shopping list card.

    Attributes:
        name (str): The name of the item.
        purchased (bool): Whether this list item has been purchased.
    """

    name: str
    purchased: bool


class ShoppingListOut(Schema):
    """
    Schema to represent a ShoppingList.

    Attributes:
        id (int): ID of the shopping list.
        name (str): The name of the shopping list.
        store_id (int): The ID of the store for the shopping list.
        store (StoreOut): The Store object.
        totalitems (int): The total number of items on the shopping list.
        totalpurchased (int): The number of items marked purchased.
        preview_items (List[ListPreviewItem]): The first few items, unpurchased first,
            for previewing the list without fetching it in full.
    """

    id: int
    name: str
    store_id: int
    store: StoreOut
    totalitems: int = 0
    totalpurchased: int = 0
    preview_items: List[ListPreviewItem] = []

    @staticmethod
    def resolve_preview_items(obj):
        """
        Returns the first few list items, already ordered unpurchased-first by the
        prefetch in `shoppinglist_queryset`. Falls back to an empty list when the
        object was not loaded through that queryset.
        """
        listitems = getattr(obj, "listitem_set", None)
        if listitems is None:
            return []
        return [
            ListPreviewItem(name=listitem.item.name, purchased=listitem.purchased)
            for listitem in listitems.all()[:LIST_PREVIEW_ITEM_COUNT]
        ]


class AislesWithItems(Schema):
    """
    Schema to represent an Aisle with ListItems assigned to it.

    Attributes:
        id (int): ID of the aisle.
        name (str): The name of the aisle.
        order (int): The order of the aisle.
        store_id (int): The id of the store this aisle is in.
        listitems (List[ListItemOut]): A list of list items in this aisle.
    """

    id: int
    name: str
    order: int = 1
    store_id: int
    listitems: List[ListItemOut]


class ShoppingListFull(Schema):
    """
    Schema to represent a ShoppingList with ListItems assigned to it.

    Attributes:
        id (int): ID of the shopping list.
        name (str): The name of the shopping list.
        store_id (int): The ID of the store for this shopping list.
        store (StoreOut): The Store object.
        aisles (List[AislesWithItems]): A list of aisles with listitems assigned.
        purchased_aisles (List[AislesWithItems]): A list of aisles with listitems marked as
            purchased.
        totalitems (int): The total number of items on the shopping list.
        totalpurchased (int): The total number of items marked purchased on the shopping list.
    """

    id: int
    name: str
    store_id: int
    store: StoreOut
    aisles: List[AislesWithItems]
    purchased_aisles: List[AislesWithItems]
    totalitems: int
    totalpurchased: int


class FreezerIn(Schema):
    """
    Schema to validate a Freezer.

    Attributes:
        name (str): The name of the freezer.
        location (str): Where the freezer is. Default = None.
    """

    name: str
    location: str = None


class FreezerPreviewItem(Schema):
    """
    Schema to represent a single item previewed on a freezer card.

    Attributes:
        name (str): The name of the frozen food.
        days_until_discard (int): Days left before discard_date, negative once
            past it. None when no discard_date is set.
        is_expired (bool): True if the discard date has passed.
    """

    name: str
    days_until_discard: int = None
    is_expired: bool = False


class FreezerOut(Schema):
    """
    Schema to represent a Freezer.

    Attributes:
        id (int): ID integer. Unique.
        name (str): The name of the freezer.
        location (str): Where the freezer is. Default = None.
        totalitems (int): The total number of frozen foods in this freezer.
        totalexpired (int): How many are already past their discard date.
        totalexpiring (int): How many reach their discard date within
            FREEZER_SOON_DAYS days, not counting the ones already past it.
        preview_items (List[FreezerPreviewItem]): The items closest to their
            discard date, for previewing the freezer without fetching it whole.
    """

    id: int
    name: str
    location: str = None
    totalitems: int = 0
    totalexpired: int = 0
    totalexpiring: int = 0
    preview_items: List[FreezerPreviewItem] = []

    @staticmethod
    def resolve_preview_items(obj):
        """
        Returns the items closest to their discard date, already ordered by the
        prefetch in `freezer_queryset`. Falls back to an empty list when the
        object was not loaded through that queryset.
        """
        freezeritems = getattr(obj, "freezeritem_set", None)
        if freezeritems is None:
            return []
        return [
            FreezerPreviewItem(
                name=freezeritem.name,
                days_until_discard=freezeritem.days_until_discard,
                is_expired=freezeritem.is_expired,
            )
            for freezeritem in freezeritems.all()[:FREEZER_PREVIEW_ITEM_COUNT]
        ]


class FreezerItemIn(Schema):
    """
    Schema to validate a FreezerItem.

    Attributes:
        name (str): The name of the frozen food.
        qty (int): How much is stored. Default = 1.
        unit (str): The unit for qty. Default = None.
        date_added (date): The date this went into the freezer. Default = None,
            meaning the date is unknown.
        discard_date (date): The date this should be thrown out. Default = None.
        notes (str): Notes for the frozen food. Default = None.
        freezer_id (int): ID of the freezer.
    """

    name: str
    qty: int = 1
    unit: str = None
    date_added: date = None
    discard_date: date = None
    notes: str = None
    freezer_id: int


class FreezerItemOut(Schema):
    """
    Schema to represent a FreezerItem.

    Attributes:
        id (int): The ID of the freezer item.
        name (str): The name of the frozen food.
        qty (int): How much is stored. Default = 1.
        unit (str): The unit for qty. Default = None.
        date_added (date): The date this went into the freezer. None when the
            date is unknown.
        discard_date (date): The date this should be thrown out. Default = None.
        notes (str): Notes for the frozen food. Default = None.
        freezer_id (int): ID of the freezer.
        days_until_discard (int): Days left before discard_date, negative once
            past it. None when no discard_date is set.
        is_expired (bool): True if the discard date has passed.
        image_url (str): Path to the full photo, for tap-to-enlarge. None when
            the frozen food has no photo.
        thumbnail_url (str): Path to the thumbnail shown on rows. None when the
            frozen food has no photo.
    """

    id: int
    name: str
    qty: int = 1
    unit: str = None
    date_added: date = None
    discard_date: date = None
    notes: str = None
    freezer_id: int
    days_until_discard: int = None
    is_expired: bool = False
    image_url: str = None
    thumbnail_url: str = None

    @staticmethod
    def resolve_image_url(obj):
        """
        Returns:
            (str): The media path of the full photo, or None.
        """
        return image_path(obj.image)

    @staticmethod
    def resolve_thumbnail_url(obj):
        """
        Returns:
            (str): The media path of the thumbnail, or None.
        """
        return image_path(obj.thumbnail)


class FreezerFull(Schema):
    """
    Schema to represent a Freezer with the FreezerItems stored in it.

    Attributes:
        id (int): ID of the freezer.
        name (str): The name of the freezer.
        location (str): Where the freezer is. Default = None.
        freezeritems (List[FreezerItemOut]): The frozen foods in this freezer.
        totalitems (int): The total number of frozen foods in this freezer.
        totalexpired (int): How many of those are past their discard date.
    """

    id: int
    name: str
    location: str = None
    freezeritems: List[FreezerItemOut]
    totalitems: int
    totalexpired: int


@api.get("/me", response=UserSchema)
def me(request):
    """
    The function `me` returns a user.

    Endpoint:
        - **Path**: `/api/me`
        - **Method**: `GET`

    Args:
        request ():

    Returns:
        (UserSchema): Returns a user.
    """
    return request.user


@api.post("/aisles")
def create_aisle(request, payload: AisleIn):
    """
    The function `create_aisle` creates an Aisle.

    Endpoint:
        - **Path**: `/api/aisles`
        - **Method**: `POST`

    Args:
        request ():
        payload (AisleIn): An object using schema of AisleIn.

    Returns:
        id (int): returns the id of the created Aisle.
    """
    aisle = Aisle.objects.create(**payload.dict())
    broadcast_invalidate(["aisles"])
    return {"id": aisle.id}


@api.post("/items", response=ItemOut)
def create_item(request, payload: ItemIn):
    """
    The function `create_item` creates an Item.

    Endpoint:
        - **Path**: `/api/items`
        - **Method**: `POST`

    Args:
        request ():
        payload (ItemIn): An object using schema of ItemIn.

    Returns:
        id (int): returns the id of the created Item.
    """
    item = Item.objects.create(**payload.dict())
    broadcast_invalidate(["items"])
    return item


def merge_duplicate_listitem(listitem):
    """
    Folds a ListItem into another row for the same item on the same list that is
    in the same purchased state, and returns whichever row survives.

    A list is allowed at most one outstanding row and one bought row per item.
    Two rows exist on purpose while an item is partly bought — one in the cart,
    one still to find — because they mean different things and sit in different
    sections of the list. Once a flag change puts them both in the same state
    that distinction is gone, and leaving them apart shows the same item twice
    in one section, which reads as a fault rather than as history.

    Args:
        listitem (ListItem): The row that has just changed state.

    Returns:
        (ListItem): The surviving row, which may be the one passed in.
    """
    duplicate = (
        ListItem.objects.filter(
            shopping_list_id=listitem.shopping_list_id,
            item_id=listitem.item_id,
            purchased=listitem.purchased,
        )
        .exclude(id=listitem.id)
        .order_by("id")
        .first()
    )
    if duplicate is None:
        return listitem

    duplicate.qty += listitem.qty
    # Notes are only worth carrying over if the survivor has none; concatenating
    # them would be worse than dropping one.
    if listitem.notes and not duplicate.notes:
        duplicate.notes = listitem.notes
    # The later purchase is the one that describes the merged row.
    if listitem.purch_date and (
        duplicate.purch_date is None or listitem.purch_date > duplicate.purch_date
    ):
        duplicate.purch_date = listitem.purch_date
    duplicate.save()
    listitem.delete()
    return duplicate


@api.post("/listitems")
def create_listitem(request, payload: ListItemIn):
    """
    The function `create_listitem` creates a ListItem.

    Endpoint:
        - **Path**: `/api/listitems`
        - **Method**: `POST`

    Args:
        request ():
        payload (ListItemIn): An object using schema of ListItemIn.

    Returns:
        id (int): returns the id of the created ListItem.
    """
    # Only an item still to be found is a candidate to merge into. Adding
    # something you have already put in the cart means you need more of it, so
    # it starts a new line rather than reopening the old one — otherwise the
    # quantities add together and the row silently reverts to unpurchased,
    # which reads as the app forgetting you bought it.
    existing_item = ListItem.objects.filter(
        shopping_list_id=payload.shopping_list_id,
        item_id=payload.item_id,
        purchased=False,
    ).first()
    if existing_item is None:
        listitem = ListItem.objects.create(**payload.dict())
        item = Item.objects.get(id=payload.item_id)
        item.aisle_id = payload.aisle_id
        item.save()
        broadcast_invalidate(["fullshoppinglist", "shoppinglists"])
        return {"id": listitem.id}
    else:
        existing_item.qty += payload.qty
        existing_item.save()
        broadcast_invalidate(["fullshoppinglist", "shoppinglists"])
        return {"id": existing_item.id}


@api.post("/shoppinglists")
def create_shoppinglist(request, payload: ShoppingListIn):
    """
    The function `create_shoppinglist` creates a ShoppingList.

    Endpoint:
        - **Path**: `/api/shoppinglists`
        - **Method**: `POST`

    Args:
        request ():
        payload (ShoppingListIn): An object using schema of ShoppingListIn.

    Returns:
        id (int): returns the id of the created ShoppingList.
    """
    shoppinglist = ShoppingList.objects.create(**payload.dict())
    broadcast_invalidate(["shoppinglists"])
    return {"id": shoppinglist.id}


@api.get("/aisles/{aisle_id}", response=AisleOut)
def get_aisle(request, aisle_id: int):
    """
    The function `get_aisle` returns an Aisle.

    Endpoint:
        - **Path**: `/api/aisles/{aisle_id}`
        - **Method**: `GET`

    Args:
        request ():
        aisle_id (int): An ID of an Aisle.

    Returns:
        (AisleOut): returns the Aisle object.
    """
    aisle = get_object_or_404(Aisle, id=aisle_id)
    return aisle


@api.get("/items/{item_id}", response=ItemOut)
def get_item(request, item_id: int):
    """
    The function `get_item` returns an Item.

    Endpoint:
        - **Path**: `/api/items/{item_id}`
        - **Method**: `GET`

    Args:
        request ():
        item_id (int): The ID of an Item.

    Returns:
        (ItemOut): returns an Item object.
    """
    item = get_object_or_404(Item, id=item_id)
    return item


@api.get("/listitems/{listitem_id}", response=ListItemOut)
def get_listitem(request, listitem_id: int):
    """
    The function `get_listitem` returns a ListItem

    Endpoint:
        - **Path**: `/api/listitems/{listitem_id}`
        - **Method**: `GET`

    Args:
        request ():
        listitem_id (int): The ID of a ListItem.

    Returns:
        (ListItemOut): returns a ListItem object.
    """
    listitem = get_object_or_404(ListItem, id=listitem_id)
    return listitem


@api.get("/shoppinglists/{shoppinglist_id}", response=ShoppingListOut)
def get_shoppinglist(request, shoppinglist_id: int):
    """
    The function `get_shoppinglist` returns a ShoppingList.

    Endpoint:
        - **Path**: `/api/shoppinglists/{shoppinglist_id}`
        - **Method**: `GET`

    Args:
        request ():
        shoppinglist_id (int): An ID of a ShoppingList.

    Returns:
        (ShoppingListOut): returns a ShoppingList object.
    """
    shoppinglist = get_object_or_404(shoppinglist_queryset(), id=shoppinglist_id)
    return shoppinglist


@api.get("/shoppinglistfull/{shoppinglist_id}", response=ShoppingListFull)
def get_shoppinglistfull(request, shoppinglist_id: int):
    """
    The function `get_shoppinglistfull` returns a ShoppingList with aisles and items.

    Endpoint:
        - **Path**: `/api/shoppinglistfull/{shoppinglist_id}`
        - **Method**: `GET`

    Args:
        request ():
        shoppinglist_id (int): The ID of a ShoppingList.

    Returns:
        (ShoppingListFull): returns a ShoppingListFull object.
    """
    shoppinglist = get_object_or_404(ShoppingList, id=shoppinglist_id)
    store = shoppinglist.store
    aisles = Aisle.objects.filter(
        store=store,
        listitem__shopping_list=shoppinglist,
        listitem__purchased=False,
    ).order_by("order", "name")
    purchasedaisles = Aisle.objects.filter(
        store=store,
        listitem__shopping_list=shoppinglist,
        listitem__purchased=True,
    ).order_by("order", "name")
    aisles_dict = {
        aisle.id: AislesWithItems(
            id=aisle.id,
            name=aisle.name,
            order=aisle.order,
            store_id=store.id,
            listitems=[],
        )
        for aisle in aisles
    }
    purchased_aisles_dict = {
        aisle.id: AislesWithItems(
            id=aisle.id,
            name=aisle.name,
            order=aisle.order,
            store_id=store.id,
            listitems=[],
        )
        for aisle in purchasedaisles
    }
    # select_related because every row below reads listitem.item and
    # listitem.aisle; without it a full list costs two extra queries per row.
    listitems = (
        ListItem.objects.filter(shopping_list=shoppinglist, purchased=False)
        .select_related("item", "aisle")
        .order_by("purchased", "item__name")
    )
    purchasedlistitems = (
        ListItem.objects.filter(shopping_list=shoppinglist, purchased=True)
        .select_related("item", "aisle")
        .order_by("purchased", "item__name")
    )
    total_purchased_count = ListItem.objects.filter(
        shopping_list=shoppinglist, purchased=True
    ).count()
    total_items_count = (
        ListItem.objects.filter(shopping_list=shoppinglist)
        .order_by("purchased", "item__name")
        .count()
    )

    for listitem in listitems:
        aisles_dict[listitem.aisle.id].listitems.append(
            ListItemOut(
                id=listitem.id,
                qty=listitem.qty,
                purchased=listitem.purchased,
                notes=listitem.notes,
                purch_date=listitem.purch_date,
                item_id=listitem.item.id,
                aisle_id=listitem.aisle_id,
                shopping_list_id=listitem.shopping_list.id,
                # Built by hand rather than from_orm so the item's aisle is left
                # off: it is redundant here (the row already sits under an aisle)
                # and resolving it would cost two queries per row. The image
                # paths have to be passed explicitly for the same reason — the
                # ItemOut resolvers only run under from_orm.
                item=ItemOut(
                    id=listitem.item.id,
                    name=listitem.item.name,
                    matches=listitem.item.matches,
                    image_url=image_path(listitem.item.image),
                    thumbnail_url=image_path(listitem.item.thumbnail),
                ),
            )
        )

    for listitem in purchasedlistitems:
        purchased_aisles_dict[listitem.aisle.id].listitems.append(
            ListItemOut(
                id=listitem.id,
                qty=listitem.qty,
                purchased=listitem.purchased,
                notes=listitem.notes,
                purch_date=listitem.purch_date,
                item_id=listitem.item.id,
                aisle_id=listitem.aisle_id,
                shopping_list_id=listitem.shopping_list.id,
                # Built by hand rather than from_orm so the item's aisle is left
                # off: it is redundant here (the row already sits under an aisle)
                # and resolving it would cost two queries per row. The image
                # paths have to be passed explicitly for the same reason — the
                # ItemOut resolvers only run under from_orm.
                item=ItemOut(
                    id=listitem.item.id,
                    name=listitem.item.name,
                    matches=listitem.item.matches,
                    image_url=image_path(listitem.item.image),
                    thumbnail_url=image_path(listitem.item.thumbnail),
                ),
            )
        )

    response_data = ShoppingListFull(
        id=shoppinglist.id,
        name=shoppinglist.name,
        store_id=store.id,
        store=StoreOut(id=store.id, name=store.name),
        aisles=list(aisles_dict.values()),
        purchased_aisles=list(purchased_aisles_dict.values()),
        totalitems=total_items_count,
        totalpurchased=total_purchased_count,
    )
    return response_data


@api.get("/aisles", response=List[AisleOut])
def list_aisles(request):
    """
    The function `list_aisles` returns a list of Aisles.

    Endpoint:
        - **Path**: `/api/aisles`
        - **Method**: `GET`

    Args:
        request ():

    Returns:
        (List[AisleOut]): returns a list of Aisle objects.
    """
    qs = Aisle.objects.all()
    return qs


@api.get("/aislesbystore/{store_id}", response=List[AisleOut])
def list_aislesbystore(request, store_id: int):
    """
    The function `list_aislesbystore` returns a list of Aisles for a matching
    store ID.

    Endpoint:
        - **Path**: `/api/aislesbystore/{store_id}`
        - **Method**: `GET`

    Args:
        request ():
        store_id (int): An ID of a Store.

    Returns:
        (List[AisleOut]): Returns a list of Aisles.
    """
    qs = Aisle.objects.all().filter(store__id=store_id).order_by("order")
    return qs


@api.get("/items", response=PaginatedItems)
def list_items(
    request,
    page: Optional[int] = Query(1),
    page_size: Optional[int] = Query(15),
    full: Optional[bool] = Query(False),
):
    """
    The function `list_items` returns a paginated list of Items.

    Endpoint:
        - **Path**: `/api/items`
        - **Method**: `GET`

    Args:
        request ():
        page (int): The page number to return. Optional. Default = 1.
        page_size (int): Hoe many items per page. Optional. Default = 15.
        full (bool): Wehter this is a full request or not. Optional. Default = False.

    Returns:
        (PaginatedItems): returns a PaginatedItems object.
    """
    qs = Item.objects.all().order_by("name")
    total_pages = 0
    item_list = []
    if not full:
        if len(qs) > 0:
            paginator = Paginator(qs, page_size)
            page_obj = paginator.page(page)
            item_list = list(page_obj.object_list)
            total_pages = paginator.num_pages
    else:
        item_list = list(qs)
    total_records = len(qs)
    paginated_items = PaginatedItems(
        items=item_list,
        current_page=page,
        total_pages=total_pages,
        total_records=total_records,
    )
    return paginated_items


@api.get("/listitems", response=List[ListItemOut])
def list_listitems(request):
    """
    The function `list_listitems` returns a list of ListItems.

    Endpoint:
        - **Path**: `/api/listitems`
        - **Method**: `GET`

    Args:
        request ():

    Returns:
        (List[ListItemOut]): Returns a list of ListItem objects.
    """
    qs = ListItem.objects.all()
    return qs


@api.get("/shoppinglists", response=List[ShoppingListOut])
def list_shoppinglists(request):
    """
    The function `list_shoppinglists` returns a list of ShoppingLists.

    Endpoint:
        - **Path**: `/api/shoppinglists`
        - **Method**: `GET`

    Args:
        request ():

    Returns:
        (List[ShoppingListOut]): Returns a list of ShoppingList objects.
    """
    qs = shoppinglist_queryset().order_by("store__name", "name")
    return qs


@api.get("/listsbystore/{store_id}", response=List[ShoppingListOut])
def list_listsbystore(request, store_id: int):
    """
    The function `list_listsbystore` returns a list of ShoppingLists for a given
    Store ID.

    Endpoint:
        - **Path**: `/api/listsbystore/{store_id}`
        - **Method**: `GET`

    Args:
        request ():
        store_id (int): The ID of a Store.

    Returns:
        (List[ShoppingListOut]): Returns a list of ShoppingList objects.
    """
    qs = shoppinglist_queryset().filter(store__id=store_id).order_by("name")
    return qs


@api.put("/aisles/{aisle_id}")
def update_aisle(request, aisle_id: int, payload: AisleIn):
    """
    The function `update_aisle` updates an Aisle

    Endpoint:
        - **Path**: `/api/aisles/{aisle_id}`
        - **Method**: `PUT`

    Args:
        request ():
        aisle_id (int): The ID of an aisle object.
        payload (AisleIn): An Aisle object.

    Returns:
        success (bool): True if successfully updated.
    """
    aisle = get_object_or_404(Aisle, id=aisle_id)
    aisle.name = payload.name
    aisle.order = payload.order
    aisle.store_id = payload.store_id
    aisle.save()
    broadcast_invalidate(["aisles"])
    return {"success": True}


@api.put("/items/{item_id}")
def update_item(request, item_id: int, payload: ItemIn):
    """
    The function `update_item` updates an Item.

    Endpoint:
        - **Path**: `/api/items/{item_id}`
        - **Method**: `PUT`

    Args:
        request ():
        item_id (int): ID of the item to update.
        payload (ItemIn): An Item object with updates.

    Returns:
        success (bool): True if successfully updated.
    """
    item = get_object_or_404(Item, id=item_id)
    item.name = payload.name
    item.matches = payload.matches
    item.save()
    broadcast_invalidate(["items"])
    return {"success": True}


@api.put("/listitems/{listitem_id}")
def update_listitem(request, listitem_id: int, payload: ListItemIn):
    """
    The function `update_listitem` updates a ListItem.

    Endpoint:
        - **Path**: `/api/listitems/{listitem_id}`
        - **Method**: `PUT`

    Args:
        request ():
        listitem_id (int): The ID of a ListItem to update.
        payload (ListItemIn): A ListItem object with updates.

    Returns:
        success (bool): True if successfully updated.
    """
    listitem = get_object_or_404(ListItem, id=listitem_id)
    listitem.qty = payload.qty
    listitem.purchased = payload.purchased
    listitem.notes = payload.notes
    listitem.purch_date = payload.purch_date
    listitem.item_id = payload.item_id
    listitem.aisle_id = payload.aisle_id
    listitem.shopping_list_id = payload.shopping_list_id
    listitem.save()
    # Ticking off a row that was split out from a bought one puts both in the
    # cart; unticking does the same in reverse. Either way they fold back into
    # a single line. A no-op unless a genuine duplicate exists, so editing the
    # notes or quantity of an ordinary row is unaffected.
    merge_duplicate_listitem(listitem)
    broadcast_invalidate(["fullshoppinglist", "shoppinglists"])
    return {"success": True}


@api.put("/shoppinglists/{shoppinglist_id}")
def update_shoppinglist(request, shoppinglist_id: int, payload: ShoppingListIn):
    """
    The function `update_shoppinglist` updates a given ShoppingList.

    Endpoint:
        - **Path**: `/api/shoppinglists/{shoppinglist_id}`
        - **Method**: `PUT`

    Args:
        request ():
        shoppinglist_id (int): ID of the Shoppinglist to update.
        payload (ShoppingListIn): A ShoppingList object with updates.

    Returns:
        success (bpp;): True if successfully updated.
    """
    shoppinglist = get_object_or_404(ShoppingList, id=shoppinglist_id)
    shoppinglist.name = payload.name
    shoppinglist.store_id = payload.store_id
    shoppinglist.save()
    broadcast_invalidate(["shoppinglists"])
    return {"success": True}


@api.delete("/aisles/{aisle_id}")
def delete_aisle(request, aisle_id: int):
    """
    The function `delete_aisle` deletes a given Aisle.

    Endpoint:
        - **Path**: `/api/aisles/{aisle_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        aisle_id (int): ID of an Aisle to delete.

    Returns:
        success (bool): True if successfully deleted.
    """
    aisle = get_object_or_404(Aisle, id=aisle_id)
    aisle.delete()
    broadcast_invalidate(["aisles"])
    return {"success": True}


@api.delete("/items/{item_id}")
def delete_item(request, item_id: int):
    """
    The function `delete_item` deletes a given Item.

    Endpoint:
        - **Path**: `/api/items/{item_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        item_id (int): ID of an Item to delete.

    Returns:
        success (bool): True if successfully deleted.
    """
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    broadcast_invalidate(["items"])
    return {"success": True}


# Photos are uploaded on their own endpoints rather than folded into the item
# PUT, because the rest of the API is JSON and a file has to arrive as
# multipart. Keeping them separate also means the frontend can save a rename
# without re-sending a 1MB photo.
#
# A photo on an Item shows up on shopping list rows, so writing one has to
# invalidate the list keys as well as "items" — the row is rendered from
# ListItemOut.item, not from a separate items fetch.
ITEM_IMAGE_KEYS = ["items", "fullshoppinglist", "shoppinglists"]
FREEZERITEM_IMAGE_KEYS = ["freezers", "freezeritems", "freezerfull"]


def store_upload(obj, upload):
    """
    Replaces an object's photo with a newly uploaded one.

    Args:
        obj (Model): An Item or FreezerItem.
        upload (UploadedFile): The uploaded photo.

    Returns:
        (Model): The saved object.

    Raises:
        HttpError: 400 if the upload is not a usable image.
    """
    try:
        full, thumb = build_renditions(upload)
    except ImageUploadError as error:
        raise HttpError(400, str(error))

    # The old files are dropped first so replacing a photo does not strand the
    # previous pair on the media volume. save=False because the field
    # assignments below are about to write the row anyway.
    delete_renditions(obj)

    obj.image.save(full.name, full, save=False)
    obj.thumbnail.save(thumb.name, thumb, save=False)
    obj.save()
    return obj


def clear_upload(obj):
    """
    Removes an object's photo, leaving the object itself alone.

    Args:
        obj (Model): An Item or FreezerItem.

    Returns:
        (Model): The saved object.
    """
    delete_renditions(obj)
    obj.image = None
    obj.thumbnail = None
    obj.save()
    return obj


@api.post("/items/{item_id}/image", response=ItemOut)
def upload_item_image(request, item_id: int, image: UploadedFile = File(...)):
    """
    The function `upload_item_image` sets the photo for an Item, replacing any
    photo already on it.

    Endpoint:
        - **Path**: `/api/items/{item_id}/image`
        - **Method**: `POST`

    Args:
        request ():
        item_id (int): ID of the Item to attach the photo to.
        image (UploadedFile): The uploaded photo, as multipart form data.

    Returns:
        (ItemOut): The Item, with its new image paths.
    """
    item = get_object_or_404(Item, id=item_id)
    item = store_upload(item, image)
    broadcast_invalidate(ITEM_IMAGE_KEYS)
    return item


@api.delete("/items/{item_id}/image", response=ItemOut)
def delete_item_image(request, item_id: int):
    """
    The function `delete_item_image` removes the photo from an Item.

    Endpoint:
        - **Path**: `/api/items/{item_id}/image`
        - **Method**: `DELETE`

    Args:
        request ():
        item_id (int): ID of the Item to remove the photo from.

    Returns:
        (ItemOut): The Item, with its image paths cleared.
    """
    item = get_object_or_404(Item, id=item_id)
    item = clear_upload(item)
    broadcast_invalidate(ITEM_IMAGE_KEYS)
    return item


@api.post("/freezeritems/{freezeritem_id}/image", response=FreezerItemOut)
def upload_freezeritem_image(
    request, freezeritem_id: int, image: UploadedFile = File(...)
):
    """
    The function `upload_freezeritem_image` sets the photo for a FreezerItem,
    replacing any photo already on it.

    Endpoint:
        - **Path**: `/api/freezeritems/{freezeritem_id}/image`
        - **Method**: `POST`

    Args:
        request ():
        freezeritem_id (int): ID of the FreezerItem to attach the photo to.
        image (UploadedFile): The uploaded photo, as multipart form data.

    Returns:
        (FreezerItemOut): The FreezerItem, with its new image paths.
    """
    freezeritem = get_object_or_404(FreezerItem, id=freezeritem_id)
    freezeritem = store_upload(freezeritem, image)
    broadcast_invalidate(FREEZERITEM_IMAGE_KEYS)
    return freezeritem


@api.delete("/freezeritems/{freezeritem_id}/image", response=FreezerItemOut)
def delete_freezeritem_image(request, freezeritem_id: int):
    """
    The function `delete_freezeritem_image` removes the photo from a
    FreezerItem.

    Endpoint:
        - **Path**: `/api/freezeritems/{freezeritem_id}/image`
        - **Method**: `DELETE`

    Args:
        request ():
        freezeritem_id (int): ID of the FreezerItem to remove the photo from.

    Returns:
        (FreezerItemOut): The FreezerItem, with its image paths cleared.
    """
    freezeritem = get_object_or_404(FreezerItem, id=freezeritem_id)
    freezeritem = clear_upload(freezeritem)
    broadcast_invalidate(FREEZERITEM_IMAGE_KEYS)
    return freezeritem


@api.delete("/listitems/{listitem_id}")
def delete_listitem(request, listitem_id: int):
    """
    The function `delete_listitem` deletes a given ListItem.

    Endpoint:
        - **Path**: `/api/listitems/{listitem_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        listitem_id (int): ID of an ListItem to delete.

    Returns:
        success (bool): True if successfully deleted.
    """
    listitem = get_object_or_404(ListItem, id=listitem_id)
    listitem.delete()
    broadcast_invalidate(["fullshoppinglist", "shoppinglists"])
    return {"success": True}


@api.delete("/listitems/deleteall/{shoppinglist_id}")
def delete_listitems_by_shoppinglist(request, shoppinglist_id: int):
    """
    The function `delete_listitems_by_shoppinglist` deletes all ListItems for
    a given ShoppingList ID.

    Endpoint:
        - **Path**: `/api/listitems/deleteall/{shoppinglist_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        shoppinglist_id (int): ID of a ShoppingList.

    Returns:
        success (bool): True if successfully deleted.
    """
    listitems = ListItem.objects.filter(shopping_list_id=shoppinglist_id)
    listitems.delete()
    broadcast_invalidate(["fullshoppinglist", "shoppinglists"])
    return {"success": True}


@api.delete("/listitems/deletepurchased/{shoppinglist_id}")
def delete_purchased_listitems_by_shoppinglist(request, shoppinglist_id: int):
    """
    The function `delete_purchased_listitems_by_shoppinglist` deletes all ListItems
    markded as purchased on a given ShoppingList.

    Endpoint:
        - **Path**: `/api/listitems/deletepurchased/{shoppinglist_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        shoppinglist_id (int): ID of a ShoppingList.

    Returns:
        success (bool): True if successfully deleted.
    """
    listitems = ListItem.objects.filter(
        shopping_list_id=shoppinglist_id, purchased=True
    )
    listitems.delete()
    broadcast_invalidate(["fullshoppinglist", "shoppinglists"])
    return {"success": True}


@api.delete("/shoppinglists/{shoppinglist_id}")
def delete_shoppinglist(request, shoppinglist_id: int):
    """
    The function `delete_shoppinglist` deletes a given ShoppingList.

    Endpoint:
        - **Path**: `/api/shoppinglists/{shoppinglist_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        shoppinglist_id (int): ID of a ShoppingList to delete.

    Returns:
        success (bool): True if successfully deleted.
    """
    shoppinglist = get_object_or_404(ShoppingList, id=shoppinglist_id)
    shoppinglist.delete()
    broadcast_invalidate(["shoppinglists"])
    return {"success": True}


@api.post("/stores")
def create_store(request, payload: StoreIn):
    """
    The function `create_store` creates a Store.

    Endpoint:
        - **Path**: `/api/stores`
        - **Method**: `POST`

    Args:
        request ():
        payload (StoreIn): A Store object to add.

    Returns:
        id (int): The ID of the added Store.
    """
    store = Store.objects.create(**payload.dict())
    broadcast_invalidate(["stores"])
    return {"id": store.id}


@api.get("/stores/{store_id}", response=StoreOut)
def get_store(request, store_id: int):
    """
    The function `get_store` returns a Store object for a given ID.

    Endpoint:
        - **Path**: `/api/stores/{store_id}`
        - **Method**: `GET`

    Args:
        request ():
        store_id (int): ID of a Store to retreive.

    Returns:
        (StoreOut): A Store object.
    """
    store = get_object_or_404(Store, id=store_id)
    return store


@api.get("/stores", response=List[StoreOut])
def list_stores(request):
    """
    The function `list_stores` returns a list of Stores.

    Endpoint:
        - **Path**: `/api/stores`
        - **Method**: `GET`

    Args:
        request ():

    Returns:
        (List[StoreOut]): A list of Store objects.
    """
    qs = Store.objects.all()
    return qs


@api.put("/stores/{store_id}")
def update_store(request, store_id: int, payload: StoreIn):
    """
    The function `update_store` updates a give Store.

    Endpoint:
        - **Path**: `/api/stores/{store_id}`
        - **Method**: `PUT`

    Args:
        request ():
        store_id (int): ID of a Store to update.
        payload (StoreIn): A Store object with updates.

    Returns:
        success (bool): True if successfully updated.
    """
    store = get_object_or_404(Store, id=store_id)
    store.name = payload.name
    store.save()
    broadcast_invalidate(["stores"])
    return {"success": True}


@api.delete("/stores/{store_id}")
def delete_store(request, store_id: int):
    """
    The function `delete_store` deletes a given Store.

    Endpoint:
        - **Path**: `/api/stores/{store_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        store_id (int): ID of a Store to delete.

    Returns:
        success (bool): True if successfully deleted.
    """
    store = get_object_or_404(Store, id=store_id)
    store.delete()
    broadcast_invalidate(["stores"])
    return {"success": True}


@api.post("/freezers")
def create_freezer(request, payload: FreezerIn):
    """
    The function `create_freezer` creates a Freezer.

    Endpoint:
        - **Path**: `/api/freezers`
        - **Method**: `POST`

    Args:
        request ():
        payload (FreezerIn): A Freezer object to add.

    Returns:
        id (int): The ID of the added Freezer.
    """
    freezer = Freezer.objects.create(**payload.dict())
    broadcast_invalidate(["freezers"])
    return {"id": freezer.id}


@api.get("/freezers/{freezer_id}", response=FreezerOut)
def get_freezer(request, freezer_id: int):
    """
    The function `get_freezer` returns a Freezer object for a given ID.

    Endpoint:
        - **Path**: `/api/freezers/{freezer_id}`
        - **Method**: `GET`

    Args:
        request ():
        freezer_id (int): ID of a Freezer to retreive.

    Returns:
        (FreezerOut): A Freezer object.
    """
    freezer = get_object_or_404(freezer_queryset(), id=freezer_id)
    return freezer


@api.get("/freezers", response=List[FreezerOut])
def list_freezers(request):
    """
    The function `list_freezers` returns a list of Freezers.

    Endpoint:
        - **Path**: `/api/freezers`
        - **Method**: `GET`

    Args:
        request ():

    Returns:
        (List[FreezerOut]): A list of Freezer objects.
    """
    qs = freezer_queryset().order_by("name")
    return qs


@api.put("/freezers/{freezer_id}")
def update_freezer(request, freezer_id: int, payload: FreezerIn):
    """
    The function `update_freezer` updates a given Freezer.

    Endpoint:
        - **Path**: `/api/freezers/{freezer_id}`
        - **Method**: `PUT`

    Args:
        request ():
        freezer_id (int): ID of a Freezer to update.
        payload (FreezerIn): A Freezer object with updates.

    Returns:
        success (bool): True if successfully updated.
    """
    freezer = get_object_or_404(Freezer, id=freezer_id)
    freezer.name = payload.name
    freezer.location = payload.location
    freezer.save()
    broadcast_invalidate(["freezers", "freezerfull"])
    return {"success": True}


@api.delete("/freezers/{freezer_id}")
def delete_freezer(request, freezer_id: int):
    """
    The function `delete_freezer` deletes a given Freezer and everything in it.

    Endpoint:
        - **Path**: `/api/freezers/{freezer_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        freezer_id (int): ID of a Freezer to delete.

    Returns:
        success (bool): True if successfully deleted.
    """
    freezer = get_object_or_404(Freezer, id=freezer_id)
    freezer.delete()
    broadcast_invalidate(["freezers", "freezeritems", "freezerfull"])
    return {"success": True}


@api.get("/freezerfull/{freezer_id}", response=FreezerFull)
def get_freezerfull(request, freezer_id: int):
    """
    The function `get_freezerfull` returns a Freezer with its frozen foods.

    Items are ordered so the ones closest to their discard date come first,
    with undated items last.

    Endpoint:
        - **Path**: `/api/freezerfull/{freezer_id}`
        - **Method**: `GET`

    Args:
        request ():
        freezer_id (int): The ID of a Freezer.

    Returns:
        (FreezerFull): A FreezerFull object.
    """
    freezer = get_object_or_404(Freezer, id=freezer_id)
    freezeritems = FreezerItem.objects.filter(freezer=freezer).order_by(
        F("discard_date").asc(nulls_last=True), "name"
    )
    totalexpired = FreezerItem.objects.filter(
        freezer=freezer, discard_date__lt=date.today()
    ).count()
    return FreezerFull(
        id=freezer.id,
        name=freezer.name,
        location=freezer.location,
        freezeritems=[FreezerItemOut.from_orm(fi) for fi in freezeritems],
        totalitems=freezeritems.count(),
        totalexpired=totalexpired,
    )


@api.post("/freezeritems")
def create_freezeritem(request, payload: FreezerItemIn):
    """
    The function `create_freezeritem` creates a FreezerItem.

    Endpoint:
        - **Path**: `/api/freezeritems`
        - **Method**: `POST`

    Args:
        request ():
        payload (FreezerItemIn): A FreezerItem object to add.

    Returns:
        id (int): The ID of the added FreezerItem.
    """
    freezeritem = FreezerItem.objects.create(**payload.dict())
    # "freezers" too: the freezer list carries the dashboard's item and expiry
    # counts, so they go stale whenever an item is added, changed or removed.
    broadcast_invalidate(["freezers", "freezeritems", "freezerfull"])
    return {"id": freezeritem.id}


@api.get("/freezeritems/{freezeritem_id}", response=FreezerItemOut)
def get_freezeritem(request, freezeritem_id: int):
    """
    The function `get_freezeritem` returns a FreezerItem for a given ID.

    Endpoint:
        - **Path**: `/api/freezeritems/{freezeritem_id}`
        - **Method**: `GET`

    Args:
        request ():
        freezeritem_id (int): ID of a FreezerItem to retreive.

    Returns:
        (FreezerItemOut): A FreezerItem object.
    """
    freezeritem = get_object_or_404(FreezerItem, id=freezeritem_id)
    return freezeritem


@api.get("/freezeritems", response=List[FreezerItemOut])
def list_freezeritems(request):
    """
    The function `list_freezeritems` returns a list of all FreezerItems.

    Endpoint:
        - **Path**: `/api/freezeritems`
        - **Method**: `GET`

    Args:
        request ():

    Returns:
        (List[FreezerItemOut]): A list of FreezerItem objects.
    """
    qs = FreezerItem.objects.all().order_by(
        F("discard_date").asc(nulls_last=True), "name"
    )
    return qs


@api.get("/freezeritemsbyfreezer/{freezer_id}", response=List[FreezerItemOut])
def list_freezeritemsbyfreezer(request, freezer_id: int):
    """
    The function `list_freezeritemsbyfreezer` returns the FreezerItems in a
    given Freezer.

    Endpoint:
        - **Path**: `/api/freezeritemsbyfreezer/{freezer_id}`
        - **Method**: `GET`

    Args:
        request ():
        freezer_id (int): ID of the Freezer to list frozen foods for.

    Returns:
        (List[FreezerItemOut]): A list of FreezerItem objects.
    """
    qs = FreezerItem.objects.filter(freezer_id=freezer_id).order_by(
        F("discard_date").asc(nulls_last=True), "name"
    )
    return qs


@api.get("/freezeritemsexpiring", response=List[FreezerItemOut])
def list_freezeritemsexpiring(request, days: int = FREEZER_SOON_DAYS):
    """
    The function `list_freezeritemsexpiring` returns FreezerItems that are
    already past their discard date or reach it within `days` days.

    Endpoint:
        - **Path**: `/api/freezeritemsexpiring`
        - **Method**: `GET`

    Args:
        request ():
        days (int): How many days ahead to look. Default = 14.

    Returns:
        (List[FreezerItemOut]): A list of FreezerItem objects.
    """
    cutoff = date.today() + timedelta(days=days)
    qs = FreezerItem.objects.filter(
        discard_date__isnull=False, discard_date__lte=cutoff
    ).order_by("discard_date", "name")
    return qs


@api.put("/freezeritems/{freezeritem_id}")
def update_freezeritem(request, freezeritem_id: int, payload: FreezerItemIn):
    """
    The function `update_freezeritem` updates a given FreezerItem.

    Endpoint:
        - **Path**: `/api/freezeritems/{freezeritem_id}`
        - **Method**: `PUT`

    Args:
        request ():
        freezeritem_id (int): ID of a FreezerItem to update.
        payload (FreezerItemIn): A FreezerItem object with updates.

    Returns:
        success (bool): True if successfully updated.
    """
    freezeritem = get_object_or_404(FreezerItem, id=freezeritem_id)
    freezeritem.name = payload.name
    freezeritem.qty = payload.qty
    freezeritem.unit = payload.unit
    # Assigned unconditionally: None is a meaningful value here ("date added
    # unknown"), so clearing the field has to be possible.
    freezeritem.date_added = payload.date_added
    freezeritem.discard_date = payload.discard_date
    freezeritem.notes = payload.notes
    freezeritem.freezer_id = payload.freezer_id
    freezeritem.save()
    # "freezers" too: the freezer list carries the dashboard's item and expiry
    # counts, so they go stale whenever an item is added, changed or removed.
    broadcast_invalidate(["freezers", "freezeritems", "freezerfull"])
    return {"success": True}


@api.delete("/freezeritems/{freezeritem_id}")
def delete_freezeritem(request, freezeritem_id: int):
    """
    The function `delete_freezeritem` deletes a given FreezerItem.

    Endpoint:
        - **Path**: `/api/freezeritems/{freezeritem_id}`
        - **Method**: `DELETE`

    Args:
        request ():
        freezeritem_id (int): ID of a FreezerItem to delete.

    Returns:
        success (bool): True if successfully deleted.
    """
    freezeritem = get_object_or_404(FreezerItem, id=freezeritem_id)
    freezeritem.delete()
    # "freezers" too: the freezer list carries the dashboard's item and expiry
    # counts, so they go stale whenever an item is added, changed or removed.
    broadcast_invalidate(["freezers", "freezeritems", "freezerfull"])
    return {"success": True}


@api.get("/version/list", response=VersionOut)
def list_version(request):
    """
    The function `list_version` retrieves the app version number
    from the backend.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (VersionOut): a version object
    """

    return {"version_number": api.version}


@api.post("/demo/load", response={200: dict, 409: dict})
def load_demo_data(request):
    """
    Load demo stores, aisles, items, and shopping lists.
    Only succeeds if no stores exist yet.
    Returns 409 if the database already has store data.
    """
    if Store.objects.exists():
        raise HttpError(409, "Demo data not loaded: stores already exist.")
    call_command("load_demo_data")
    return {"success": True, "message": "Demo data loaded successfully."}
