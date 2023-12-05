import os
from dotenv import load_dotenv
import requests
import mysql.connector
import datetime
import json
import geo
import re

load_dotenv()

connection = mysql.connector.connect(
 host=os.environ.get('MYSQL_HOST', 'localhost'),
 port=int(os.environ('MYSQL_PORT', '3306')),
 user=os.environ.get('MYSQL_USER', 'user'),
 password=os.environ.get('MYSQL_PASSWORD', 'password'),
 database=os.environ.get('MYSQL_DATABASE', 'database'),
)

db_cursor = connection.cursor()

db_cursor.execute("""SELECT project_id AS id, project_name AS title ,
                  CONCAT(conception, ' ', objective_note, ' ', target_note, ' ', contact_person, ' ', telephone_no) AS body,
                  x ,y, created_at, updated_at FROM tbl_project_main;
""")
                  

results = db_cursor.fetchall()

lines = []

for result in results:
  loc = geo.reverse_geo(float(result[4]), float(result[3]))
  print(loc['hits']['hits'][0]['_source']['properties'])
  lines.append(json.dumps({
    "index" : { "_index" : "search-gis-bma", "_id" : 'project:' + result[0] } 
  }))
  lines.append(json.dumps({
    'id': 'project:' + p['id'],
    'source': 'BMA project',
    "title" : re.sub(r'/\s', ' ', result[1]).strip(),
    "body" : re.sub(r'/\s', ' ', result[2]).strip(),
    'location': [float(result[4]), float(result[3])],
    **({
      'district': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
      'subdistrict':loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
      'province': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
      } if len(loc['hits']['hits']) > 0 else {}),
    "retrived_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "created_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "updated_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
  }))

if len(lines) > 0:
  r = requests.post(os.environ.get('ES_URL', 'http://elastiecsearch:9200') + '/_bulk', '\n'.join(lines) + '\n', headers={
    'Content-Type': 'application/json',
    'Authorization': 'ApiKey ' + os.environ.get('ES_API_KEY', 'API_KEY')
  })
  print(r.text)