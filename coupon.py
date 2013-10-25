# Coupons in October 2013
import datetime
from twiceweb.common import models
from twiceweb.analytics.query_utils import query_dates as qd

coupons = models.Coupon.objects(created_dt__gte=qd.Date("2013-10-14").to_utc(),
                                internal_description="_new_arrivals").order_by("created_dt")

print coupons.count()

curr_date = coupons[0].created_dt.date()
num_coupons = 0.0
enabling_items = 0.0

for c in coupons:
    if c.created_dt.date() <= curr_date:
        num_coupons += 1
        enabling_items += len(c.payoff.enabling_item_properties["disp_id__in"])
    else:
        print curr_date
        print "Number of Coupons:  %s" % num_coupons
        print "Number of Items:  %s\n" % enabling_items
        num_coupons = 1
        enabling_items = len(c.payoff.enabling_item_properties["disp_id__in"])
        curr_date = c.created_dt.date()

print curr_date
print "Number of Coupons:  %s" % num_coupons
print "Number of Items:  %s\n" % enabling_items
print "Number of Items/Coupon: %0.2f" % (enabling_items/num_coupons)
