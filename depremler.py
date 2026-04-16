import requests
import time
import xmltodict
import json
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

startYear = 2023
endYear = date.today().year

WORKERS = 16
MAX_RETRIES = 3

def make_session():
    session = requests.Session()
    retry = Retry(
        total=MAX_RETRIES,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_month(session, year, month):
    url = f'http://udim.koeri.boun.edu.tr/zeqmap/xmlt/{year}{str(month).zfill(2)}.xml'
    response = session.get(url, timeout=30)
    if response.status_code == 404:
        return year, month, []
    data_dict = xmltodict.parse(response.content)
    items = data_dict["eqlist"]["earhquake"]
    return year, month, items

print("veriler alınıyor...")

start = time.time()

session = make_session()
tasks = [(year, month) for year in range(startYear, endYear + 1) for month in range(1, 13)]
year_items = {year: [] for year in range(startYear, endYear + 1)}

with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    futures = {executor.submit(fetch_month, session, year, month): (year, month) for year, month in tasks}
    for future in as_completed(futures):
        year, month, items = future.result()
        year_items[year].extend(items)

for year in range(startYear, endYear + 1):
    results = []
    for item in year_items[year]:
        results.append({
            "id": len(results),
            "date": str(item["@name"]).strip().replace('.', '-'),
            "location": str(item["@lokasyon"]).replace('\u00ddlksel', 'ilksel').replace('   ', '').strip(),
            "lat": float(item["@lat"].replace(' ', '')),
            "lng": float(item["@lng"].replace(' ', '')),
            "mag": float(str(item["@mag"]).replace('-.-', '0.0')),
            "depth": float(item["@Depth"])
        })
    with open(f"./viewer/data/{year}.json", "w", encoding='utf-8') as json_file:
        json_file.write(json.dumps(results, indent=2))

end = time.time()

print(f"veriler yazıldı ({round(end-start,1)}s)")
