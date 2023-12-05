import requests
import json
import datetime
import os
from requests.adapters import HTTPAdapter, Retry
import geo

lines = []
with requests.Session() as s:
    retries = Retry(total=50,
            backoff_factor=1)
    s.mount('https://', HTTPAdapter(max_retries=retries))
    r = s.get('https://publicapi.traffy.in.th/share/teamchadchart/search?state_type=start', timeout=120)
    if r.status_code < 300:
      for feature in r.json()['results']:
        loc = geo.reverse_geo(float(feature['coords'][0]), float(feature['coords'][1]))
        lines.append(json.dumps({
          "index" : { "_index" : "search-gis-bma", "_id" : 'fondue:' + feature['ticket_id'] } 
        }))
        lines.append(json.dumps({
          'id': 'fondue:' + feature['ticket_id'],
          'source': 'Traffy fondue',
          'title': feature['type'],
          'body': "%s %s บริเวณ %s หน่วยงาน %s สถานะ %s" % (feature['type'],
                              feature['description'],
                              feature['address'],
                              feature['org'],
                              feature['state'],),
          'location': [float(feature['coords'][0]), float(feature['coords'][1])],
          **({
            'district': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
            'subdistrict':loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
            'province': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
            } if len(loc['hits']['hits']) > 0 else {}),
          "retrived_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
          "created_at": datetime.datetime.strptime(feature['timestamp'] + "00", '%Y-%m-%d %H:%M:%S.%f%z').isoformat(),
          "updated_at": datetime.datetime.strptime(feature['last_activity'] + "00", '%Y-%m-%d %H:%M:%S.%f%z').isoformat()
        }))

      r = s.post(os.environ.get('ES_URL', 'http://elastiecsearch:9200') + '/_bulk', '\n'.join(lines) + '\n', headers={
        'Content-Type': 'application/json',
        'Authorization': 'ApiKey ' + os.environ.get('ES_API_KEY', 'API_KEY')
      })
      print(r.text)
    lines = []
    r = s.get('https://publicapi.traffy.in.th/share/teamchadchart/search?state_type=inprogress', timeout=120)
    if r.status_code < 300:
      for feature in r.json()['results']:
        loc = geo.reverse_geo(float(feature['coords'][0]), float(feature['coords'][1]))
        lines.append(json.dumps({
          "index" : { "_index" : "search-gis-bma", "_id" : feature['ticket_id'] } 
        }))
        lines.append(json.dumps({
          'id': 'fondue:' + feature['ticket_id'],
          'source': 'Traffy fondue',
          'title': feature['type'],
          'body': "%s %s บริเวณ %s หน่วยงาน %s สถานะ %s" % (feature['type'],
                              feature['description'],
                              feature['address'],
                              feature['org'],
                              feature['state'],),
          'location': [float(feature['coords'][0]), float(feature['coords'][1])],
          **({
            'district': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
            'subdistrict':loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
            'province': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
            } if len(loc['hits']['hits']) > 0 else {}),
          "retrived_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
          "created_at": datetime.datetime.strptime(feature['timestamp'] + "00", '%Y-%m-%d %H:%M:%S.%f%z').isoformat(),
          "updated_at": datetime.datetime.strptime(feature['last_activity'] + "00", '%Y-%m-%d %H:%M:%S.%f%z').isoformat()
        }))
      r = s.post(os.environ.get('ES_URL', 'http://elastiecsearch:9200') + '/_bulk', '\n'.join(lines) + '\n', headers={
        'Content-Type': 'application/json',
        'Authorization': 'ApiKey ' + os.environ.get('ES_API_KEY', 'API_KEY')
      })
      print(r.text)
    lines = []
    r = s.get('https://publicapi.traffy.in.th/share/teamchadchart/search?state_type=forward', timeout=120)
    if r.status_code < 300:
      for feature in r.json()['results']:
        loc = geo.reverse_geo(float(feature['coords'][0]), float(feature['coords'][1]))
        lines.append(json.dumps({
          "index" : { "_index" : "search-gis-bma", "_id" : feature['ticket_id'] } 
        }))
        lines.append(json.dumps({
          'id': 'fondue:' + feature['ticket_id'],
          'source': 'Traffy fondue',
          'title': feature['type'],
          'body': "%s %s บริเวณ %s หน่วยงาน %s สถานะ %s" % (feature['type'],
                              feature['description'],
                              feature['address'],
                              feature['org'],
                              feature['state'],),
          'location': [float(feature['coords'][0]), float(feature['coords'][1])],
          **({
            'district': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
            'subdistrict':loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
            'province': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
            } if len(loc['hits']['hits']) > 0 else {}),
          "retrived_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
          "created_at": datetime.datetime.strptime(feature['timestamp'] + "00", '%Y-%m-%d %H:%M:%S.%f%z').isoformat(),
          "updated_at": datetime.datetime.strptime(feature['last_activity'] + "00", '%Y-%m-%d %H:%M:%S.%f%z').isoformat()
        }))

      r = s.post(os.environ.get('ES_URL', 'http://elastiecsearch:9200') + '/_bulk', '\n'.join(lines) + '\n', headers={
        'Content-Type': 'application/json',
        'Authorization': 'ApiKey ' + os.environ.get('ES_API_KEY', 'API_KEY')
      })
      print(r.text)

