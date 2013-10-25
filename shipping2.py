# Python Queries for Shipping Appendix Slide
import pytz
import datetime


from twiceweb.common import models
from twiceweb.analytics.query_utils import query_dates as qd


start_date = "2013-09-01"
end_date = "2013-10-01"
start_date2 = "2013-08-01"
end_date2 = "2013-09-01"


# Sell Order Kit Requests
sell_order_requests = (
    models.SellOrder
    .objects(created_dt__gte=qd.Date(start_date).to_utc(),
             created_dt__lt=qd.Date(end_date).to_utc()))

print "Sell order kits out:  %s" % sell_order_requests.count()


# Sell Order Received
sell_orders_received = (
    models.SellOrder
    .objects(evaluation_completed_dt__gte=qd.Date(start_date).to_utc(),
             evaluation_completed_dt__lt=qd.Date(end_date).to_utc()))

print "Sell orders received:  %s" % sell_orders_received.count()


# Sell Order Returned
sell_orders_returned = (
    models.SellOrder
    .objects(evaluation_completed_dt__gte=qd.Date(start_date).to_utc(),
             evaluation_completed_dt__lt=qd.Date(end_date).to_utc(),
             exit_outcome=models.SellOrderExitOutcome.RETURNED))

print "Sell orders returned:  %s" % sell_orders_returned.count()

shipping_costs = 0
for returns in sell_orders_returned:
    parcels = returns.sell_order_return.parcels
    for p in parcels:
        shipping_costs+= p.total_parcel_shipping_cost

print "Sell orders returned costs:  $%0.2f" % (shipping_costs/100.0)


# Purchase Orders
total_orders = (
    models.PurchaseOrder
    .objects(status=models.PurchaseOrderStatus.SHIPPED,
             created_dt__gte=qd.Date(start_date2).to_utc(),
             created_dt__lt=qd.Date(end_date2).to_utc())
    .exclude("purchase_order_items.item_snapshot"))

print "Purchase orders out:  %s" % total_orders.count()

shipping_costs = 0
for order in total_orders:
    parcels = order.parcels
    for p in parcels:
        if p.total_parcel_shipping_cost != None:
            shipping_costs += p.total_parcel_shipping_cost

print "Purchase orders shipping costs:  $%0.2f" % (shipping_costs/100.0)


# Purchase Order Returns
returned_orders = (
    models.PurchaseOrder
    .objects(returns__status=models.PurchaseOrderReturnStatus.REFUNDED,
             created_dt__gte=qd.Date(start_date2).to_utc(),
             created_dt__lt=qd.Date(end_date2).to_utc())
    .exclude("purchase_order_items.item_snapshot"))

print "Purchase orders returned:  %s" % returned_orders.count()




