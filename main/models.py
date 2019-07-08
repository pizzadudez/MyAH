from django.db import models
from django.db.models import Sum, F


class SortManager(models.Manager):
    def mean_price(self, realm, item_id):
        """Returns mean min price for this (realm, item_id)."""

        all_chunks = super().get_queryset().filter(realm=realm, item_id=item_id)
        if len(all_chunks) == 0:
            return 999999 # no auctions so put this realm on top

        total_quantity = all_chunks.aggregate(Sum('quantity'))['quantity__sum']
        percentage = 0.4 # CHANGEME
        max_quantity = total_quantity * percentage
        curr_quantity = 0
        mean_numerator = 0

        for chunk in all_chunks:
            if curr_quantity + chunk.quantity <= max_quantity or curr_quantity == 0:
                mean_numerator += chunk.quantity * chunk.price
            else:
                break  
            curr_quantity += chunk.quantity

        return mean_numerator / curr_quantity

    def my_price_and_undercut_count(self, realm, item_id):
        """Returns price of lowest AuctionChunk owned by Realm's seller and also
        how many auctions are posted for less (undercut). Returns None if no
        auctions are posted by the seller.
        """

        seller = Realm.objects.get(name=realm).seller
        full_name = f"{seller}-{realm.replace(' ', '')}"
        query = super().get_queryset().filter(realm=realm, item_id=item_id, owner=full_name).values_list('price')
        # No chunk posted by seller
        if len(query) < 1:
            return None, None
        # Sort price_list and return lowest
        price_list = [x[0] for x in list(query)]
        price_list.sort()
        my_price = price_list[0]

        # Count how many auctions are posted for less than my_price
        query = super().get_queryset().filter(realm=realm, item_id=item_id, price__lt=my_price)
        undercut_count = query.aggregate(Sum('quantity'))['quantity__sum'] or 0

        return my_price, undercut_count


class AuctionChunk(models.Model):
    chunk_id = models.AutoField(primary_key=True)
    realm = models.TextField(blank=True, null=True)
    item_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    stack_size = models.IntegerField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    time_left = models.TextField(blank=True, null=True)

    objects = models.Manager()
    sort_values = SortManager()

    def __str__(self):
        return str(self.price)

    class Meta:
        managed = False
        db_table = 'auction_chunks'


class AuctionId(models.Model):
    auc_id = models.IntegerField(blank=True, null=True)
    chunk = models.ForeignKey(AuctionChunk, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auction_ids'


class Realm(models.Model):
    name = models.TextField(primary_key=True, unique=True)
    slug = models.TextField(unique=True)
    code = models.TextField(unique=True)
    update_interval = models.IntegerField(blank=True, null=True)
    last_update = models.IntegerField(blank=True, null=True)
    #last_check = models.IntegerField(blank=True, null=True)
    json_link = models.TextField(blank=True, null=True)

    seller = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)
    position = models.IntegerField(blank=False, null=False, default=0)
    account = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'realms'


class ItemCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    position = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'item_categories'


class Item(models.Model):
    item_id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    short_name = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ItemCategory, models.DO_NOTHING, blank=True, null=True)
    position = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'items'


class StackSize(models.Model):
    row_id = models.AutoField(primary_key=True)
    stack_size = models.IntegerField()
    category = models.ForeignKey(ItemCategory, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return str(self.stack_size)

    class Meta:
        db_table = 'stack_sizes'
