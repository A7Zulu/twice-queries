import datetime
from collections import defaultdict

import numpy
from mongoengine import Q

from twiceweb.analytics.query_utils import query_dates as qd
from twiceweb.common import models

cutoff_dt = qd.Date("2012-3-1").to_utc()

shoppers = models.PurchaseOrder.objects(
    type="store",
    created_dt__gte=cutoff_dt).distinct("user")

num_multi_purchasers = 0
num_single_purchasers = 0

num_multi_purchaser_referrers = 0
num_single_purchaser_referrers = 0

num_multi_purchaser_successful_referrers = 0
num_single_purchaser_successful_referrers = 0

multi_purchasers_num_invitations_sent = 0
single_purchasers_num_invitations_sent = 0

multi_purchasers_num_invitations_accepted = 0
single_purchasers_num_invitations_accepted = 0

times_to_send_referral = []

num_users_by_cycle = defaultdict(int)
num_referrals_sent_by_cycle = defaultdict(int)
num_referrals_accepted_by_cycle = defaultdict(int)

for user in shoppers:
    num_invitations_sent = len(user.referrals)
    referred = models.User.objects(referred_by=user)
    num_referred = len([referred_user for referred_user
                        in referred if referred_user in shoppers])

    first_purchase = (
        models.PurchaseOrder
        .objects(user=user,
                 type="store")
        .order_by("created_dt")
        .first())

    for referral in user.referrals:
        times_to_send_referral.append((referral.created_dt -
                                       first_purchase.created_dt).total_seconds())

    if models.PurchaseOrder.objects(user=user, type="store").count() > 1:
        num_multi_purchasers += 1
        if num_invitations_sent:
            num_multi_purchaser_referrers += 1
        if num_referred:
            num_multi_purchaser_successful_referrers += 1
        multi_purchasers_num_invitations_sent += num_invitations_sent
        multi_purchasers_num_invitations_accepted += num_referred
    else:
        num_single_purchasers += 1
        if num_invitations_sent:
            num_single_purchaser_referrers += 1
        if num_referred:
            num_single_purchaser_successful_referrers += 1
        single_purchasers_num_invitations_sent += num_invitations_sent
        single_purchasers_num_invitations_accepted += num_referred

    """
    cycle = 0
    cur_user = user
    while True:
        if cycle >= 3:
            break
        if cur_user.referred_by:
            cycle += 1
            cur_user = cur_user.referred_by
        else:
            break
    num_users_by_cycle[cycle] += 1
    num_referrals_sent_by_cycle[cycle] += num_invitations_sent
    num_referrals_accepted_by_cycle[cycle] += num_referred
    """

print "Single purchasers"
print "-----------------"
print "Num users\t%s" % num_single_purchasers
print "Num referrers\t%s" % num_single_purchaser_referrers
print "Num successful referrers\t%s" % num_single_purchaser_successful_referrers
print "Num invited\t%s" % single_purchasers_num_invitations_sent
print "Num referred\t%s" % single_purchasers_num_invitations_accepted
print
print "Multi purchasers"
print "-----------------"
print "Num users\t%s" % num_multi_purchasers
print "Num referrers\t%s" % num_multi_purchaser_referrers
print "Num successful referrers\t%s" % num_multi_purchaser_successful_referrers
print "Num invited\t%s" % multi_purchasers_num_invitations_sent
print "Num referred\t%s" % multi_purchasers_num_invitations_accepted
"""
print
print "Cycles"
print "----------------"
print "Cycle number\tNum users\tNum referrals sent\tNum referrals accepted"
for k, num_users in num_users_by_cycle.iteritems():
    print "%s\t%s\t%s\t%s" % (k,
                              num_users,
                              num_referrals_sent_by_cycle[k],
                              num_referrals_accepted_by_cycle[k])
"""
