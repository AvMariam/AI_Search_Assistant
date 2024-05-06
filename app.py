import requests

from functions import collect_data, add_to_db, find_similars, get_collection
from flask import Flask, render_template, request, flash


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = "ai-assistant"

@app.route("/")
def index():
    flash("Hello, I am here to help you extract information from the url provided by you.")
    flash("Please enter valid url.")
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Handling empty search error
        if request.form.get('url'):
            url = request.form.get('url')
            # Handling not url search error
            try:
                requests.get(url)
            except:
                return render_template("results.html", respond="The url is invalid.")
            new_info = collect_data(url, [])
            # Handling locked website error
            if type(new_info) is list:
                new_info = new_info[0]
                db = get_collection()
                add_to_db(new_info, db)
                sim_comps = find_similars(new_info["About"])
                line_1 = f"Name of the company: {new_info['Name']},"
                line_2 = f"\nContact info: {new_info['Contacts']},"
                line_3 = f"\nIndustries company invest in: {new_info['Investment industry']},"
                line_4 = f"\nRounds company do investments: {new_info['Investment rounds']}."
                line_5 = f"\n3 similar firms are: {sim_comps}."
                return render_template("results.html", line_1=line_1, line_2=line_2,
                                       line_3=line_3, line_4=line_4, line_5=line_5)
            else:
                return render_template("results.html", respond=new_info)
        else:
            return render_template("results.html", respond="Search box is empty. Please enter url.")


if __name__ == "__main__":
    app.run(debug=True)
