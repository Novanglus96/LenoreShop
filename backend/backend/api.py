from ninja import NinjaAPI, Schema, Query
from api.models import Store, Aisle, Item, ListItem, ShoppingList, Version
from typing import List, Optional
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.paginator import Paginator

api = NinjaAPI()
api.title = "Shopping API"
api.version = "1.5.7"
api.description = "API documentation for Shopping"


class VersionOut(Schema):
    id: int
    version_number: str


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None
    first_name: str = None
    last_name: str = None


class StoreIn(Schema):
    name: str


class StoreOut(Schema):
    id: int
    name: str


class AisleIn(Schema):
    name: str
    order: int = 1
    store_id: int


class AisleOut(Schema):
    id: int
    name: str
    order: int = 1
    store_id: int
    store: StoreOut


class ItemIn(Schema):
    name: str
    matches: str = None
    aisle: Optional[AisleOut]


class ItemOut(Schema):
    id: int
    name: str
    matches: str = None
    aisle: Optional[AisleOut]


class PaginatedItems(Schema):
    items: List[ItemOut]
    current_page: int
    total_pages: int
    total_records: int


class ListItemIn(Schema):
    qty: int = 1
    purchased: bool = False
    notes: str = None
    purch_date: date = None
    item_id: int
    aisle_id: int
    shopping_list_id: int


class ListItemOut(Schema):
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
    name: str
    store_id: int


class ShoppingListOut(Schema):
    id: int
    name: str
    store_id: int
    store: StoreOut


class AislesWithItems(Schema):
    id: int
    name: str
    order: int = 1
    store_id: int
    listitems: List[ListItemOut]


class ShoppingListFull(Schema):
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
    return request.user


@api.post("/aisles")
def create_aisle(request, payload: AisleIn):
    aisle = Aisle.objects.create(**payload.dict())
    return {"id": aisle.id}


@api.post("/items", response=ItemOut)
def create_item(request, payload: ItemIn):
    item = Item.objects.create(**payload.dict())
    return item


@api.post("/listitems")
def create_listitem(request, payload: ListItemIn):
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
        existing_item.save()
        return {"id": existing_item.id}


@api.post("/shoppinglists")
def create_shoppinglist(request, payload: ShoppingListIn):
    shoppinglist = ShoppingList.objects.create(**payload.dict())
    return {"id": shoppinglist.id}


@api.get("/aisles/{aisle_id}", response=AisleOut)
def get_aisle(request, aisle_id: int):
    aisle = get_object_or_404(Aisle, id=aisle_id)
    return aisle


@api.get("/items/{item_id}", response=ItemOut)
def get_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    return item


@api.get("/listitems/{listitem_id}", response=ListItemOut)
def get_listitem(request, listitem_id: int):
    listitem = get_object_or_404(ListItem, id=listitem_id)
    return listitem


@api.get("/shoppinglists/{shoppinglist_id}", response=ShoppingListOut)
def get_shoppinglist(request, shoppinglist_id: int):
    shoppinglist = get_object_or_404(ShoppingList, id=shoppinglist_id)
    return shoppinglist


@api.get("/shoppinglistfull/{shoppinglist_id}", response=ShoppingListFull)
def get_shoppinglistfull(request, shoppinglist_id: int):
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
    qs = Aisle.objects.all()
    return qs


@api.get("/aislesbystore/{store_id}", response=List[AisleOut])
def list_aislesbystore(request, store_id: int):
    qs = Aisle.objects.all().filter(store__id=store_id).order_by("order")
    return qs


@api.get("/items", response=PaginatedItems)
def list_items(
    request,
    page: Optional[int] = Query(1),
    page_size: Optional[int] = Query(15),
    full: Optional[bool] = Query(False),
):
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
    qs = ListItem.objects.all()
    return qs


@api.get("/shoppinglists", response=List[ShoppingListOut])
def list_shoppinglists(request):
    qs = ShoppingList.objects.all()
    return qs


@api.get("/listsbystore/{store_id}", response=List[ShoppingListOut])
def list_listsbystore(request, store_id: int):
    qs = ShoppingList.objects.all().filter(store__id=store_id)
    return qs


@api.put("/aisles/{aisle_id}")
def update_aisle(request, aisle_id: int, payload: AisleIn):
    aisle = get_object_or_404(Aisle, id=aisle_id)
    aisle.name = payload.name
    aisle.order = payload.order
    aisle.store_id = payload.store_id
    aisle.save()
    return {"success": True}


@api.put("/items/{item_id}")
def update_item(request, item_id: int, payload: ItemIn):
    item = get_object_or_404(Item, id=item_id)
    item.name = payload.name
    item.matches = payload.matches
    item.save()
    return {"success": True}


@api.put("/listitems/{listitem_id}")
def update_listitem(request, listitem_id: int, payload: ListItemIn):
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
    shoppinglist = get_object_or_404(ShoppingList, id=shoppinglist_id)
    shoppinglist.name = payload.name
    shoppinglist.store_id = payload.store_id
    shoppinglist.save()
    return {"success": True}


@api.delete("/aisles/{aisle_id}")
def delete_aisle(request, aisle_id: int):
    aisle = get_object_or_404(Aisle, id=aisle_id)
    aisle.delete()
    return {"success": True}


@api.delete("/items/{item_id}")
def delete_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return {"success": True}


@api.delete("/listitems/{listitem_id}")
def delete_listitem(request, listitem_id: int):
    listitem = get_object_or_404(ListItem, id=listitem_id)
    listitem.delete()
    return {"success": True}


@api.delete("/listitems/deleteall/{shoppinglist_id}")
def delete_listitems_by_shoppinglist(request, shoppinglist_id: int):
    listitems = ListItem.objects.filter(shopping_list_id=shoppinglist_id)
    listitems.delete()
    return {"success": True}


@api.delete("/listitems/deletepurchased/{shoppinglist_id}")
def delete_purchased_listitems_by_shoppinglist(request, shoppinglist_id: int):
    listitems = ListItem.objects.filter(
        shopping_list_id=shoppinglist_id, purchased=True
    )
    listitems.delete()
    return {"success": True}


@api.delete("/shoppinglists/{shoppinglist_id}")
def delete_shoppinglist(request, shoppinglist_id: int):
    shoppinglist = get_object_or_404(ShoppingList, id=shoppinglist_id)
    shoppinglist.delete()
    return {"success": True}


@api.post("/stores")
def create_store(request, payload: StoreIn):
    store = Store.objects.create(**payload.dict())
    return {"id": store.id}


@api.get("/stores/{store_id}", response=StoreOut)
def get_store(request, store_id: int):
    store = get_object_or_404(Store, id=store_id)
    return store


@api.get("/stores", response=List[StoreOut])
def list_stores(request):
    qs = Store.objects.all()
    return qs


@api.put("/stores/{store_id}")
def update_store(request, store_id: int, payload: StoreIn):
    store = get_object_or_404(Store, id=store_id)
    store.name = payload.name
    store.save()
    return {"success": True}


@api.delete("/stores/{store_id}")
def delete_store(request, store_id: int):
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
        VersionOut: a version object
    """

    try:
        qs = get_object_or_404(Version, id=1)
        return qs
    except Exception as e:
        raise HttpError(500, f"Record retrieval error: {str(e)}")
