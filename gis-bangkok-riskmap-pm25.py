import requests
import json
import datetime
import os
import geo

API_KEY = 'API_KEY'

lines = []

r = requests.get('https://bmagis.bangkok.go.th/arcgis/rest/services/RISK_pnt_pm25_6465_district/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&having=&gdbVersion=&historicMoment=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=xyFootprint&resultOffset=&resultRecordCount=&returnTrueCurves=false&returnExceededLimitFeatures=false&quantizationParameters=&returnCentroid=false&sqlFormat=none&resultType=&featureEncoding=esriDefault&f=pjson')
for feature in r.json()['features']:
  loc = geo.reverse_geo(feature['attributes']['LONGITUDE'], feature['attributes']['LATITUDE'])
  lines.append(json.dumps({
    "index" : { "_index" : "search-gis-bma", "_id" : 'riskMapPM25:' + str(feature['attributes']['OBJECTID']).replace('{', '').replace('}', '') } 
  }))
  lines.append(json.dumps({
    'id': 'riskMapPM25:' + str(feature['attributes']['OBJECTID']).replace('{', '').replace('}', ''),
    'source': 'BMA Risk Map : PM 2.5',
    'title': feature['attributes']['STATION'],
    'body': "สถานี %s ฝุ่นเกินกว่า 50 ไมโครกรัมต่อลูกบาศก์เมตร ต่อเนื่องเกิน 3 วัน จำนวน %d วัน" % (feature['attributes']['STATION'],
                         feature['attributes']['PL25COUNT_OVER50'],),
      **({
        'district': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
        'subdistrict':loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
        'province': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
        } if len(loc['hits']['hits']) > 0 else {}),
    'location': [feature['attributes']['LONGITUDE'], feature['attributes']['LATITUDE']],
    "retrived_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "created_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "updated_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
  }))

r = requests.get('https://bmagis.bangkok.go.th/arcgis/rest/services/RISK_PM25_AVG_YEAR/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&having=&gdbVersion=&historicMoment=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=xyFootprint&resultOffset=&resultRecordCount=&returnTrueCurves=false&returnExceededLimitFeatures=false&quantizationParameters=&returnCentroid=false&sqlFormat=none&resultType=&featureEncoding=esriDefault&f=pjson')
for feature in r.json()['features']:
  loc = geo.reverse_geo(feature['geometry']['x'] if 'geometry' in feature else 0, feature['geometry']['y'] if 'geometry' in feature else 0)
  lines.append(json.dumps({
    "index" : { "_index" : "search-gis-bma", "_id" : 'riskMapPM25:' + feature['attributes']['GLOBALID'].replace('{', '').replace('}', '') } 
  }))
  lines.append(json.dumps({
    'id': 'riskMapPM25:' + feature['attributes']['GLOBALID'].replace('{', '').replace('}', ''),
    'source': 'BMA Risk Map : PM 2.5',
    'title': feature['attributes']['PLACE_1'],
    'body': "บริเวณ %s ค่าเฉลี่ย PM 2.5 ทั้งปี %f" % (feature['attributes']['PLACE_1'],
                         feature['attributes']['MEAN_PM2_5'],),
      **({
        'district': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
        'subdistrict':loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
        'province': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
        } if len(loc['hits']['hits']) > 0 else {}),
    'location': [feature['geometry']['x'] if 'geometry' in feature else 0, feature['geometry']['y'] if 'geometry' in feature else 0],
    "retrived_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "created_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "updated_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
  }))


r = requests.post(os.environ.get('ES_URL', 'http://elastiecsearch:9200') + '/_bulk', '\n'.join(lines) + '\n', headers={
  'Content-Type': 'application/json',
  'Authorization': 'ApiKey ' + os.environ.get('ES_API_KEY', 'API_KEY')
})
print(r.text)