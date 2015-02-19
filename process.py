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

import unicodedata
 
def deaccent(some_unicode_string):
    return u''.join(c for c in unicodedata.normalize('NFD', some_unicode_string)
               if unicodedata.category(c) != 'Mn')

def processFile(f):
  processFeatures(fiona.open(f))

def processFeatures(input):
  for f in input:
    basefilename = f['properties']['GEOID'] + '-' + deaccent(f['properties']['NAME'].lower().replace(' ', '_').replace('/', '_'))
    filename = basefilename + '.geojson'
    directory = data_dir + '/' + us.states.lookup(f['properties']['STATEFP']).abbr + '/' + f['properties']['NAME'][0]
    if not os.path.exists(directory):
      os.makedirs(directory)
    print 'writing %s' % filename
    output = fiona.open('%s/%s' % (directory, filename), 'w', schema = input.schema, driver='GeoJSON')
    output.write(f)
    output.close()
    print 'wrote %s' % filename

    if True:
      shapefile = '%s/%s.shp' % (directory, filename)
      print shapefile
      output = fiona.open(shapefile,  'w', schema = input.schema, driver='ESRI Shapefile')
      output.write(f)
      output.close()

      from kartograph import Kartograph

      attributes = f['properties'].keys()

      cfg = {
        "layers": {
            "mylayer": {
                "labeling": { "key": "NAME" },
                "attributes": attributes,
                "src": shapefile
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
      K.generate(cfg, outfile=os.path.join(directory, filename))

for f in input_files:
  processFile(f)
