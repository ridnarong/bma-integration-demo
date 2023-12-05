import requests
import json
import datetime
import os
import geo


lines = []

r = requests.get('https://bmagis.bangkok.go.th/arcgis/rest/services/RISK_Tedsakit/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Kilometer&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&having=&gdbVersion=&historicMoment=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=xyFootprint&resultOffset=&resultRecordCount=&returnTrueCurves=false&returnExceededLimitFeatures=false&quantizationParameters=&returnCentroid=false&sqlFormat=none&resultType=&featureEncoding=esriCompressedShapeBuffer&f=geojson')
for feature in r.json()['features']:
  loc = geo.reverse_geo(feature['geometry']['coordinates'][0], feature['geometry']['coordinates'][1])
  lines.append(json.dumps({
    "index" : { "_index" : "search-gis-bma", "_id" : 'riskMapTedsakit:' + feature['properties']['GLOBALID_1'].replace('{', '').replace('}', '') } 
  }))
  risk_type = []
  area_type = []
  improve_type = []
  if feature['properties']["PUBLIC_"]:
    area_type.append('สาธารณะ')
  if feature['properties']["PRIVATE"]:
    area_type.append('เอกชน')
  if feature['properties']["SERVICE"]:
    area_type.append('บริการ')
  if feature['properties']["MONASTERY"]:
    area_type.append('วัด')
  if feature['properties']["ENTERPRISE"]:
    area_type.append('บริษัท')
  if feature['properties']["OVERPASS"]:
    area_type.append('สะพานลอยคนเดินข้าม/รถจักรยานยนต์ข้าม')
  if feature['properties']["POSTAL_SIG"]:
    area_type.append('ตู้ไปรษณี')
  if feature['properties']["PARK"]:
    area_type.append('สวนสาธารณะ/สวนหย่อม')
  if feature['properties']["ESTABLISHM"]:
    area_type.append('อนุสาวรีย์')
  if feature['properties']["CONDO_HOUS"]:
    area_type.append('คอนโด หมู่บ้าน')
  if feature['properties']["LAND"]:
    area_type.append('ที่ดิน (ว่างเปล่า)')
  if feature['properties']["GARDEN"]:
    area_type.append('สวน')
  if feature['properties']["ROAD"]:
    area_type.append('ถนน')
  if feature['properties']["PAVEMENT"]:
    area_type.append('ทางเท้า')
  if feature['properties']["ALLEY"]:
    area_type.append('ซอย')
  if feature['properties']["UNDER_BRID"]:
    area_type.append('พื้นที่ใต้ (ด้านล่าง) สะพาน ถนน ทางด่วน')
  if feature['properties']["COMMUNITY"]:
    area_type.append('ชุมชน')
  if feature['properties']["MARKET"]:
    area_type.append('ตลาด')
  if feature['properties']["ATTRACTION"]:
    area_type.append('สถานที่ท่องเที่ยว')
  if feature['properties']["ACADEMY"]:
    area_type.append('โรงเรียน')
  if feature['properties']["GOVERNMENT"]:
    area_type.append('สถานที่ราชการ')
  if feature['properties']["RELIGIOUS_"]:
    area_type.append('ศาสนสถาน')
  if feature['properties']["SPORTS_CEN"]:
    area_type.append('ศูนย์กีฬา')
  if feature['properties']["TRAIN_STAT"]:
    area_type.append('สถานีรถไฟ')
  if feature['properties']["BUS_STATIO"]:
    area_type.append('ป้ายรถโดยสารประจำทาง')
  if feature['properties']["PORT"]:
    area_type.append('โป๊ะ/ท่าเรือ')
  if feature['properties']["WATERFRONT"]:
    area_type.append('ริมน้ำ')
  if feature['properties']["CROSSROADS"]:
    area_type.append('ทางม้าลาย')
  area_type.append(feature['properties']["ETC"])
  if feature['properties']['RISKTYPE1']:
    risk_type.append('จุดมืด จุดเปลี่ยว')
  if feature['properties']['RISKTYPE2']:
    risk_type.append('จุดรกร้าง/พื้นที่ลักลอบทิ้งขยะ')
  if feature['properties']['RISKTYPE3']:
    risk_type.append('.โครงสร้างวัสดุชำรุดรอซ่อมแซม/ติดตั้งเพิ่ม')
  if feature['properties']['RISKTYPE4']:
    risk_type.append('แหล่งมั่วสุม')
  if feature['properties']['RISKTYPE5']:
    risk_type.append('จุดล่อแหลมต่อการเกิดอาชญากรรม')
  if feature['properties']['RISKTYPE6']:
    risk_type.append('ประชากรหนาแน่น/พลุกพล่าน')
  if feature['properties']['RISKTYPE7']:
    risk_type.append('จุดที่กำลังดำเนินการแก้ไขต่อการเกิดอุบัติเหตุ')

  if feature['properties']["SURVEILLAN"]:
    improve_type.append('ตรวจตราและเฝ้าระวัง')
  if feature['properties']["CLEAN"]:
    improve_type.append('ทำความสะอาด')
  if feature['properties']["PRUNING"]:
    improve_type.append('ดูแลรักษา/ตัดแต่งต้นไม้')
  if feature['properties']["ADJUST_LAN"]:
    improve_type.append('ปรับภูมิทัศน์')
  if feature['properties']["DISMANTLE"]:
    improve_type.append('รื้อถอน')
  if feature['properties']["CCTV"]:
    improve_type.append('ติดตั้งกล้องวงจรปิด (CCTV)')
  if feature['properties']["INSTALL_LI"]:
    improve_type.append('ติดตั้งไฟส่องสว่าง')
  if feature['properties']["REPAIR_LIG"]:
    improve_type.append('บำรุง/ซ่อมแซมไฟส่องสว่าง')
  if feature['properties']["ALERT_SIGN"]:
    improve_type.append('ติดป้ายประชาสัมพันธ์/ป้ายแจ้งเตือน')
  if feature['properties']["INSTALL_RE"]:
    improve_type.append('ติดตั้ง/ซ่อมแซมไฟสัญญาณ')
  if feature['properties']["INSTALL_SA"]:
    improve_type.append('ติดตั้งวัสดุอุปกรณ์ด้านความปลอดภัยเพิ่มเติม')
  if feature['properties']["ARREST"]:
    improve_type.append('ตักเตือน/จับ/ปรับ/ดำเนินการทางกฎหมาย (ตามอำนาจหน้าที่)')
  if feature['properties']["REPAIR_SID"]:
    improve_type.append('ซ่อมทางเท้า')
  if feature['properties']["REPAIR_ROA"]:
    improve_type.append('ซ่อมถนน')
  if feature['properties']["ORGANIZE_T"]:
    improve_type.append('จัดเจ้าหน้าที่จราจร')
  if feature['properties']["COOD_POLIC"]:
    improve_type.append('ประสาน สน.')
  if feature['properties']["COOD_RELEV"]:
    improve_type.append('.ประสานเจ้าของพื้นที่/หน่วยงานที่เกี่ยวข้อง')
  if feature['properties']["BOX_EMERGE"]:
    improve_type.append('ติดตั้งตู้เขียว')
  lines.append(json.dumps({
    'id': 'riskMapTedsakit:' + feature['properties']['GLOBALID'].replace('{', '').replace('}', ''),
    'source': 'BMA Risk Map : Tedsakit',
    'title': feature['properties']['LOCATION'],
    'body': "เขต	%s บริเวณที่ตั้ง	%s สถานีตำรวจนครบาล	%s ประเภทความเสี่ยง	%s ประเภทสถานที่	%s วิธีดำเนินการแก้ไข	%s" % (feature['properties']['DNAME'],
                         feature['properties']['LOCATION'],
                         feature['properties']['POLICE_STA'],
                         ' '.join(risk_type),
                         ' '.join(area_type),
                         ' '.join(improve_type),),
    'district': feature['properties']['DNAME'],
      **({
        'district': loc['hits']['hits'][0]['_source']['properties']['District_TH'],
        'subdistrict':loc['hits']['hits'][0]['_source']['properties']['SubDistrict_TH'],
        'province': loc['hits']['hits'][0]['_source']['properties']['Province_TH']
        } if len(loc['hits']['hits']) > 0 else {}),
    'location': [feature['geometry']['coordinates'][0], feature['geometry']['coordinates'][1]],
    "retrived_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "created_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
    "updated_at": datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
  }))


r = requests.post(os.environ.get('ES_URL', 'http://elastiecsearch:9200') +'/_bulk', '\n'.join(lines) + '\n', headers={
  'Content-Type': 'application/json',
  'Authorization': 'ApiKey ' + os.environ.get('ES_API_KEY', 'API_KEY')
})
print(r.text)