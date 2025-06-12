from django.db import models

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
    """

    name = models.CharField(max_length=50, unique=True)
    matches = models.CharField(max_length=254, null=True, blank=True)
    plural = models.CharField(max_length=50, null=True, blank=True)
    aisle = models.ForeignKey(
        Aisle, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )

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
