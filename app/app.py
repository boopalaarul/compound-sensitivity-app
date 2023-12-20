from flask import Flask, render_template, request, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

import tests

#init new Flask object
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route("/")
def index(): #mainpage HTML
    """
        Displays a form to the user with three datalist inputs.
    """
    with open("../data/site_names.txt") as f:
        sites = f.readlines()
    with open("../data/histology_names.txt") as f:
        histologies = f.readlines()
    with open("../data/compound_names.txt") as f:
        compounds = f.readlines()

    return render_template("index.html", data={
        "sites" : sites, 
        "histologies" : histologies,
        "compounds" : compounds
    })

@app.route("/render-output", methods=["GET", "POST"])
def render_output_page():
    """
        Renders output page with graphs and statistics produced in tests.py.
    """
    if request.method == "POST":
        site = request.form.get('site')
        histology = request.form.get('histology')
        compound = request.form.get('compound')

        data_summary, site_results, hist_results, site_table, hist_table = tests.sensitivity_tests(compound)

        return render_template("output.html", 
                               data=data_summary, 
                               site_table=site_table, 
                               hist_table=hist_table,
                               site_results=site_results,
                               hist_results=hist_results,
                               site_id=site,
                               hist_id=histology)
    return redirect(url_for("index"))