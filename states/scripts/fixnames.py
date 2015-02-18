#!/usr/bin/python

import us
import sys

for f in sys.argv[1:]:
  print 'mv %s %s-places.geojson' % (f, us.states.lookup(f.split('_')[2]).abbr)
