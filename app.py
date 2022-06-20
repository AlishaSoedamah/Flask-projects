from flask import Flask
from flask import render_template
from flask import redirect, url_for, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


@app.route("/scrape")
def scrape():
    url = "https://stagemarkt.nl/vacatures/?Termen=Software+developer+(25604)&PlaatsPostcode=amsterdam&Straal=0&Land=e883076c-11d5-11d4-90d3-009027dcddb5&ZoekenIn=A&Page=1&Longitude=&Latitude=&Regio=&Plaats=&Niveau=&SBI=&Kwalificatie=&Sector=&RandomSeed=743&Leerweg=&Internationaal=&Beschikbaarheid=&AlleWerkprocessenUitvoerbaar=&LeerplaatsGewijzigd=&Sortering=0&Bron=STA&Focus=&LeerplaatsKenmerk=&OrganisatieKenmerk="
    request = requests.get(url)
    html = str(request.text)
    soup = BeautifulSoup(html, 'html.parser')

    output = soup.find(class_="c-link-blocks-single")

    vacaturesHTML = soup.find_all(class_="c-link-blocks-single")
    vacatureList = []
    for vacature in vacaturesHTML:
        vacatureDict = {
            "title": str(vacature.h2.text),
            "bedrijf": str(vacature.h3.text),
            "link": str("http://www.stagemarkt.nl" + vacature['href'])
        }
    vacatureList.append(vacatureDict)
    # return json.dumps(vacatureList)

    for vacature in vacatureList:
        request = requests.get(vacature['link'])
        html = request.text
        soup = BeautifulSoup(html, 'html.parser')

        companyDetails = soup.find(class_="c-detail-company")

        # sstores this string in the vacancy dict under key 'straat'
        vacature['straat'] = str(companyDetails.contents[3].contents[3].text)

        i = 0
        for item in companyDetails.contents:
            print(str(i) + " - " + str(item) + "<br>")
            i = i + 1

        json.dumps(vacatureList)
        return str(companyDetails.contents[3].text)


@app.route("/")
def index():
    return "<h1>A cool title!</h1>"


@app.route("/helloworld")  # add /helloworld in url from liveserver
def helloWorld():
    return "Hello world"


@app.route("/user/<name>")  # add /user*name* in url from liveserver
def getUser(name):
    return "User is " + name


# add /login in url from liveserver
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("getUser", name=user))
    else:
        user = request.args.get("name")
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
