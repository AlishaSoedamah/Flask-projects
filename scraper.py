import requests
import json
from bs4 import BeautifulSoup

url = "https://stagemarkt.nl/vacatures/?Termen=Software+developer+(25604)&PlaatsPostcode=amsterdam&Straal=0&Land=e883076c-11d5-11d4-90d3-009027dcddb5&ZoekenIn=A&Page=1&Longitude=&Latitude=&Regio=&Plaats=&Niveau=&SBI=&Kwalificatie=&Sector=&RandomSeed=743&Leerweg=&Internationaal=&Beschikbaarheid=&AlleWerkprocessenUitvoerbaar=&LeerplaatsGewijzigd=&Sortering=0&Bron=STA&Focus=&LeerplaatsKenmerk=&OrganisatieKenmerk="

request = requests.get(url)
html = str(request.text)
soup = BeautifulSoup(html, 'html.parser')

vacaturesHTML = soup.find_all(class_="c-link-blocks-single")
vacatureList = []

for vacature in vacaturesHTML:
    vacatureDict = {
        "title": str(vacature.h2.text),
        "bedrijf": str(vacature.h3.text),
        "link": str("http://www.stagemarkt.nl" + vacature['href'])
    }
    vacatureList.append(vacatureDict)

counter = 0
for vacature in vacatureList:
    print("fetching vacature nr: " + str(counter))  # progress feedback
    request = requests.get(vacature['link'])
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    companyDetails = soup.find(class_="c-detail-company")
    counter += 1

print("complete")  # scrape complete
print(json.dumps(vacatureList))
