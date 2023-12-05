import requests
import os
from dotenv import load_dotenv

load_dotenv()

def reverse_geo(lon, lat):
  r= requests.post(os.environ.get('ES_URL', 'http://elastiecsearch:9200') + '/thailand-administrative/_search', json={
    "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": [
            {
              "geo_shape": {
                "geometry": {
                  "shape": {
                    "type": "point",
                    "coordinates": [ lon, lat ]
                  },
                  "relation": "intersects"
                }
              }
            },
            {
              "exists": {
                "field": "properties.SubDistrict_TH"
              }
            }
          ]
        }
      }
    },
    headers={
      'Content-Type': 'application/json',
      'Authorization': 'ApiKey ' + os.environ.get('ES_API_KEY', 'API_KEY')
    })
  return r.json()

if __name__ == '__main__':
  loc = reverse_geo(100.65797, 13.82391)
  if len(loc['hits']['hits']) > 0:
    print({
      'แขวง': loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
      'เขต': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
      'จังหวัด': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
    })