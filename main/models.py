from django.db import models

class AuctionChunk(models.Model):
    chunk_id = models.AutoField(primary_key=True)
    realm = models.TextField(blank=True, null=True)
    item_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    stack_size = models.IntegerField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    time_left = models.TextField(blank=True, null=True)

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
    name = models.TextField(unique=True, primary_key=True)
    slug = models.TextField(unique=True)
    code = models.TextField(unique=True)
    region = models.TextField()
    seller = models.TextField(blank=True, null=True)
    update_interval = models.IntegerField(blank=True, null=True)
    last_update = models.IntegerField(blank=True, null=True)
    json_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'realms'


class ItemCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'item_categories'


class Item(models.Model):
    item_id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    short_name = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ItemCategory, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items'


class StackSize(models.Model):
    stack_size = models.IntegerField()
    category = models.ForeignKey(ItemCategory, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stack_sizes'


class RealmOrder(models.Model):
    realm_name = models.TextField(primary_key=True)
    order = models.IntegerField(blank=True, null=True)
    account = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'realm_order'
