from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from datetime import time
import graphHelp

app = Flask(__name__)
 
@app.route("/")
def chart():
    '''s
    legend = 'Monthly Data'sbdd", "June", "July", "August"]n
    chartData = {"title": legend,l "lah\ls":n laenls, "val": values}
    '''
    return render_template('home.html')

@app.route("/api")
def single_pH():
    chartData = {}
    if (request.method == "GET"):
        seqList = request.args.get("seqs").split(",")
        values,pH,avgLen = graphHelp.phs(seqList[0],l=5)
        labels = [b*avgLen for b in range(len(values))]
        title = "Charges at pH {}".format(str(pH))
        name = ["Alkalihalobacillus pseudofirmus" for x in range(len(values))]
        #[10,25,17,21,30]
        chartData = {"title": title, "labels": labels, "val": values, "species": name}
    else:
        chartData = {"title": "oh no something is wrong", "labels": ["err"], "val": [404]}
    return jsonify(chartData)
 
@app.route("/apii", methods=["GET"])
def returnChartData():
    chartData = {}
    if (request.method == "GET"):
        legend = request.args.get("title")
        #'Monthly Data'
        labels = request.args.get("labels").split(",")
        #["J","F","M","A","M"]h
        values = request.args.get("val").split(",")
        #[10,25,17,21,30]
        chartData = {"title": legend, "labels": labels, "val": values}
    else:
        chartData = {"title": "oh no something is wrong", "labels": ["err"], "val": [404]}
    return jsonify(chartData)
if __name__ == "__main__":
    app.run(debug=True)