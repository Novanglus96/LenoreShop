from ninja import NinjaAPI, Schema, Query
from api.models import Store, Aisle, Item, ListItem, ShoppingList, Version
from typing import List, Optional
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from datetime import date
from django.core.paginator import Paginator

api = NinjaAPI()
api.title = "LenoreShop API"
api.version = "1.6.21"
api.description = "API documentation for LenoreShop"


# The class VersionOut is a scheam for representing Version information.
class VersionOut(Schema):
    """
    Schema to represent a Version.

    Attributes:
        id (int): ID integer. Unique.
        version_number (str): The version of the app.
    """

    id: int
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
    """

    id: int
    name: str
    matches: str = None
    aisle: Optional[AisleOut]


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


class ShoppingListOut(Schema):
    """
    Schema to represent a ShoppingList.

    Attributes:
        id (int): ID of the shopping list.
        name (str): The name of the shopping list.
        store_id (int): The ID of the store for the shopping list.
        store (StoreOut): The Store object.
    """

    id: int
    name: str
    store_id: int
    store: StoreOut


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
    return item


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
    existing_item = ListItem.objects.filter(
        shopping_list_id=payload.shopping_list_id, item_id=payload.item_id
    ).first()
    if existing_item is None:
        listitem = ListItem.objects.create(**payload.dict())
        item = Item.objects.get(id=payload.item_id)
        item.aisle_id = payload.aisle_id
        item.save()
        return {"id": listitem.id}
    else:
        existing_item.qty += payload.qty
        existing_item.purchased = False
        existing_item.save()
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
    shoppinglist = get_object_or_404(ShoppingList, id=shoppinglist_id)
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
    listitems = ListItem.objects.filter(
        shopping_list=shoppinglist, purchased=False
    ).order_by("purchased", "item__name")
    purchasedlistitems = ListItem.objects.filter(
        shopping_list=shoppinglist, purchased=True
    ).order_by("purchased", "item__name")
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
                item=ItemOut(
                    id=listitem.item.id,
                    name=listitem.item.name,
                    matches=listitem.item.matches,
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
                item=ItemOut(
                    id=listitem.item.id,
                    name=listitem.item.name,
                    matches=listitem.item.matches,
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
    qs = ShoppingList.objects.all()
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
    qs = ShoppingList.objects.all().filter(store__id=store_id)
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
    return {"success": True}


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

    try:
        qs = get_object_or_404(Version, id=1)
        return qs
    except Exception as e:
        raise HttpError(500, f"Record retrieval error: {str(e)}")
