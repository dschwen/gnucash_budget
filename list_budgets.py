#!/usr/bin/python
# -*- coding: utf-8 -*-

import _mysql
import sys

# user needs to provide database info and credentials here
import config

query = 'select guid, name from budgets;'

try:
    con = _mysql.connect(host=config.host, port=config.port,
                         user=config.user, passwd=config.password,
                         db=config.database)
    con.query(query)
    result = con.use_result()

    while True:
        row = result.fetch_row()
        if row == ():
            break
        print "%s %s" % row[0]

except _mysql.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
