from django.shortcuts import render

from .models import AuctionChunk, AuctionId, Realm, Item

def index(request):
    item_category = 1
    items = Item.objects.filter(category_id=item_category).values_list('item_id', 'name')
    realms = [x[0] for x in Realm.objects.values_list('name')]

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
    realms = [x[0] for x in Realm.objects.values_list('name')]

    context = {
        'realms': realms,
    }

    return render(request, 'main/settings.html', context=context)
