class MainRouter(object):
    """
    This routes assigns which external_db each model in the main
    app should read data from.
    """

    def db_for_read(self, model, **hints):
        if model._meta.label in ('main.AuctionChunk', 'main.AuctionId'):
            return 'auctions'
        elif model._meta.label == 'main.Realm':
            return 'realms'
        elif model._meta.label in ('main.ItemCategory', 'main.Item', 'main.StackSize'):
            return 'items'
        elif model._meta.label == 'main.HopRealm':
            return 'hop_realms'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.label == 'main.Realm':
            return 'realms'
        if model._meta.label in ('main.ItemCategory', 'main.Item', 'main.StackSize'):
            return 'items'
        elif model._meta.label == 'main.HopRealm':
            return 'hop_realms'
        return None