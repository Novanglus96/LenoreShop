from datetime import date, timedelta

from django.db.utils import IntegrityError
from django.test import TestCase

from backend.api import (
    FREEZER_PREVIEW_ITEM_COUNT,
    FREEZER_SOON_DAYS,
    LIST_PREVIEW_ITEM_COUNT,
)

from .models import Aisle, Freezer, FreezerItem, Item, ListItem, ShoppingList, Store


class FreezerModelTests(TestCase):
    """
    Tests for the Freezer and FreezerItem models.
    """

    def setUp(self):
        self.freezer = Freezer.objects.create(name="Garage", location="Garage")

    def test_date_added_is_unknown_when_not_given(self):
        item = FreezerItem.objects.create(name="Peas", freezer=self.freezer)
        self.assertIsNone(item.date_added)

    def test_days_until_discard_is_none_without_a_discard_date(self):
        item = FreezerItem.objects.create(name="Peas", freezer=self.freezer)
        self.assertIsNone(item.days_until_discard)
        self.assertFalse(item.is_expired)

    def test_days_until_discard_counts_forward(self):
        item = FreezerItem.objects.create(
            name="Chicken",
            freezer=self.freezer,
            discard_date=date.today() + timedelta(days=10),
        )
        self.assertEqual(item.days_until_discard, 10)
        self.assertFalse(item.is_expired)

    def test_days_until_discard_goes_negative_once_past(self):
        item = FreezerItem.objects.create(
            name="Old chili",
            freezer=self.freezer,
            discard_date=date.today() - timedelta(days=3),
        )
        self.assertEqual(item.days_until_discard, -3)
        self.assertTrue(item.is_expired)

    def test_discarding_today_is_not_yet_expired(self):
        item = FreezerItem.objects.create(
            name="Fish", freezer=self.freezer, discard_date=date.today()
        )
        self.assertEqual(item.days_until_discard, 0)
        self.assertFalse(item.is_expired)

    def test_freezer_names_are_unique(self):
        with self.assertRaises(IntegrityError):
            Freezer.objects.create(name="Garage")

    def test_deleting_a_freezer_removes_its_contents(self):
        FreezerItem.objects.create(name="Peas", freezer=self.freezer)
        self.freezer.delete()
        self.assertEqual(FreezerItem.objects.count(), 0)


