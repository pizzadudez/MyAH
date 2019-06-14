from django.shortcuts import render, get_object_or_404

from .models import AuctionChunk, AuctionId, Realm, ItemCategory, Item

import json


def auctions(request):
    item_category = 1
    # get list of (item_id, name) tuples
    item_list = Item.objects.filter(category_id=item_category).values_list('item_id', 'name').order_by('position')
    realms = [x[0] for x in Realm.objects.values_list('name').order_by('position')]

    auc_data = {}
    realm_order = {}
    for item in item_list:
        item_id = item[0]
        auc_data[item_id] = {}
        realm_order[item_id] = {}
        realm_order[item_id]['position'] = realms # order based on realm positions in Realm model

        # create MeanPrice ordered realm list
        temp_list = [(x, AuctionChunk.sort_values.mean_price(realm=x, item_id=item_id)) for x in realms]
        temp_list.sort(key=lambda x: x[1], reverse=True)
        mean_list = [x[0] for x in temp_list]
        realm_order[item_id]['mean_price'] = mean_list

        # create realm orders where seller's auction appear first and ordered by price/undercut_count
        temp_list = []
        mean_list_rest = []
        for realm in mean_list:
            my_price, undercut_count = AuctionChunk.sort_values.my_price_and_undercut_count(realm, item_id)
            if my_price:
                temp_list.append((realm, my_price, undercut_count))
            else:
                mean_list_rest.append(realm)
        temp_list.sort(key=lambda x: x[1], reverse=True)
        realm_order[item_id]['my_price'] = [x[0] for x in temp_list] + mean_list_rest
        temp_list.sort(key=lambda x: x[2], reverse=True)
        realm_order[item_id]['undercut_count'] = [x[0] for x in temp_list] + mean_list_rest
            

        # Fetch item data from model
        default_realm_order = realm_order[item_id]['mean_price']
        for realm in default_realm_order:
            auctions = AuctionChunk.objects.filter(realm=realm, item_id=item_id).values_list('quantity', 'price', 'owner')
            code = Realm.objects.filter(name=realm).values_list('code')
            seller = '-'.join([Realm.objects.get(name=realm).seller, realm.replace(' ', '')])

            auc_data[item_id][realm] = (list(auctions), code[0][0], seller)

    context = {
        'item_list': item_list,
        'auc_data': auc_data,
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
