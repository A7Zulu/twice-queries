import collections
import mongoengine

from twiceweb.common import models
from twiceweb.analytics.query_utils import query_dates as qd


# For a given date, find the sell-through on items that were created a week
# before that. In order to avoid day-of-week effects, we look at the averaged
# results over the trailing 7 days, so it's sort of a 10.5-day sell-through

days = 60
sell_through = [0] * days
start_date = "2013-07-01"
end_date = "2013-08-09"
dr = qd.DateRange(start_date, end_date).total_days()

print "Blended cohort sell-through rates from %s to %s" % (start_date, end_date)

for date in qd.DateRange(start_date, end_date).bucketed(days=1):

    window_start = date.start_dt.offset(days=0).to_utc()
    window_end = date.start_dt.offset(days=1).to_utc()

    md = models.match_dict(
        created_dt__gte=window_start,
        created_dt__lt=window_end
    )
    items = models.Item.objects(store_listings__match=md)
    num_created = items.count()
    
    for i in range(days):
     
        # Ok if they were sold and then returned -- just have to have at least 1
        # store listing ending with a correct reason
        md.update(models.match_dict(
            ending_reason__in=[
                models.StoreListingEndingReason.SOLD,
                models.StoreListingEndingReason.SOLD_ELSEWHERE
            ],
            ended_dt__lt=date.start_dt.offset(days=i+1).to_utc()
        ))
        sold_items = models.Item.objects(store_listings__match=md)
        num_sold = sold_items.count()
        pct_sold = float(num_sold)/float(num_created)

        sell_through[i] += pct_sold/dr
    

for i in range(days):
    print "Day %s:  %0.2f" % (i+1, sell_through[i])
