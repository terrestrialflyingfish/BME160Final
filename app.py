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

#this dictionary holds the current FASTA file species and sequences
#below is default values
currentData = {
    "species":  ["Alkalihalobacillus pseudofirmus","Alkalibacter_saccharofermentans","Halorhodospira halochloris","Helicobacter pylori","Escherichia coli","Vibrio alginolyticus","Acidiphilium cryptum","Acidithiobacillus ferrooxidans","Sulfobacillus acidophilus"],
    "seqs": ["MSIKPEEISSLIKQQIESFQSDVQVQDVGTVIR", "VAAADVGTVPEMSIKLIKQQIESFQSDEISSIR", "YLHSRLLERAAKMSDEFGAGSLTALPVIE","PIGRGQRELIIGDRQIGKTALAIDAIINQKDSGIFSIYVA", "ALAIDAIAVVADVGKTVMEFGAGPEM", "MSLIKQALAIDSAKPEMISAIINQKDSGIFS", "IGDRQIGKTALAIDAIINQKDSGIMPP", "KDSGIFIYVASIYVAKDSGIFSVVADVGK", "VASIYVAIGRGQRELIIKQQIESFQSDES"]
}

# Creating the upload folder
upload_folder = "uploads/"
if os.listdir(upload_folder): #clear uploads folder on when app restarts
    shutil.rmtree(upload_folder)
if not os.path.exists(upload_folder): #make uploads folder if it doesn't exist yet
    os.mkdir(upload_folder)

@app.route("/", methods = ['GET', 'POST'])
#returns homepage and handles uploads
def upload():
    if request.method == 'POST': # check if the method is post
 
        #get uploaded Fasta file
        f = request.files["file-upload"] # get the file from the files object
        fname = os.path.join("uploads/",secure_filename(f.filename))
        f.save(fname) 
        
        #read uploaded FastA file
        reader = FastAreader(fname)
        
        #change currentData based on contents of uploaded Fasta file
        speciesList = []
        seqList = []
        for head, seq in reader.readFasta():
            speciesList.append(head)
            seqList.append(''.join([i for i in seq if i.isalpha()]))
        currentData["species"] = speciesList
        currentData["seqs"] = seqList
        
        formObj = {"message": 'file uploaded successfully'}
        return render_template('home.html', form=formObj)# reload page
    else:
        #render page 
        formObj = {"message": "upload file"}
        return render_template('home.html', form=formObj)

@app.route("/api")
def getpHGraphs():
    chartData = {}
    if (request.method == "GET"):
        seqList = currentData["seqs"]
        ph = request.args.get("ph") #pH to calculate charge values for
        fragLen = request.args.get("fraglen")
        
        #generate graph data
        datasets = [datagen.phs(seqList[i],pH=ph,l=fragLen) for i in range(len(seqList))] #get charges of protein 
        
        # x values for line graph
        datasetLens = [len(dataset) for dataset in datasets]
        labels = [b*int(fragLen) for b in range(max(datasetLens))] #scale x-axis to the longest sequence in the dataset
        
        title = "Charges at pH {}".format(str(ph))
        species = currentData["species"]
        colors = datagen.colors(len(species)) #generate colors for each line on the graph
        chartData = {"title": title, "labels": labels, "val": datasets, "species": species, "colors": colors}
    else:
        chartData = {"title": "oh no something is wrong", "labels": ["err"], "val": [404]}
    return jsonify(chartData)
 
@app.route("/group")
def groupProt():
    chartData = {}
    if (request.method == "GET"):
        seqList = currentData["seqs"] #get current sequences
        ph = request.args.get("ph")
        fragLen = request.args.get("fraglen") 
        clusterNum = request.args.get("num")#this is a string, for some reason I can't put int around this here because it returns an error
        species = currentData["species"]
   
        #get pH vectors 
        allPhs = [datagen.phs(sq,pH=ph,l=fragLen) for sq in seqList]
        
        #turn vectors into points with coordinates based on how similar they are to each other
        x,y,points = datagen.pca(allPhs)
        x = [xx for xx in x]
        y = [yy for yy in y]
        groupsSpecies = []
        clusters = mL.getClusters(points, int(clusterNum))
        datasets = []
        
        #create separate dataset for each group
        for it in range(int(clusterNum)):
            #have to convert to float because of some numpy shenanigans
            dataset = [{"x": float(x[i]), "y": float(y[i])} for i in range(len(x)) if clusters[i] == it]
            
            #get the species that fall into this group or cluster
            datasets.append(dataset)
            
            #get the names of each species in this group
            thisGroupSpecies = [species[i] for i in range(len(x)) if clusters[i] == it]
            groupsSpecies.append(thisGroupSpecies)
            
        #title for graph
        title = "Protein Clusters at pH {}".format(str(ph))
        
        colors = datagen.colors(int(clusterNum)) #generate colors for each clustter on the graph
        groups = ["Group"+str(i+1) for i in range(int(clusterNum))] #create group names
        chartData = {"title": title, "labels": groupsSpecies, "val": datasets, "groups": groups, "colors": colors}
    else:
        #if some error happens
        chartData = {"title": "oh no something is wrong", "labels": ["err"], "val": [404]}
    return jsonify(chartData) #send to webpage   

if __name__ == "__main__":
    app.run(debug=True)