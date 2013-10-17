import datetime
from collections import defaultdict

import numpy
from mongoengine import Q

from twiceweb.analytics.query_utils import query_dates as qd
from twiceweb.common import models

start_dt = qd.Date("2012-3-1")

total_revenue = 0
total_revenue_from_repeat = 0

cohort_shoppers_by_month = {}
cohort_purchases_by_month = {}
cohort_revenue_by_month = {}

for i in xrange(0, 19):
    dt = start_dt.offset(months=i)
    cohort_shoppers_by_month[dt.short_format()] = defaultdict(set)
    cohort_purchases_by_month[dt.short_format()] = defaultdict(int)
    cohort_revenue_by_month[dt.short_format()] = defaultdict(int)

while True:
    end_dt = start_dt.offset(months=1)
    if end_dt.to_utc() > datetime.datetime.utcnow():
        break

    purchases = models.PurchaseOrder.objects(
        type="store",
        created_dt__gte=start_dt.to_utc(),
        created_dt__lt=end_dt.to_utc())

    purchasing_users = purchases.distinct("user")

    for user in purchasing_users:
        user_purchases = (
            models.PurchaseOrder
            .objects(user=user,
                     type="store")
            .order_by("created_dt"))
        first_purchase = user_purchases.first()
        if first_purchase.created_dt < start_dt.to_utc():
            continue

        for purchase in user_purchases:
            purchase_month = qd.Date(purchase.created_dt).floor("month")
            cohort_shoppers_by_month[start_dt.short_format()][purchase_month.short_format()].add(user.disp_id)
            cohort_purchases_by_month[start_dt.short_format()][purchase_month.short_format()] += 1
            cohort_revenue_by_month[start_dt.short_format()][purchase_month.short_format()] += purchase.get_revenue()

            total_revenue += purchase.get_revenue()

            if purchase != first_purchase:
                total_revenue_from_repeat += purchase.get_revenue()

    start_dt = end_dt

print "Cohort shoppers by month"
print "------------------------"
for cohort_month, d in cohort_shoppers_by_month.iteritems():
    revenue_months = cohort_shoppers_by_month.keys()
    print "\t".join(
        [cohort_month] + [str(len(d[month])) for month in revenue_months])
print
print "Cohort purchases by month"
print "------------------------"
for cohort_month, d in cohort_purchases_by_month.iteritems():
    revenue_months = cohort_purchases_by_month.keys()
    print "\t".join(
        [cohort_month] + [str(d[month]) for month in revenue_months])
print
print "Cohort revenue by month"
print "------------------------"
for cohort_month, d in cohort_revenue_by_month.iteritems():
    revenue_months = cohort_revenue_by_month.keys()
    print "\t".join(
        [cohort_month] + [str(d[month]) for month in revenue_months])
print
print "Purchase repetition"
print "-----------------------"
print "Total revenue\t%s" % total_revenue
print "Total revenue from repeat\t%s" % total_revenue_from_repeat
