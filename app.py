from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from datetime import time
from graphHelp import DataGen
from graphHelp import ml
import random
import numpy as np
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))',
    comment_start_string='(#',
    comment_end_string='#)',
  ))
app = CustomFlask(__name__)
datagen = DataGen()
mL = ml()
@app.route("/")
def chart():
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
        labels = ["Alkalihalobacillus pseudofirmus","Alkalibacter_saccharofermentans","Halorhodospira halochloris","Helicobacter pylori","Escherichia coli","Vibrio alginolyticus","Acidiphilium cryptum","Acidithiobacillus ferrooxidans","Sulfobacillus acidophilus"]

        for zz in range(100):
            tesList = list(seqList[int(np.floor(zz/5))])
            tesList[zz+zz:zz+zz+16] = list(seqList[int(np.floor(zz/4))])[zz+zz:zz+zz+16]
            asdf = list(seqList[int(np.floor(zz/6))])[zz+zz+38:zz+zz+60]
            random.shuffle(asdf)
            tesList[zz+zz+38:zz+zz+60] = asdf
            tesList[zz+zz+100:zz+zz+134] = list(seqList[int(np.floor(zz/3.5))])[zz+zz+100:zz+zz+134]
            tesList[zz+zz+200:zz+zz+234] = list(seqList[int(np.floor(zz+2/5.5))])[zz+zz+200:zz+zz+234]
            seqList.append(''.join(tesList))
            labels.append("test"+str(zz))
        allPhs = [datagen.phs(sq,pH=ph,l=fragLen) for sq in seqList]
        
        x,y,points = datagen.pca(allPhs)
        x = [xx for xx in x]
        y = [yy for yy in y]
        groupLabels = []
        clusters = mL.getClusters(points, 3)
        datapoints = []
        for it in range(3):
            curPoints = [{"x": float(x[i]), "y": float(y[i])} for i in range(len(x)) if clusters[i] == int(it)]
            thisLabels = [labels[i] for i in range(len(x)) if clusters[i] == int(it)]
            datapoints.append(curPoints)
            groupLabels.append(thisLabels)
        title = "Protein Clusters at pH {}".format(str(ph))
        colors = datagen.colors(3)
        groups = ["Group1","Group2","Group3","Group4","Group5"]
        chartData = {"title": title, "labels": groupLabels, "val": datapoints, "groups": groups, "colors": colors}
    else:
        chartData = {"title": "oh no something iss wrong", "labels": ["err"], "val": [404]}
    return jsonify(chartData)    
   