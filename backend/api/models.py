from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from api.images import delete_renditions

# Create your models here.


class SingletonModel(models.Model):
    """
    Model representing a singleton model.

    Attributes:
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Override save method to validate only one instance exists.
        """
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError("There is already one instance of this model")
        return super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete method to block deletes.
        """
        raise ValidationError("You cannot delete this object")


class Store(models.Model):
    """
    Model representing a Store.

    Attributes:
        name (CharField): The name of a store. Required. Unique.
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        Returns:
            (String): The Store Object name.
        """
        return self.name


class Aisle(models.Model):
    """
    Model representing an aisle in a store.

    Attributes:
        name (CharField): The name of the Aisle.
        order (IntegerField): The order of appearance for Aisle.
        store (Store): An object respresenting a store.
    """

    name = models.CharField(max_length=50)
    order = models.IntegerField(default=1)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns:
            (String): The Aisle Object name.
        """
        return f"{self.store.name} | {self.name}"


class Item(models.Model):
    """
    Model representing an item.

    Attributes:
        name (CharField): The name of the Item. Unique.
        matches (CharField): Alternate spelling that matches.
        plural (CharField): Plural spelling of item name.
        aisle (Aisle): An object representing an aisle.
        image (ImageField): A photo of the item, for telling it apart from
            similar products on a shelf. Optional.
        thumbnail (ImageField): The downscaled rendition shown on list rows.
            Written by the upload endpoint alongside `image`; never set on its
            own.
    """

    name = models.CharField(max_length=50, unique=True)
    matches = models.CharField(max_length=254, null=True, blank=True)
    plural = models.CharField(max_length=50, null=True, blank=True)
    aisle = models.ForeignKey(
        Aisle, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    image = models.ImageField(upload_to="items/", null=True, blank=True)
    thumbnail = models.ImageField(upload_to="items/thumbs/", null=True, blank=True)

    def __str__(self):
        """
        Returns:
            (String): The Item Object name.
        """
        return self.name


class ShoppingList(models.Model):
    """
    Model representing a ShopingList object.

    Attributes:
        name (CharField): The name of the shopping list.
        store (Store): An object representing a store.
    """

    name = models.CharField(max_length=50)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns:
            (String): The ShoppingList Object name.
        """
        return f"{self.store.name} | {self.name}"


class ListItem(models.Model):
    """
    Model representing a ListItem object.

    Attributes:
        qty (IntegerField): The numder of items for this list item.
        purchased (BooleanField): Wether this list item has been purchased.
        notes (TextField): Notes associated with this list item.
        purch_date(DateFild): The date this list item was purchased.
        item (Item): An object representing an Item.
        aisle (Aisle): An object representing an Aisle.
        shopping_list (ShoppingList): An object representing a ShoppingList.

    """

    qty = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    purch_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    aisle = models.ForeignKey(Aisle, on_delete=models.CASCADE, null=True)
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns:
            (String): The ListItem Object name.
        """
        return self.item.name


class Freezer(models.Model):
    """
    Model representing a Freezer.

    Attributes:
        name (CharField): The name of the freezer. Required. Unique.
        location (CharField): Where the freezer is, eg. "Garage". Optional.
    """

    name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        """
        Returns:
            (String): The Freezer Object name.
        """
        return self.name


class FreezerItem(models.Model):
    """
    Model representing a frozen food stored in a Freezer.

    Unlike ListItem, this does not reference the Item catalog. Freezer
    contents are often one-off leftovers ("chili, Nov 3") that would only
    pollute the shopping list catalog if they were forced into it.

    Attributes:
        name (CharField): The name of the frozen food.
        qty (IntegerField): How much is stored. Default = 1.
        unit (CharField): The unit for qty, eg. "lbs", "bags". Optional.
        date_added (DateField): The date this was put in the freezer. Optional,
            since food already in the freezer often has no date on it.
        discard_date (DateField): The date this should be thrown out. Optional.
        notes (TextField): Notes associated with this frozen food.
        freezer (Freezer): An object representing a Freezer.
        image (ImageField): A photo of the frozen food. Optional, and carried
            here rather than on Item because FreezerItem has no Item FK.
        thumbnail (ImageField): The downscaled rendition shown on freezer rows.
            Written by the upload endpoint alongside `image`; never set on its
            own.
    """

    name = models.CharField(max_length=50)
    qty = models.IntegerField(default=1)
    unit = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    discard_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    notes = models.TextField(null=True, blank=True)
    freezer = models.ForeignKey(Freezer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="freezeritems/", null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to="freezeritems/thumbs/", null=True, blank=True
    )

    class Meta:
        ordering = ["freezer", "name"]

    @property
    def days_until_discard(self):
        """
        Returns:
            (int): Days until discard_date, negative once past it. None if no
                discard_date is set.
        """
        if not self.discard_date:
            return None
        return (self.discard_date - date.today()).days

    @property
    def is_expired(self):
        """
        Returns:
            (bool): True if the discard date has passed.
        """
        days = self.days_until_discard
        return days is not None and days < 0

    def __str__(self):
        """
        Returns:
            (String): The FreezerItem Object name.
        """
        return f"{self.freezer.name} | {self.name}"


class Version(SingletonModel):
    """
    Model representing app version.

    Fields:
    - version_number (CharField): The current version of the app.
    """

    version_number = models.CharField(max_length=10)

    def __str__(self):
        """
        Returns:
            (String): The version number.
        """
        return self.version_number


@receiver(post_delete, sender=Item)
@receiver(post_delete, sender=FreezerItem)
def delete_image_files(sender, instance, **kwargs):
    """
    Removes an object's photo files once its row is gone.

    Django deletes the row but never the file behind an ImageField, so without
    this every deleted item leaves its photo on the media volume forever. Hung
    off post_delete rather than the API handler so cascades and admin deletes
    are covered too.

    Args:
        sender (Model): The model class the signal fired for.
        instance (Model): The object that was deleted.
    """
    delete_renditions(instance)
