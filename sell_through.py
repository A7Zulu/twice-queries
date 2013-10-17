print "7-day STR, by store listing"
print
 
# For a given date, find the sell-through on items that were created a week
# before that. In order to avoid day-of-week effects, we look at the averaged
# results over the trailing 7 days, so it's sort of a 10.5-day sell-through
for dr in qd.DateRange("2013-6-16", "2013-6-19").bucketed(days=1):
    window_start = dr.start_dt.offset(days=-7 - 7).to_utc()
    window_end = dr.start_dt.offset(days=-7).to_utc()
 
    md = models.match_dict(
        created_dt__gte=window_start,
        created_dt__lt=window_end
    )
    items = models.Item.objects(store_listings__match=md)
    num_created = items.count()
 
    # Ok if they were sold and then returned -- just have to have at least 1
    # store listing ending with a correct reason
    md.update(models.match_dict(
        ending_reason__in=[
            models.StoreListingEndingReason.SOLD,
            models.StoreListingEndingReason.SOLD_ELSEWHERE
        ],
        ended_dt__lt=dr.start_dt.to_utc()
    ))
    sold_items = models.Item.objects(store_listings__match=md)
    num_sold = sold_items.count()
 
    print "%s\t%s\t%s" % (
        dr.start_dt.short_format(),
        num_created,
        num_sold
    )
