from django.shortcuts import render

from .models import AuctionChunk, AuctionId, Realm

def index(request):
    item_id = 152507
    auc_data = {}

    realms = [x[0] for x in Realm.objects.values_list('name')]
    for realm in realms:    
        auc_data[realm] = AuctionChunk.objects.filter(realm=realm, item_id=item_id).values_list('quantity', 'price')

    context = {
        'auc_data': auc_data,
    }

    return render(request, 'main/index.html', context=context)
