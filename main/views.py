from django.shortcuts import render, get_object_or_404

from .models import AuctionChunk, AuctionId, Realm, ItemCategory, Item

import json


def auctions(request):
    item_category = 1
    # get list of (item_id, name) tuples
    item_list = Item.objects.filter(category_id=item_category).values_list('item_id', 'name').order_by('position')
    realms = [x[0] for x in Realm.objects.values_list('name').order_by('position')]

    data = {}
    for item in item_list:
        item_id = item[0]
        data[item_id] = {}
        realm_lists = {}
        realm_lists['position'] = realms
        data[item_id]['realm_order_lists'] = realm_lists

        # create MeanPrice ordered realm list
        temp_list = [(x, AuctionChunk.sorting.mean_price(realm=x, item_id=item_id)) for x in realms]
        temp_list.sort(key=lambda x: x[1], reverse=True)
        realm_lists['mean_price'] = [x[0] for x in temp_list]

        # Fetch item data from model
        default_realm_list = realm_lists['mean_price']
        item_data = {}
        data[item_id]['item_data'] = item_data
        for realm in default_realm_list:
            auctions = AuctionChunk.objects.filter(realm=realm, item_id=item_id).values_list('quantity', 'price', 'owner')
            code = Realm.objects.filter(name=realm).values_list('code')
            seller = '-'.join([Realm.objects.get(name=realm).seller, realm.replace(' ', '')])

            item_data[realm] = (list(auctions), code[0][0], seller)

    # Just the realm Orders for sorting with JS 
    realm_order = {}
    for item_id in data.keys():
        realm_order[item_id] = data[item_id]['realm_order_lists']

    context = {
        'item_list': item_list,
        'data': data,
        'realm_order': realm_order,
    }

    return render(request, 'main/auctions.html', context=context)

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
