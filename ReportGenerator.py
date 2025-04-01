# Written by Mutanheroe

import webbrowser
import os
from GlobalVariables import  * 

def generateReport():
    print(modInfoHashMap)
    print(result)
    print(folderHashMap)
    with open("HashConflictReport.html", 'w', encoding="utf-8") as report:
        if(len(result.keys())>0):
            report.write(getHeader())
            report.write(fileSearchPanel())
            orderedItems = orderItems()
            report.write(exaustiveSearchPanel(orderedItems))
            report.write(getBottom())        
        else:
            report.write(emptyResults())
        report.flush()
    report.close()     
    webbrowser.open('file://' + os.path.realpath("HashConflictReport.html")) 

#Sort
def orderItems():
    res =[]
    for key in result.keys():
        result[key]['hash'] = key
        res.append(result[key])
    res.sort(reverse=True,key=order)
    return res

#Sort2
def order(res):
    return res['grade']



#Mod Conflict Panel
def fileSearchPanel():
    html_template = """<div class="card-body" id="ModConflict" style="display:none "><h3>Mod Conflict</h3> <ul class="list-group">
    <p>This hashes appear on different files, this is not forced a conflict if they are intentionally set by moders or users</p>
    """
    count =1
    for key in folderHashMap:
       id = str(count)+"id"
       html_template += generateHTMLListElementFiles(folderHashMap[key],key,id) 
       count+=1
    html_template += """</ul></div>"""
    return html_template

#Hash Conflict Panel
def exaustiveSearchPanel (orderedItems):
    html_template = """<div class="card-body" id="HashList" style="display:none " ><h3>Hash List</h3><p>The process has found """+str(len(result.keys()))+""" hash, but only show the ones that appear in different files.</p> <ul class="list-group">""" 
    for key in orderedItems:
        html_template += generateHTMLListElement(result[key['hash']],key['hash'],str(0)) 
    html_template += """</ul></div>"""
    return html_template


#HTML Code for 1 item of mod conflict panel
def generateHTMLListElementFiles(element,hash,id):
    html_template =  """<li  class="list-group-item d-flex justify-content-between align-items-center" >
    <div id="accordion"""+id+"""">
    Mod: <button class="btn btn-link" data-toggle="collapse" data-target="#"""+id+"""" aria-expanded="false" aria-controls="collapseOne" type="button"> """+ hash+"""</button> 
    <div id="""+id+""" aria-labelledby="headingOne" class="accordion-body collapse" data-parent="#accordion"""+id+"""" >
    <div class="card-body">
    <ul class="list-group">"""
    html_template +="""<div class="card-body"> <ul class="list-group">"""
    
    count = 1
    for ocurrence in element:
       # if count ==1:
        #    print(ocurrence)
        html_template += generateHTMLListElement(ocurrence,ocurrence['hash'],str(id)+str(count)) 
        count+=1
    html_template += """</ul></div>"""                   
    html_template +="</ul></div></div></div></li>"                   
    return  html_template

#HTML Code for 1 item of hash conflict panel
def generateHTMLListElement(element,hash,stamp):
    if len(element['iniNames']) > 50:
        element['iniNames'] = element['iniNames'][:50]+"..."
    html_template = """  <li  class="list-group-item d-flex justify-content-between align-items-center" ><div id="accordion"""+hash+stamp+"""">
            
                    
                       Hash: <button class="btn btn-link" data-toggle="collapse" data-target="#"""+hash+stamp+"""" aria-expanded="false" aria-controls="collapseOne" type="button"> """+ hash+"""</button> """+element['iniNames']+""" : """+str(len(element['lineNumber']))+""" elements
                    
                <div id="""+hash+stamp+""" aria-labelledby="headingOne" class="accordion-body collapse" data-parent="#accordion"""+hash+stamp+"""" >
                <div class="card-body">
                    <ul class="list-group">"""
    

    
    for ocurrence in range(len(element['line'])):
        html_template += """ <li class="list-group-item fs-6"> Found at line number """+ str(element['lineNumber'][ocurrence])+""": <a href="file:///"""+ element['absolutepaht'][ocurrence]+"""">"""+ element['filepath'][ocurrence]+"""</a></li>"""

    html_template +="</ul></div></div></li>"
    return html_template

#HTML Code for no results (Need to fix)
def emptyResults():
    html_template = """<!DOCTYPE html> 
    <html lang="en">
    <head> 
    
    <title>Hash Conflict Report</title> 
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    </head> 
    <body> 
    <div class="container">
    <h2>Hash Conflict Report</h2>

    <p>Congratulations, the process has not found any conflict</p>
    </div>
    </body> 
    </html> 
    """
    return html_template

#HTML Code for header
def getHeader():
    html_template = """<!DOCTYPE html> 
    <html lang="en">
    <head> 
    <title>Hash Conflict Report</title> 
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
   
    <style>
  
    </style>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  
    
    </head> 
    <body> 
    <div class="container">
    
    <h2>Hash Conflict Report</h2>
    
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    

    <button id="ModInfoButton" class="btn btn-primary" type="button"   aria-expanded="false" aria-label="Toggle navigation"">Mod Info
    </button>

    <button id="ModConflictButton" class="btn btn-primary" type="button"  aria-expanded="false" aria-label="Toggle navigation" ">Mod Conflict
    </button>


    <button  id="HashListButton" class="btn btn-primary" type="button"   aria-expanded="false" aria-label="Toggle navigation" ">Hash List
    </button>
    
    </nav>
     
  
    """
    return html_template

#HTML Code for end
def getBottom():
    html_template = """ 
    <a href="https://github.com/Mutanheroe/HashConflictReport">Project Source Code</a>
    </div>
    </div>
   
    
    """+getJQueryScripts()+"""
    </body> 
    </html> 
    """
    return html_template

def getJQueryScripts():
    html_template = """ <script>
    $("#ModInfoButton").on("click", function() {
      $("#ModInfo").show()
      $("#ModConflict").hide()
      $("#HashList").hide()
    });
     $("#ModConflictButton").on("click", function() {
      $("#ModConflict").show()
      $("#ModInfo").hide()
      $("#HashList").hide()
    });
     $("#HashListButton").on("click", function() {
      $("#HashList").show()
      $("#ModInfo").hide()
      $("#ModConflict").hide()
    });


    </script>"""
    return html_template


