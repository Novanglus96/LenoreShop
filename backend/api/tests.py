from datetime import date, timedelta

from django.db.utils import IntegrityError
from django.test import TestCase

from backend.api import LIST_PREVIEW_ITEM_COUNT

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
