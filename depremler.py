import requests
import time
import xmltodict
import json

results = {}
startYear = 2003
endYear = 2022

print("veriler alınıyor...")

start = time.time()
for i in range(startYear,endYear+1):
  for j in range(1,13):
    results[str(j).zfill(2)] = []
    response = requests.get(f'http://udim.koeri.boun.edu.tr/zeqmap/xmlt/{i}{str(j).zfill(2)}.xml')
    data_dict = xmltodict.parse(response.content)
    if(response.status_code != 404):
      items = data_dict["eqlist"]["earhquake"]
      for index,item in enumerate(items):
        results[str(j).zfill(2)].insert(index,{
          "name": str(item["@name"]).strip(),
          "location": str(item["@lokasyon"]).replace('\u00ddlksel','ilksel').replace('   ','').strip(),
          "lat": float(item["@lat"]),
          "lng": float(item["@lng"]),
          "mag": float(str(item["@mag"]).replace('-.-','0.0')),
          "depth": float(item["@Depth"])
        })
  with open(f"{i}.json", "w", encoding='utf-8') as json_file:
    json_file.write(json.dumps(results,indent=2))
    json_file.close()
end = time.time()

print(f"veriler yazıldı ({round(end-start,1)}s)")