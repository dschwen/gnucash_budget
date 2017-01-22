#!/usr/bin/python
# -*- coding: utf-8 -*-

import _mysql
import sys

# user needs to provide database info and credentials here
import config

if len(sys.argv) != 3:
    print "Split the 1 year budget 'inguid' into a 12 month budget 'outguid'."
    print "Both budgets must exist. Determine the guids using list_budgets.py"
    print "Usage: %s inguid outguid" % sys.argv[0]
    sys.exit(1)

inguid = sys.argv[1]
outguid = sys.argv[2]

try:
    con1 = _mysql.connect(host=config.host, port=config.port,
                          user=config.user, passwd=config.password,
                          db=config.database)

    con2 = _mysql.connect(host=config.host, port=config.port,
                          user=config.user, passwd=config.password,
                          db=config.database)


    # select the entries of the annual budget (inguid)
    query = "select account_guid, amount_num, amount_denom from budget_amounts where budget_guid = '%s' and period_num = 0;" % inguid
    con1.query(query)
    result = con1.use_result()

    # delete the output budget entries
    query = "delete from budget_amounts where budget_guid = '%s';" % outguid
    con2.query(query)

    while True:
        row = result.fetch_row()
        if row == ():
            break
        print "%s %s %s" % row[0]
        account_guid = row[0][0]
        amount_num = int(row[0][1])
        amount_denom = int(row[0][2])
        amount = amount_num * 100 / amount_denom
        cents_per_month = amount / 12
        modulo = amount % 12

        values = []
        for period in range(12):
            if period < modulo:
                amount = cents_per_month + 1
            else:
                amount = cents_per_month

            if amount % 100 == 0:
                amount = amount / 100
                denom = 1
            else:
                denom = 100

            values.append("('%s', '%s', %d, %d, %d) " % (outguid, account_guid, period, amount, denom))

        query = "insert into budget_amounts (budget_guid, account_guid, period_num, amount_num, amount_denom) values %s" % ','.join(values)
        con2.query(query)

except _mysql.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con1:
        con1.close()

    if con2:
        con2.close()

# c.executemany(
#       """INSERT INTO breakfast (name, spam, eggs, sausage, price)
#       VALUES (%s, %s, %s, %s, %s)""",
#       [
#       ("Spam and Sausage Lover's Plate", 5, 1, 8, 7.95 ),
#       ("Not So Much Spam Plate", 3, 2, 0, 3.95 ),
#       ("Don't Wany ANY SPAM! Plate", 0, 4, 3, 5.95 )
#       ] )
