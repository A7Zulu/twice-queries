# Python Queries for Finncial Model
import pytz
import datetime

from celery import current_app as celery

from twiceweb.common import models
from twiceweb.analytics.query_utils import query_dates as qd
from mongoengine import Q



# Calculates # of distinct shoppers in last 12 months
total_orders = (
    models.PurchaseOrder
    .objects(type=models.PurchaseOrderType.STORE, 
             status=models.PurchaseOrderStatus.SHIPPED,
             created_dt__gte=qd.Date("2013-10-01").to_utc())
    .exclude("purchase_order_items.item_snapshot").distinct("user"))

print total_orders.count()

# customer_list = [total_orders[c].user for c in range(total_orders.count())]
# print len(customer_list)

# customer_set = set(customer_list)
# print len(customer_set)


