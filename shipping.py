# Python Queries for Shipping Appendix Slide
import pytz
import datetime


from twiceweb.common import models
from twiceweb.analytics.query_utils import query_dates as qd



# Average Items Purchases / Customer / Order
def sell_order_kits_out(start_date, end_date):
    sell_order_requests = (
        models.SellOrder
        .objects(created_dt__gte=qd.Date(start_date).to_utc(),
                 created_dt__lt=qd.Date(end_date).to_utc()))

    print "Sell order kits out:  %s" % sell_order_requests.count()

def sell_orders_received(start_date, end_date):
    sell_orders_received = (
        models.SellOrder
        .objects(created_dt__gte=qd.Date(start_date).to_utc(),
                 created_dt__lt=qd.Date(end_date).to_utc(),
                 offer_outcome__ne=models.SellOrderOfferOutcome.EXPIRED))

    print "Sell orders received:  %s" % sell_orders_received.count()


def sell_orders_returned(start_date, end_date):
    sell_orders_returned = (
        models.SellOrder
        .objects(created_dt__gte=qd.Date(start_date).to_utc(),
                 created_dt__lt=qd.Date(end_date).to_utc(),
                 exit_outcome=models.SellOrderExitOutcome.RETURNED))

    print "Sell orders returned:  %s" % sell_orders_returned.count()
    
    shipping_costs = 0
    for returns in sell_orders_returned:
        parcels = returns.sell_order_return.parcels
        for p in parcels:
            shipping_costs+= p.total_parcel_shipping_cost

    print "Sell orders returned costs:  $%0.2f" % (shipping_costs/100.0)



def purchase_orders_out(start_date, end_date):
    total_orders = (
        models.PurchaseOrder
        .objects(status=models.PurchaseOrderStatus.SHIPPED,
                 created_dt__gte=qd.Date(start_date).to_utc(),
                 created_dt__lt=qd.Date(end_date).to_utc())
        .exclude("purchase_order_items.item_snapshot"))

    print "Purchase orders out:  %s" % total_orders.count()

    shipping_costs = 0
    for order in total_orders:
        parcels = order.parcels
        for p in parcels:
            if p.total_parcel_shipping_cost != None:
                shipping_costs += p.total_parcel_shipping_cost

    print "Purchase orders shipping costs:  $%0.2f" % (shipping_costs/100.0)


def purchase_orders_returned(start_date, end_date):
    returned_orders = (
        models.PurchaseOrder
        .objects(returns__status=models.PurchaseOrderReturnStatus.REFUNDED,
                 created_dt__gte=qd.Date(start_date).to_utc(),
                 created_dt__lt=qd.Date(end_date).to_utc())
        .exclude("purchase_order_items.item_snapshot"))

    print "Purchase orders returned:  %s" % returned_orders.count()
    
    #shipping_costs = 0.
    #for returns in returned_orders:
        #    for r in returns.returns:
            #        cost = r.parcel.total_parcel_shipping_cost
            #if cost != None:
                #    shipping_costs += cost

    #print "Purchase orders returned costs:  $%0.2f" % shipping_costs


def main():
    start_date = "2013-09-01"
    end_date = "2013-10-01"
    sell_order_kits_out(start_date, end_date)
    sell_orders_received(start_date, end_date)
    sell_orders_returned(start_date, end_date)
    purchase_orders_out(start_date, end_date)
    purchase_orders_returned(start_date, end_date)


if __name__ == "__main__":
    main()
    
