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



