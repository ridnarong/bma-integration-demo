import requests
import json
import datetime
import os
import geo

lines = []

r = requests.get('https://bmagis.bangkok.go.th/arcgis/rest/services/FloodProblemBmaFinal/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Kilometer&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&having=&gdbVersion=&historicMoment=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=xyFootprint&resultOffset=&resultRecordCount=&returnTrueCurves=false&returnExceededLimitFeatures=false&quantizationParameters=&returnCentroid=false&sqlFormat=none&resultType=&featureEncoding=esriDefault&f=pjson')

for feature in r.json()['features']:
  loc = geo.reverse_geo(feature['geometry']['x'], feature['geometry']['y'])
  lines.append(json.dumps({
    "index" : { "_index" : "search-gis-bma", "_id" : 'riskMapFlood:' + feature['attributes']['GLOBALID'].replace('{', '').replace('}', '') } 
  }))
  lines.append(json.dumps({
    'id': 'riskMapFlood:' + feature['attributes']['GLOBALID'].replace('{', '').replace('}', ''),
    'source': 'BMA Risk Map : Flood',
    'title': feature['attributes']['NAME'],
    'body': "ประเภทปัญหา %s รายละเอียด %s โครงการ %s" % (feature['attributes']['TYPEPROBELM'],
                         feature['attributes']['DETAIL'],
                         feature['attributes']['PROJECT'],),
    'location': [feature['geometry']['x'], feature['geometry']['y']],
    **({
      'district': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
      'subdistrict':loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
      'province': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
      } if len(loc['hits']['hits']) > 0 else {}),
    "retrived_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "created_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "updated_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
  }))


r = requests.post(os.environ.get('ES_URL', 'http://elastiecsearch:9200') + '/_bulk', '\n'.join(lines) + '\n', headers={
  'Content-Type': 'application/json',
  'Authorization': 'ApiKey ' + os.environ.get('ES_API_KEY', 'API_KEY')
})
print(r.text)