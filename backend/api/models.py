from django.db import models

# Create your models here.


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError("There is already one instance of this model")
        return super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("You cannot delete this object")


class Store(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Aisle(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField(default=1)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.store.name} | {self.name}"


class Item(models.Model):
    name = models.CharField(max_length=50, unique=True)
    matches = models.CharField(max_length=254, null=True, blank=True)
    plural = models.CharField(max_length=50, null=True, blank=True)
    aisle = models.ForeignKey(
        Aisle, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    name = models.CharField(max_length=50)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.store.name} | {self.name}"


class ListItem(models.Model):
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
        return self.item.name


class Version(SingletonModel):
    """
    Model representing app version.

    Fields:
    - version_number (CharField): The current version of the app.
    """

    version_number = models.CharField(max_length=10)

    def __str__(self):
        return self.version_number
