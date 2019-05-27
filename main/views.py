from django.shortcuts import render

from .models import AuctionChunk, AuctionId, Realm

def index(request):
    item_id = 152505
    auc_data = {}

    realms = [x[0] for x in Realm.objects.values_list('name')]
    for realm in realms:    
        auctions = AuctionChunk.objects.filter(realm=realm, item_id=item_id).values_list('quantity', 'price')
        code = Realm.objects.filter(name=realm).values_list('code')
        auc_data[realm] = (auctions, code[0][0])

    context = {
        'auc_data': auc_data,
    }

    return render(request, 'main/index.html', context=context)
