#!/usr/bin/python

import fiona
import os
import sys
import us
 
from os import listdir
from os.path import isfile, join
input_files = [ join('srcdata', f) for f in listdir('srcdata') if isfile(join('srcdata',f)) and f.endswith('shp') ]

data_dir = 'individual'
svg_dir = 'svg'

def processFile(f):
  processFeatures(fiona.open(f))

def processFeatures(input):
  for f in input:
    filename = f['properties']['GEOID'] + '-' + f['properties']['NAME'].lower().replace(' ', '_').replace('/', '_') + '.geojson'
    directory = 'data/' + us.states.lookup(f['properties']['STATEFP']).abbr
    if not os.path.exists(directory):
      os.makedirs(directory)
    print 'writing %s' % filename
    output = fiona.open('%s/%s' % (directory, filename), 'w', schema = input.schema, driver='GeoJSON')
    output.write(f)
    output.close()
    print 'wrote %s' % filename

    if False:
      from kartograph import Kartograph
      output = fiona.open('/tmp/t.shp', 'w', schema = input.schema, driver = 'ESRI Shapefile')

      cfg = {
        "layers": {
            "mylayer": {
                "labeling": f['properties'],
                "src": "/tmp/t.shp",
            }
        },
        "export": {
          "width": 1000,
          "height": 1000
        }
      }


      K = Kartograph()

      filename = filename.replace('.geojson', '.svg')
      directory = 'svg/' + directory
      if not os.path.exists(directory):
        os.makedirs(directory)
      output = fiona.open('%s/%s' % (directory, filename), 'w', schema = input.schema, driver='GeoJSON')
      K.generate(cfg, outfile='mymap.svg')

for f in input_files:
  processFile(f)
