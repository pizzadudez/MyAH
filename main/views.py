from django.shortcuts import render, get_object_or_404

from .models import AuctionChunk, AuctionId, Realm, Item, RealmOrder

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
    if request.method == "POST":
        realm_order = request.POST.getlist('order[]')
        for order, realm_name in enumerate(realm_order):
            realm = RealmOrder.objects.filter(realm_name=realm_name).first()
            if realm:
                realm.order = order
            else:
                realm = RealmOrder(realm_name=realm_name, order=order)
            realm.save()
    
    #TODO sort out fetching realms from Realm model if RealmOrder model doesnt have a realm
            



    realms = [x[0] for x in Realm.objects.values_list('name')]

    context = {
        'realms': realms,
    }

    return render(request, 'main/settings.html', context=context)
