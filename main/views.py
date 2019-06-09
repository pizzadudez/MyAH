from django.shortcuts import render, get_object_or_404

from .models import AuctionChunk, AuctionId, Realm, ItemCategory, Item

import json

def index(request):
    item_category = 1
    items = Item.objects.filter(category_id=item_category).values_list('item_id', 'name').order_by('position')
    realms = [x[0] for x in Realm.objects.values_list('name').order_by('position')]

    data = {}
    for item in items:
        item_id = item[0]
        data[item_id] = {}
        for realm in realms:    
            auctions = AuctionChunk.objects.filter(realm=realm, item_id=item_id).values_list('quantity', 'price', 'owner')
            code = Realm.objects.filter(name=realm).values_list('code')
            seller = '-'.join([Realm.objects.get(name=realm).seller, realm.replace(' ', '')])

            data[item_id][realm] = (auctions, code[0][0], seller)

    context = {
        'data': data,
        'items': items,
    }

    return render(request, 'main/index.html', context=context)

def settings(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        for position, realm_name in enumerate(json_data['realmOrder']):
            realm = Realm.objects.get(name=realm_name)
            realm.position = position
            realm.save()
        for position, category in enumerate(json_data['itemOrder']):
            item_category = ItemCategory.objects.get(name=category['name'])
            item_category.position = position
            item_category.save()
            for position, item_name in enumerate(category['items']):
                item = Item.objects.get(name=item_name)
                item.position = position
                item.save()

   
    # Realm names sorted by position field
    realms = [x[0] for x in Realm.objects.values_list('name').order_by('position')]
    # Items by category
    item_categories = [x[0] for x in ItemCategory.objects.values_list('name').order_by('position')]
    items = {}
    for category in item_categories:
        item_list = Item.objects.filter(category__name=category).order_by('position')
        if len(item_list):
            items[category] = item_list
            
    context = {
        'realms': realms,
        'items': items,
    }

    return render(request, 'main/settings.html', context=context)
