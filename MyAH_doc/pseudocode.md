# Settings Page
- [x] Refactor JS
- [x] add itemCategory sorting (togheter with item or sepparate)
- [x] Sort out the serialization
- [x] Handle POST request to change model data

# Ideas

## Seller auctions
- Every time we get an update to a realm we call it a snapshot
- We store seller snapshots somehow
- When we detect that the seller posted new items between last snapshot and current one we store that snapshot and it's posted items somewhere
- each snapshot after that we check what has been sold from the "items posted" and store these changes somewhere (probably local to the snapshot that has the changes)

### What do we do when we repost?
- the auc_ids from the last initial post snapshot are probably gone and the new items posted/reposted have new ones
- should we treat these collection of snapshots after posting and before expiring/reposting as chunks?
- what if these snapshot chunks intersect sometimes (2nd Posting for today)

## Auctions Overview
- Cluster simillar priced auctions togheter
- each cluster will be rendered as (avg price + stackcount) and also as each chunk individually
- clicking a button will display either clusters or chunks
- another option might be to cluster only over a set amount of chunks or price

# AvgMinPrice
- Q: should this be calculated on the spot in django's backend or in api_data?
  - A: seems like it can be done with aggregate() on a queryset
  - auc.aggregate(amp=ExpressionWrapper(Sum(F('price') * F('quantity')) / Sum(F('quantity')), output_field=FloatField()))
- How is this calculated?
  - weighted average price of first x% of auctions
  - x% depends on server and maybe some hardcoded numbers, TBD
- How do I get the auctionChunks that are in the first x% of auctions?
    ```
    get queryset
    get max_quant
    loop thru the queryset
        q_so_far += q
        if q_so_far > max_quant
            break
    ```

## Thinktank
```
data = {
    [item_id] = {
        'realm_order_lists' = {
            'position' = [],
            'mean_price' = [],
            'my_price' = [],
            'undercut_qty' = []
        },
        'item_data' = {
            [realm] = {

            }
        }
    }
}
```


