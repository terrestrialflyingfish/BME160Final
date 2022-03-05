from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from datetime import time
from graphHelp import dataGen

app = Flask(__name__)
datagen = dataGen()
@app.route("/")
def chart():
    '''s
    legend = 'Monthly Data'sbdd", "une", "July", "August"]n
    chartData = {"title": lekgjend,l "lah\ls":n laenls, "val": values}
    '''
    return render_template('home.html')

@app.route("/api")
def single_pH():
    chartData = {}
    if (request.method == "GET"):
        seqList = request.args.get("seqs").split(",")
        ph = request.args.get("ph")
        fragLen = request.args.get("fraglen")
        values = datagen.phs(seqList[0],pH=ph,l=fragLen)
        labels = [b*int(fragLen) for b in range(len(values))]
        title = "Charges at pH {}".format(str(ph))
        name = "Alkalihalobacillus pseudofirmus"
        #[10,25,17,21,30]xs
        chartData = {"title": title, "labels": labels, "val": values, "species": name}
    else:
        chartData = {"title": "oh no something iss wrong", "labels": ["err"], "val": [404]}
    return jsonify(chartData)
 
@app.route("/group")
def groupProt():
    chartData = {}
    if (request.method == "GET"):
        seqList = request.args.get("seqs").split(",")
        ph = request.args.get("ph")
        fragLen = request.args.get("fraglen")
        allPhs = [datagen.phs(sq,pH=ph,l=fragLen) for sq in seqList]
        x,y = datagen.pca(allPhs)
        x = [xx for xx in x]
        y = [yy for yy in y]
        datapoints = [{"x": float(x[i]), "y": float(y[i])} for i in range(len(x))]
        title = "Protein Clusters at pH {}".format(str(ph))
        name = "Group 1"
        labels = ["Alkalihalobacillus pseudofirmus","Alkalibacter_saccharofermentans","Halorhodospira halochloris","Helicobacter pylori","Escherichia coli","Vibrio alginolyticus","Acidiphilium cryptum","Acidithiobacillus ferrooxidans","Sulfobacillus acidophilus"]
        chartData = {"title": title, "labels": labels, "val": datapoints, "species": name}
    else:
        chartData = {"title": "oh no something iss wrong", "labels": ["err"], "val": [404]}
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