class FreezerAPITests(TestCase):
    """
    Tests for the Freezer and FreezerItem API endpoints.
    """

    def setUp(self):
        self.freezer = Freezer.objects.create(name="Garage", location="Garage")

    def post(self, path, payload):
        return self.client.post(path, payload, content_type="application/json")

    def put(self, path, payload):
        return self.client.put(path, payload, content_type="application/json")

    def test_create_and_list_freezers(self):
        response = self.post("/api/freezers", {"name": "Kitchen"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

        response = self.client.get("/api/freezers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([f["name"] for f in response.json()], ["Garage", "Kitchen"])

    def test_update_and_delete_a_freezer(self):
        response = self.put(
            f"/api/freezers/{self.freezer.id}",
            {"name": "Basement", "location": "Downstairs"},
        )
        self.assertEqual(response.status_code, 200)
        self.freezer.refresh_from_db()
        self.assertEqual(self.freezer.name, "Basement")
        self.assertEqual(self.freezer.location, "Downstairs")

        response = self.client.delete(f"/api/freezers/{self.freezer.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Freezer.objects.count(), 0)

    def test_missing_freezer_returns_404(self):
        self.assertEqual(self.client.get("/api/freezers/9999").status_code, 404)

    def test_create_freezeritem_without_a_date_added_is_unknown(self):
        response = self.post(
            "/api/freezeritems", {"name": "Peas", "freezer_id": self.freezer.id}
        )
        self.assertEqual(response.status_code, 200)
        item = FreezerItem.objects.get(id=response.json()["id"])
        self.assertIsNone(item.date_added)
        self.assertEqual(item.qty, 1)

    def test_unknown_date_added_is_serialised_as_null(self):
        item = FreezerItem.objects.create(name="Peas", freezer=self.freezer)
        response = self.client.get(f"/api/freezeritems/{item.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["date_added"])

    def test_create_freezeritem_honours_an_explicit_date_added(self):
        response = self.post(
            "/api/freezeritems",
            {
                "name": "Beef",
                "qty": 3,
                "unit": "lbs",
                "freezer_id": self.freezer.id,
                "date_added": "2026-01-15",
                "discard_date": "2026-07-15",
            },
        )
        self.assertEqual(response.status_code, 200)
        item = FreezerItem.objects.get(id=response.json()["id"])
        self.assertEqual(item.date_added, date(2026, 1, 15))
        self.assertEqual(item.discard_date, date(2026, 7, 15))
        self.assertEqual(item.qty, 3)
        self.assertEqual(item.unit, "lbs")

    def test_freezeritem_response_exposes_discard_countdown(self):
        item = FreezerItem.objects.create(
            name="Chicken",
            freezer=self.freezer,
            discard_date=date.today() + timedelta(days=5),
        )
        response = self.client.get(f"/api/freezeritems/{item.id}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["days_until_discard"], 5)
        self.assertFalse(body["is_expired"])

    def test_update_freezeritem_can_clear_the_discard_date(self):
        item = FreezerItem.objects.create(
            name="Chicken", freezer=self.freezer, discard_date=date.today()
        )
        response = self.put(
            f"/api/freezeritems/{item.id}",
            {"name": "Chicken", "qty": 2, "freezer_id": self.freezer.id},
        )
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertIsNone(item.discard_date)
        self.assertEqual(item.qty, 2)

    def test_update_freezeritem_can_clear_the_date_added(self):
        item = FreezerItem.objects.create(
            name="Chicken", freezer=self.freezer, date_added=date(2026, 1, 1)
        )
        self.put(
            f"/api/freezeritems/{item.id}",
            {"name": "Chicken thighs", "freezer_id": self.freezer.id},
        )
        item.refresh_from_db()
        self.assertIsNone(item.date_added)
        self.assertEqual(item.name, "Chicken thighs")

    def test_update_freezeritem_can_set_a_date_added_that_was_unknown(self):
        item = FreezerItem.objects.create(name="Chicken", freezer=self.freezer)
        self.put(
            f"/api/freezeritems/{item.id}",
            {
                "name": "Chicken",
                "freezer_id": self.freezer.id,
                "date_added": "2026-02-02",
            },
        )
        item.refresh_from_db()
        self.assertEqual(item.date_added, date(2026, 2, 2))

    def test_update_freezeritem_can_move_it_to_another_freezer(self):
        other = Freezer.objects.create(name="Kitchen")
        item = FreezerItem.objects.create(name="Peas", freezer=self.freezer)
        self.put(
            f"/api/freezeritems/{item.id}",
            {"name": "Peas", "freezer_id": other.id},
        )
        item.refresh_from_db()
        self.assertEqual(item.freezer_id, other.id)

    def test_delete_freezeritem(self):
        item = FreezerItem.objects.create(name="Peas", freezer=self.freezer)
        response = self.client.delete(f"/api/freezeritems/{item.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FreezerItem.objects.count(), 0)

    def test_list_freezeritems_by_freezer(self):
        other = Freezer.objects.create(name="Kitchen")
        FreezerItem.objects.create(name="Peas", freezer=self.freezer)
        FreezerItem.objects.create(name="Corn", freezer=other)

        response = self.client.get(f"/api/freezeritemsbyfreezer/{self.freezer.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([i["name"] for i in response.json()], ["Peas"])

    def test_freezerfull_orders_by_discard_date_with_undated_last(self):
        FreezerItem.objects.create(name="Undated", freezer=self.freezer)
        FreezerItem.objects.create(
            name="Later",
            freezer=self.freezer,
            discard_date=date.today() + timedelta(days=30),
        )
        FreezerItem.objects.create(
            name="Soonest",
            freezer=self.freezer,
            discard_date=date.today() + timedelta(days=1),
        )

        response = self.client.get(f"/api/freezerfull/{self.freezer.id}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(
            [i["name"] for i in body["freezeritems"]], ["Soonest", "Later", "Undated"]
        )
        self.assertEqual(body["totalitems"], 3)
        self.assertEqual(body["totalexpired"], 0)

    def test_freezerfull_counts_expired_items(self):
        FreezerItem.objects.create(
            name="Old chili",
            freezer=self.freezer,
            discard_date=date.today() - timedelta(days=1),
        )
        FreezerItem.objects.create(
            name="Today",
            freezer=self.freezer,
            discard_date=date.today(),
        )
        FreezerItem.objects.create(name="Undated", freezer=self.freezer)

        body = self.client.get(f"/api/freezerfull/{self.freezer.id}").json()
        self.assertEqual(body["totalitems"], 3)
        self.assertEqual(body["totalexpired"], 1)

    def test_expiring_endpoint_includes_overdue_and_upcoming_only(self):
        FreezerItem.objects.create(
            name="Overdue",
            freezer=self.freezer,
            discard_date=date.today() - timedelta(days=5),
        )
        FreezerItem.objects.create(
            name="Within window",
            freezer=self.freezer,
            discard_date=date.today() + timedelta(days=3),
        )
        FreezerItem.objects.create(
            name="Far off",
            freezer=self.freezer,
            discard_date=date.today() + timedelta(days=90),
        )
        FreezerItem.objects.create(name="Undated", freezer=self.freezer)

        response = self.client.get("/api/freezeritemsexpiring")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [i["name"] for i in response.json()], ["Overdue", "Within window"]
        )

    def test_unknown_date_added_still_tracks_its_discard_date(self):
        # Backfilled food with no date on the packet can still be given a
        # throw out date, and must behave like anything else.
        FreezerItem.objects.create(
            name="Mystery beef",
            freezer=self.freezer,
            discard_date=date.today() - timedelta(days=2),
        )
        body = self.client.get(f"/api/freezerfull/{self.freezer.id}").json()
        self.assertEqual(body["totalexpired"], 1)
        self.assertIsNone(body["freezeritems"][0]["date_added"])
        self.assertTrue(body["freezeritems"][0]["is_expired"])

        expiring = self.client.get("/api/freezeritemsexpiring").json()
        self.assertEqual([i["name"] for i in expiring], ["Mystery beef"])

    def test_expiring_endpoint_window_is_configurable(self):
        FreezerItem.objects.create(
            name="Far off",
            freezer=self.freezer,
            discard_date=date.today() + timedelta(days=90),
        )
        response = self.client.get("/api/freezeritemsexpiring?days=120")
        self.assertEqual([i["name"] for i in response.json()], ["Far off"])


class FreezerCardTests(TestCase):
    """
    Tests for the counts and preview lines the dashboard freezer cards render.
    """

    def setUp(self):
        self.freezer = Freezer.objects.create(name="Garage", location="Garage")

    def add_item(self, name, days=None):
        discard_date = None if days is None else date.today() + timedelta(days=days)
        return FreezerItem.objects.create(
            name=name, freezer=self.freezer, discard_date=discard_date
        )

    def test_empty_freezer_reports_nothing(self):
        body = self.client.get("/api/freezers").json()
        self.assertEqual(body[0]["totalitems"], 0)
        self.assertEqual(body[0]["totalexpired"], 0)
        self.assertEqual(body[0]["totalexpiring"], 0)
        self.assertEqual(body[0]["preview_items"], [])

    def test_expired_and_expiring_are_counted_separately(self):
        self.add_item("Old chili", days=-3)
        self.add_item("Peas", days=5)
        self.add_item("Chicken", days=90)
        self.add_item("Mystery beef")

        body = self.client.get("/api/freezers").json()
        self.assertEqual(body[0]["totalitems"], 4)
        self.assertEqual(body[0]["totalexpired"], 1)
        self.assertEqual(body[0]["totalexpiring"], 1)

    def test_item_due_today_counts_as_expiring_not_expired(self):
        self.add_item("Fish", days=0)

        body = self.client.get("/api/freezers").json()
        self.assertEqual(body[0]["totalexpired"], 0)
        self.assertEqual(body[0]["totalexpiring"], 1)

    def test_expiring_window_edge_is_included(self):
        self.add_item("Edge", days=FREEZER_SOON_DAYS)
        self.add_item("Past the edge", days=FREEZER_SOON_DAYS + 1)

        body = self.client.get("/api/freezers").json()
        self.assertEqual(body[0]["totalexpiring"], 1)

    def test_preview_is_ordered_soonest_first_with_undated_last(self):
        self.add_item("Chicken", days=30)
        self.add_item("Mystery beef")
        self.add_item("Old chili", days=-3)

        body = self.client.get("/api/freezers").json()
        self.assertEqual(
            [i["name"] for i in body[0]["preview_items"]],
            ["Old chili", "Chicken", "Mystery beef"],
        )

    def test_preview_carries_the_countdown_and_expiry_flag(self):
        self.add_item("Old chili", days=-3)

        body = self.client.get("/api/freezers").json()
        preview = body[0]["preview_items"][0]
        self.assertEqual(preview["days_until_discard"], -3)
        self.assertTrue(preview["is_expired"])

    def test_undated_preview_item_has_no_countdown(self):
        self.add_item("Mystery beef")

        body = self.client.get("/api/freezers").json()
        preview = body[0]["preview_items"][0]
        self.assertIsNone(preview["days_until_discard"])
        self.assertFalse(preview["is_expired"])

    def test_preview_is_capped_but_counts_are_not(self):
        for index in range(6):
            self.add_item(f"Item {index}", days=index + 1)

        body = self.client.get("/api/freezers").json()
        self.assertEqual(body[0]["totalitems"], 6)
        self.assertEqual(len(body[0]["preview_items"]), FREEZER_PREVIEW_ITEM_COUNT)

    def test_single_freezer_endpoint_carries_the_same_counts(self):
        self.add_item("Old chili", days=-3)

        body = self.client.get(f"/api/freezers/{self.freezer.id}").json()
        self.assertEqual(body["totalitems"], 1)
        self.assertEqual(body["totalexpired"], 1)

    def test_counts_are_not_inflated_by_other_freezers(self):
        kitchen = Freezer.objects.create(name="Kitchen")
        FreezerItem.objects.create(name="Ice cream", freezer=kitchen)
        self.add_item("Peas")

        body = self.client.get("/api/freezers").json()
        by_name = {row["name"]: row for row in body}
        self.assertEqual(by_name["Garage"]["totalitems"], 1)
        self.assertEqual(by_name["Kitchen"]["totalitems"], 1)

    def test_listing_does_not_query_per_freezer(self):
        for index in range(5):
            freezer = Freezer.objects.create(name=f"Freezer {index}")
            FreezerItem.objects.create(name=f"Item {index}", freezer=freezer)

        # One query for the freezers, one for the prefetched preview items.
        with self.assertNumQueries(2):
            self.client.get("/api/freezers")


class ShoppingListCardTests(TestCase):
    """
    Tests for the progress counts and preview lines the dashboard cards render.
    """

    def setUp(self):
        self.store = Store.objects.create(name="Kroger")
        self.aisle = Aisle.objects.create(name="Dairy", order=1, store=self.store)
        self.shoppinglist = ShoppingList.objects.create(
            name="Weekly", store=self.store
        )

    def add_item(self, name, purchased=False):
        item = Item.objects.create(name=name)
        return ListItem.objects.create(
            item=item,
            aisle=self.aisle,
            shopping_list=self.shoppinglist,
            purchased=purchased,
        )

    def test_empty_list_reports_no_items_and_no_preview(self):
        body = self.client.get("/api/shoppinglists").json()
        self.assertEqual(body[0]["totalitems"], 0)
        self.assertEqual(body[0]["totalpurchased"], 0)
        self.assertEqual(body[0]["preview_items"], [])

    def test_counts_track_purchased_items(self):
        self.add_item("Milk", purchased=True)
        self.add_item("Eggs")
        self.add_item("Bread")

        body = self.client.get("/api/shoppinglists").json()
        self.assertEqual(body[0]["totalitems"], 3)
        self.assertEqual(body[0]["totalpurchased"], 1)

    def test_preview_puts_unpurchased_items_first(self):
        self.add_item("Milk", purchased=True)
        self.add_item("Eggs")

        body = self.client.get("/api/shoppinglists").json()
        self.assertEqual(
            body[0]["preview_items"],
            [
                {"name": "Eggs", "purchased": False},
                {"name": "Milk", "purchased": True},
            ],
        )

    def test_preview_is_capped_but_counts_are_not(self):
        for index in range(7):
            self.add_item(f"Item {index}")

        body = self.client.get("/api/shoppinglists").json()
        self.assertEqual(body[0]["totalitems"], 7)
        self.assertEqual(len(body[0]["preview_items"]), LIST_PREVIEW_ITEM_COUNT)

    def test_single_list_endpoint_carries_the_same_counts(self):
        self.add_item("Milk", purchased=True)
        self.add_item("Eggs")

        body = self.client.get(f"/api/shoppinglists/{self.shoppinglist.id}").json()
        self.assertEqual(body["totalitems"], 2)
        self.assertEqual(body["totalpurchased"], 1)
        self.assertEqual([i["name"] for i in body["preview_items"]], ["Eggs", "Milk"])

    def test_lists_by_store_endpoint_carries_the_same_counts(self):
        self.add_item("Milk", purchased=True)

        body = self.client.get(f"/api/listsbystore/{self.store.id}").json()
        self.assertEqual(body[0]["totalitems"], 1)
        self.assertEqual(body[0]["totalpurchased"], 1)

    def test_counts_are_not_inflated_by_other_lists(self):
        other = ShoppingList.objects.create(name="Party", store=self.store)
        ListItem.objects.create(
            item=Item.objects.create(name="Chips"),
            aisle=self.aisle,
            shopping_list=other,
        )
        self.add_item("Milk")

        body = self.client.get("/api/shoppinglists").json()
        by_name = {row["name"]: row for row in body}
        self.assertEqual(by_name["Weekly"]["totalitems"], 1)
        self.assertEqual(by_name["Party"]["totalitems"], 1)

    def test_listing_does_not_query_per_list(self):
        for index in range(5):
            shoppinglist = ShoppingList.objects.create(
                name=f"List {index}", store=self.store
            )
            ListItem.objects.create(
                item=Item.objects.create(name=f"Item {index}"),
                aisle=self.aisle,
                shopping_list=shoppinglist,
            )

        # One query for the lists, one for the prefetched preview items — the count
        # must not grow with the number of lists.
        with self.assertNumQueries(2):
            self.client.get("/api/shoppinglists")

    def test_lists_are_ordered_by_store_then_name(self):
        ShoppingList.objects.create(name="Anniversary", store=self.store)
        aldi = Store.objects.create(name="Aldi")
        ShoppingList.objects.create(name="Snacks", store=aldi)

        body = self.client.get("/api/shoppinglists").json()
        self.assertEqual(
            [(row["store"]["name"], row["name"]) for row in body],
            [("Aldi", "Snacks"), ("Kroger", "Anniversary"), ("Kroger", "Weekly")],
        )


class AddExistingListItemTests(TestCase):
    """
    Tests for what POST /listitems does when the item is already on the list.

    Adding more of something still to be found should add to that line. Adding
    more of something already in the cart should start a new line instead, so
    the purchased row is left alone rather than having its quantity added to
    and being flipped back to unpurchased.
    """

    def setUp(self):
        self.store = Store.objects.create(name="Kroger")
        self.aisle = Aisle.objects.create(name="Dairy", order=1, store=self.store)
        self.shoppinglist = ShoppingList.objects.create(
            name="Weekly", store=self.store
        )
        self.milk = Item.objects.create(name="Milk")

    def post_milk(self, qty):
        return self.client.post(
            "/api/listitems",
            {
                "qty": qty,
                "item_id": self.milk.id,
                "aisle_id": self.aisle.id,
                "shopping_list_id": self.shoppinglist.id,
            },
            content_type="application/json",
        )

    def milk_rows(self):
        return ListItem.objects.filter(
            shopping_list=self.shoppinglist, item=self.milk
        ).order_by("id")

    def test_adding_to_an_unpurchased_item_sums_the_quantities(self):
        self.post_milk(2)
        self.post_milk(3)

        rows = self.milk_rows()
        self.assertEqual(rows.count(), 1)
        self.assertEqual(rows[0].qty, 5)
        self.assertFalse(rows[0].purchased)

    def test_adding_to_a_purchased_item_starts_a_new_row(self):
        first = ListItem.objects.get(id=self.post_milk(2).json()["id"])
        first.purchased = True
        first.save()

        response = self.post_milk(1)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json()["id"], first.id)

        rows = self.milk_rows()
        self.assertEqual(rows.count(), 2)

        first.refresh_from_db()
        self.assertEqual(first.qty, 2, "the purchased row keeps its quantity")
        self.assertTrue(first.purchased, "the purchased row stays purchased")

        self.assertEqual(rows[1].qty, 1)
        self.assertFalse(rows[1].purchased)

    def test_counts_after_re_adding_a_purchased_item(self):
        first = ListItem.objects.get(id=self.post_milk(2).json()["id"])
        first.purchased = True
        first.save()
        self.post_milk(1)

        body = self.client.get("/api/shoppinglists").json()[0]
        self.assertEqual(body["totalitems"], 2)
        self.assertEqual(body["totalpurchased"], 1)

    def test_a_purchased_row_is_skipped_in_favour_of_an_unpurchased_one(self):
        """
        With both a purchased and an unpurchased row present, more of the item
        merges into the unpurchased one rather than creating a third row.
        """
        bought = ListItem.objects.get(id=self.post_milk(2).json()["id"])
        bought.purchased = True
        bought.save()
        still_needed = ListItem.objects.get(id=self.post_milk(1).json()["id"])

        self.post_milk(4)

        rows = self.milk_rows()
        self.assertEqual(rows.count(), 2)
        still_needed.refresh_from_db()
        self.assertEqual(still_needed.qty, 5)
        bought.refresh_from_db()
        self.assertEqual(bought.qty, 2)
        self.assertTrue(bought.purchased)

    def test_the_full_list_shows_the_new_row_and_keeps_the_purchased_one(self):
        bought = ListItem.objects.get(id=self.post_milk(2).json()["id"])
        bought.purchased = True
        bought.save()
        self.post_milk(1)

        body = self.client.get(
            f"/api/shoppinglistfull/{self.shoppinglist.id}"
        ).json()

        unpurchased = [
            li for aisle in body["aisles"] for li in aisle["listitems"]
        ]
        purchased = [
            li for aisle in body["purchased_aisles"] for li in aisle["listitems"]
        ]
        self.assertEqual([li["qty"] for li in unpurchased], [1])
        self.assertEqual([li["qty"] for li in purchased], [2])

    def purchase(self, listitem, purchased=True, purch_date=None):
        return self.client.put(
            f"/api/listitems/{listitem.id}",
            {
                "qty": listitem.qty,
                "purchased": purchased,
                "notes": listitem.notes,
                "purch_date": purch_date.isoformat() if purch_date else None,
                "item_id": self.milk.id,
                "aisle_id": self.aisle.id,
                "shopping_list_id": self.shoppinglist.id,
            },
            content_type="application/json",
        )

    def test_buying_the_split_row_folds_it_back_into_the_bought_one(self):
        bought = ListItem.objects.get(id=self.post_milk(1).json()["id"])
        bought.purchased = True
        bought.save()
        extra = ListItem.objects.get(id=self.post_milk(2).json()["id"])

        self.purchase(extra)

        rows = self.milk_rows()
        self.assertEqual(rows.count(), 1, "the cart shows Milk once, not twice")
        self.assertEqual(rows[0].id, bought.id)
        self.assertEqual(rows[0].qty, 3)
        self.assertTrue(rows[0].purchased)

    def test_unbuying_folds_into_an_outstanding_row_the_same_way(self):
        bought = ListItem.objects.get(id=self.post_milk(2).json()["id"])
        bought.purchased = True
        bought.save()
        outstanding = ListItem.objects.get(id=self.post_milk(1).json()["id"])

        self.purchase(bought, purchased=False)

        rows = self.milk_rows()
        self.assertEqual(rows.count(), 1)
        self.assertEqual(rows[0].id, outstanding.id)
        self.assertEqual(rows[0].qty, 3)
        self.assertFalse(rows[0].purchased)

    def test_merging_keeps_the_later_purchase_date(self):
        bought = ListItem.objects.get(id=self.post_milk(1).json()["id"])
        bought.purchased = True
        bought.purch_date = date(2026, 1, 1)
        bought.save()
        extra = ListItem.objects.get(id=self.post_milk(1).json()["id"])

        self.purchase(extra, purch_date=date(2026, 3, 5))

        rows = self.milk_rows()
        self.assertEqual(rows.count(), 1)
        self.assertEqual(rows[0].purch_date, date(2026, 3, 5))

    def test_editing_an_ordinary_row_does_not_merge_anything(self):
        only = ListItem.objects.get(id=self.post_milk(2).json()["id"])

        response = self.purchase(only, purchased=False)
        self.assertEqual(response.status_code, 200)

        rows = self.milk_rows()
        self.assertEqual(rows.count(), 1)
        self.assertEqual(rows[0].id, only.id)
        self.assertEqual(rows[0].qty, 2)

    def test_a_different_item_is_never_folded_in(self):
        eggs = Item.objects.create(name="Eggs")
        milk = ListItem.objects.get(id=self.post_milk(1).json()["id"])
        ListItem.objects.create(
            item=eggs,
            aisle=self.aisle,
            shopping_list=self.shoppinglist,
            qty=1,
            purchased=False,
        )

        self.purchase(milk, purchased=False)

        self.assertEqual(
            ListItem.objects.filter(shopping_list=self.shoppinglist).count(), 2
        )
