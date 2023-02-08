import requests
import time
import xmltodict
import json
from datetime import date

startYear = 2023
endYear = date.today().year

print("veriler alınıyor...")

start = time.time()
for i in range(startYear,endYear+1):
  results = []
  index = 0
  for j in range(1,13):
    response = requests.get(f'http://udim.koeri.boun.edu.tr/zeqmap/xmlt/{i}{str(j).zfill(2)}.xml')
    data_dict = xmltodict.parse(response.content)
    if(response.status_code != 404):
      items = data_dict["eqlist"]["earhquake"]
      for item in items:
        
        results.insert(index,{
          "id": index,
          "date": str(item["@name"]).strip().replace('.','-'),
          "location": str(item["@lokasyon"]).replace('\u00ddlksel','ilksel').replace('   ','').strip(),
          "lat": float(item["@lat"].replace(' ','')),
          "lng": float(item["@lng"].replace(' ', '')),
          "mag": float(str(item["@mag"]).replace('-.-','0.0')),
          "depth": float(item["@Depth"])
        })
        index += 1      
  with open(f"./viewer/data/{i}.json", "w", encoding='utf-8') as json_file:
    json_file.write(json.dumps(results,indent=2))
    json_file.close()
end = time.time()

print(f"veriler yazıldı ({round(end-start,1)}s)")
