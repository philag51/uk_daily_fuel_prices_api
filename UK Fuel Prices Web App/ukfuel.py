import requests as rq
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    fuel = None
    petrol = None
    diesel = None

    if request.method == "POST":
        address = request.form.get("address")
        filter_option = request.form.get("filter", "all")

        if address:
            querystring = {"address": address}
            headers = {
                "x-rapidapi-key": "{API_KEY}",
                "x-rapidapi-host": "uk-daily-fuel-prices.p.rapidapi.com"
            }
            url = "https://uk-daily-fuel-prices.p.rapidapi.com/api/petrol-prices/search"
            response = rq.get(url, headers=headers, params=querystring)

            if response.status_code == 200:
                data = response.json()
                fuel = data.get("data", [])
            else:
                fuel = []

            if filter_option == "cheapest_petrol":
                fuel = sorted(
                    [s for s in fuel if s["prices"].get("E10")],
                    key=lambda s: s["prices"]["E10"]
                )

            elif filter_option == "cheapest_diesel":
                fuel = sorted(
                    [s for s in fuel if s["prices"].get("B7")],
                    key=lambda s: s["prices"]["B7"]
                )



    # Always return the HTML page — whether it's GET or POST
    return render_template("fuel.html", fuel = fuel, year = datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True)

