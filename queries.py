# Python Queries for Finncial Model
import pytz
import datetime

from celery import current_app as celery

from twiceweb.common import models
from twiceweb.analytics.query_utils import query_dates as qd
from mongoengine import Q


"""
Average Items Purchases / Customer / Order
"""
def average_items_purchased():
    total_orders = (
        models.PurchaseOrder
        .objects(type=models.PurchaseOrderType.STORE, 
                 status=models.PurchaseOrderStatus.SHIPPED,
                 created_dt__gte=qd.Date("2013-01-01").to_utc())
        .exclude("purchase_order_items.item_snapshot"))

    print "Total Orders:  %s" % total_orders.count()

    total_items_purchased = sum(models.pluck(total_orders, "get_num_items"))

    print "Total Items Purchased:  %s" % total_items_purchased

    print "Items Purchased / Order:  %0.2f" % (float(total_items_purchased)/float(total_orders.count()))

"""
Calculates the total revenues and revenue/item for a given date range
"""
def revenue_item():
    total_items_purchased = 0.0
    revenues = 0.0

    total_orders = (
        models.PurchaseOrder
        .objects(type=models.PurchaseOrderType.STORE, 
                 status=models.PurchaseOrderStatus.SHIPPED,
                 created_dt__gte=qd.Date("2013-10-01").to_utc())
        .exclude("purchase_order_items.item_snapshot"))

    total_items_purchased = sum(models.pluck(total_orders, "get_num_items"))

    print "Total Items Purchased:  %s" % total_items_purchased
    
    revenues = sum(models.pluck(total_orders, "get_revenue"))

    print "Total Revenues:  %s" % revenues
    print "Revenue / Item:  %0.2f" % (revenues/total_items_purchased)

"""
Counts the number of inventory items that are listed at a given time
"""
def inventory_count():
    start_date = "2013-09-01"
    end_date = "2013-09-30"

    for date in qd.DateRange(start_date, end_date).bucketed(days=1):
        md1 = models.match_dict(created_dt__lte=date.start_dt.to_utc(), ended_dt=None)
        md2 = models.match_dict(created_dt__lte=date.start_dt.to_utc(), ended_dt__gte=date.start_dt.to_utc())
        inventory = models.Item.objects(Q(store_listings__match=md1) | Q(store_listings__match=md2))
        
        print "%s:  %s" % (date.start_dt.short_format(), inventory.count())

"""
Calculates the number of customers that have purchased once in the last year
"""
def active_customers():
    total_orders = (
        models.PurchaseOrder
        .objects(type=models.PurchaseOrderType.STORE, 
                 status=models.PurchaseOrderStatus.SHIPPED,
                 created_dt__gte=qd.Date("2012-10-01").to_utc())
        .exclude("purchase_order_items.item_snapshot"))
   
    print total_orders.count()

    customer_list = [total_orders[c].user for c in range(total_orders.count())]
    print len(customer_list)
    
    customer_set = set(customer_list)
    print len(customer_set)


def main():
    #return average_items_purchased()
    #revenue_item()
    #inventory_count()
    active_customers()

if __name__ == "__main__":
    main()

