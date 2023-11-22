import requests
from bs4 import BeautifulSoup as bs
import re

link1 = "https://2ip.ru/"
link2 = "https://www.maxmind.com/en/geoip2-precision-demo"
link3 = "https://gist.github.com/salkar/19df1918ee2aed6669e2"
url_token = "https://www.maxmind.com/en/geoip2/demo/token"
email = "test@gmail.com"
data = {"email": email} 
s = requests.session()

# Первый сайт
conn = s.get(link1)
soup = bs(conn.text, "html.parser")

ip = soup.find('div', id='d_clip_button')
myIp = ip.span.text

conn.close()

# Второй сайт
conn = s.get(link2) 
soup = bs(conn.text, "html.parser")
script_tags = soup.find_all("script", attrs={"nonce": True})
for script_tag in script_tags:
    script_text = script_tag.text
    pattern = r"window.MaxMind.X_CSRF_TOKEN = \"(.*?)\"" 
    match = re.search(pattern, script_text)
    if match:
        token = match.group(1) 
        break 

headers = {"Content-type": "application/json", "X-Csrf-Token": token}
response = s.post(url_token, headers=headers, json=data) 
token2 = response.json()['token']

url_geoip = "https://geoip.maxmind.com/geoip/v2.1/city/" + myIp + "?demo=1"
headers = {"Authorization": f"Bearer {token2}"} 
response = requests.get(url_geoip, headers=headers)
data = response.json() 
time_zone = data['location']['time_zone']

conn.close()

# Третий сайт
conn = s.get(link3)
soup = bs(conn.text, "html.parser")

td_elements = soup.find_all("td", id=re.compile("^file-timezones-for-russian-regions"))

data = {}

for td in td_elements:
    td_text = td.get_text()
    match = re.search(r'\["(.*?)", "(.*?)"\]', td_text)
    if match:
        timezone = match.group(2) 
        region = match.group(1) 
        data.setdefault(timezone, []).append(region)

with open("timezones.txt", "w", encoding="utf-8") as f:
    for timezone, regions in data.items():
        if timezone == "Asia/Krasnoyarsk":
            f.write(timezone + "\n")
            for region in regions:
                f.write(region + "\n")
            f.write("\n")
conn.close()