# importing the required libraries
from flask import Flask, render_template, jsonify, request
from datetime import time
from werkzeug.utils import secure_filename
from graphHelp import DataGen, FastAreader
from graphHelp import ml
import shutil
import random
import os
import numpy as np
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='(<<',
    variable_end_string='>>)',
    comment_start_string='(#',
    comment_end_string='#)',
  ))
app = CustomFlask(__name__) #avoid JavaScript interference
datagen = DataGen()
mL = ml()
currentData = {
    "species":  ["Alkalihalobacillus pseudofirmus","Alkalibacter_saccharofermentans","Halorhodospira halochloris","Helicobacter pylori","Escherichia coli","Vibrio alginolyticus","Acidiphilium cryptum","Acidithiobacillus ferrooxidans","Sulfobacillus acidophilus"],
    "seqs": ["MSIKPEEISSLIKQQIESFQSDVQVQDVGTVIR", "VAAADVGTVPEMSIKLIKQQIESFQSDEISSIR", "YLHSRLLERAAKMSDEFGAGSLTALPVIE","PIGRGQRELIIGDRQIGKTALAIDAIINQKDSGIFSIYVA", "ALAIDAIAVVADVGKTVMEFGAGPEM", "MSLIKQALAIDSAKPEMISAIINQKDSGIFS", "IGDRQIGKTALAIDAIINQKDSGIMPP", "KDSGIFIYVASIYVAKDSGIFSVVADVGK", "VASIYVAIGRGQRELIIKQQIESFQSDES"]
}
# Creating the upload folder
upload_folder = "uploads/"
if os.listdir(upload_folder): #check if folder empty
    shutil.rmtree(upload_folder)
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

@app.route("/", methods = ['GET', 'POST'])
def chart():
    if request.method == 'POST': # check if the method is post
        print(request.data)
        f = request.files["file"] # get the file from the files object
        fname = os.path.join("uploads/",secure_filename(f.filename))
        f.save(fname) # this will secure the file
        reader = FastAreader(fname)
        
        speciesList = []
        seqList = []
        for head, seq in reader.readFasta():
            speciesList.append(head)
            seqList.append(''.join([i for i in seq if i.isalpha()]))
        currentData["species"] = speciesList
        currentData["seqs"] = seqList
        
        formObj = {"message": 'file uploaded successfully'}
        return render_template('home.html', form=formObj)# Display this message after uploading
    else:
        formObj = {"message": "upload file"}
        return render_template('home.html', form=formObj)

@app.route("/api")
def single_pH():
    chartData = {}
    if (request.method == "GET"):
        seqList = currentData["seqs"]
        ph = request.args.get("ph")
        fragLen = request.args.get("fraglen")
        values = [datagen.phs(seqList[i],pH=ph,l=fragLen) for i in range(len(seqList))]
        valueLens = [len(v) for v in values]
        labels = [b*int(fragLen) for b in range(max(valueLens))]
        title = "Charges at pH {}".format(str(ph))
        species = currentData["species"]
        colors = datagen.colors(len(species))
        chartData = {"title": title, "labels": labels, "val": values, "species": species, "colors": colors}
    else:
        chartData = {"title": "oh no something iss wrong", "labels": ["err"], "val": [404]}
    return jsonify(chartData)
 
@app.route("/group")
def groupProt():
    chartData = {}
    if (request.method == "GET"):
        seqList = currentData["seqs"]
        ph = request.args.get("ph")
        fragLen = request.args.get("fraglen")
        clusterNum = request.args.get("num")
        labels = currentData["species"]
        '''
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
        '''
        allPhs = [datagen.phs(sq,pH=ph,l=fragLen) for sq in seqList]
        
        x,y,points = datagen.pca(allPhs)
        x = [xx for xx in x]
        y = [yy for yy in y]
        groupLabels = []
        clusters = mL.getClusters(points, int(clusterNum))
        datapoints = []
        for it in range(int(clusterNum)):
            curPoints = [{"x": float(x[i]), "y": float(y[i])} for i in range(len(x)) if clusters[i] == int(it)]
            thisLabels = [labels[i] for i in range(len(x)) if clusters[i] == int(it)]
            datapoints.append(curPoints)
            groupLabels.append(thisLabels)
        title = "Protein Clusters at pH {}".format(str(ph))
        colors = datagen.colors(int(clusterNum))
        groups = ["Group"+str(i+1) for i in range(int(clusterNum))]
        chartData = {"title": title, "labels": groupLabels, "val": datapoints, "groups": groups, "colors": colors}
    else:
        chartData = {"title": "oh no something iss wrong", "labels": ["err"], "val": [404]}
    return jsonify(chartData)    
   
@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
    if request.method == 'POST': # check if the method is post
        print(request.data)
        f = request.files["file"] # get the file from the files object
        f.save(os.path.join("uploads/",secure_filename(f.filename))) # this will secure the file
        message = {"message": 'file uploaded successfully'}
        return jsonify(message)# Display this message after uploading
    
if __name__ == "__main__":
    app.run(debug=True)