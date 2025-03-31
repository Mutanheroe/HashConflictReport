# Written by Mutanheroe

import os
import argparse
from typing import List
import webbrowser
import magic

result = {}
folderHasMap = {}

def main():
    hashMap ={}
    parser = argparse.ArgumentParser(
        prog="Mod Hash Conflict Finder",
        description=('')
    )
    
    print("Mod Hash Conflict Finder") 
    parser.add_argument('ini_filepath', nargs='?', default=None, type=str)
    args = parser.parse_args()
    if args.ini_filepath:
        if args.ini_filepath.endswith('.ini'):
            print('Passed .ini file:', args.ini_filepath)
            hashMap = check_ini(args.ini_filepath,hashMap)
      
        else:
            print('Passed file is not an Ini')

    else:
        hashMap = process_folder('.',hashMap)

    drawbuda()
    mergeFileHash2()
    generateReport()

def process_folder(folder_path,hashMap):
    for filename in os.listdir(folder_path):
        if (not filename.upper().startswith('DISABLED') and not filename.upper().startswith('DESKTOP')):
            filepath = os.path.join(folder_path, filename)
            if os.path.isdir(filepath):
                hashMap = process_folder(filepath,hashMap)
            if filename.endswith('.ini'):
                print('Found .ini file at:', filepath)
                check_ini(filepath,hashMap)
    return hashMap

def check_ini(filepath,hashMap):
    content = ''
    enco = ''
    try:
        blob = open(filepath, 'rb').read()
        m = magic.Magic(mime_encoding=True)
        enco = m.from_buffer(blob) 

    except:    
        raise Exception('Unable to retrive encoding')

    try:
        content = open(filepath,encoding=enco)
    
    except UnicodeDecodeError:
        print ('error reading the file: ' +filepath + " encoding: "+ enco)

    
    counter = 0
    for line in content:
        linecontent  = line.split()
        
        for i in range(len(linecontent)):            
            if i+2<len(linecontent) and linecontent[i].rstrip('\n')=='hash' and linecontent[i+1].rstrip('\n')=='=' :
                hash = linecontent[i+2].rstrip('\n')
                hashMap = checkHash(hashMap,hash,filepath, counter,line)

        counter+=1
    content.close()

    return hashMap


def checkHash(hashMap,hash,filepath,lineNumber,line):
    absolutepath=os.path.abspath(filepath)
    iniName = filepath.split("\\")[1]
    if(hashMap.get(hash)==None):
        hashMap[hash] = {'hash':hash, 'lineNumber':[lineNumber], 'line':[line], 'filepath':[filepath], 'absolutepaht': [absolutepath], 'iniNames' :iniName}
    
    elif(hashMap[hash]!=None):
        sameFile = False
        for path in hashMap[hash]['filepath']:
            if(path ==filepath):
                sameFile= True                
                break
            
        
        if (not sameFile ):
            if setCheck(filepath,  hashMap[hash]['filepath']):
                hashMap[hash]['grade']=setGrade(filepath,  hashMap[hash]['filepath'])
                hashMap[hash]['lineNumber'].append(lineNumber)
                hashMap[hash]['line'].append(line)
                hashMap[hash]['filepath'].append(filepath)
                hashMap[hash]['absolutepaht'].append(absolutepath)
                hashMap[hash]['iniNames']+= ", "+iniName 
                if('sameMod' in hashMap[hash].keys()):
                     hashMap[hash]['sameMod'] = (hashMap[hash]['sameMod'] and isSameModFolder(hashMap[hash]['filepath'])) 
                else:
                    hashMap[hash]['sameMod'] = isSameModFolder(hashMap[hash]['filepath'])
                   
                result[hash] = hashMap[hash]
                result[hash]['hash'] = hash


                key =filepath.split("\\")[1]
                if( result[hash]['sameMod'] ==False):
                    if(folderHasMap.get(key)==None  ):
                         folderHasMap[key] =[result[hash]]
                    else:
                        folderHasMap[key].append(result[hash])
                
               
            



    return hashMap    

def mergeFileHash():



    
    sameFileKeys = []
    for key in folderHasMap.keys():
        if(key=='All LadyGirl NPC mod for ZenlessZoneZero'):
            print(folderHasMap[key])
        merged=[]  
        for e in folderHasMap[key]:
            found = e['sameMod'] 
            for i in merged:
                if i['hash'] == e['hash']:
                    found = True
                    break
                    
            if not found:
                merged.append(e) 
        paths =[]
        for element in merged:
            paths.append(element['filepath'])
        
        if(isSameModFolderMatrix(paths)):
            sameFileKeys.append(key)
            #folderHasMap.pop(key)
        else:    
            folderHasMap[key] = merged

    for e in sameFileKeys:
        folderHasMap.pop(e)
    

def mergeFileHash2():
    popPila = []
    for key in folderHasMap.keys():
        for element in folderHasMap[key]:
            if(element['sameMod'] ):
                folderHasMap[key].remove(element)
        if len(folderHasMap[key])==0:
            popPila.append(key)

    for e in popPila:
        folderHasMap.pop(e) 


def setGrade(filepath,posibleMatchs):
    res =  []
    splitedFilePath1 =  filepath.split("\\")
    splitedFilePath1 .pop()
    maxLength = 1;   
    for path in posibleMatchs:
        dif = 0 
        splitedFilePath2 =  path.split("\\")
        splitedFilePath2.pop()
        if(len(splitedFilePath2)>len(splitedFilePath1)):
            q = splitedFilePath1
            splitedFilePath1 =splitedFilePath2
            splitedFilePath2 = q
        if  len(splitedFilePath2) >maxLength:
            maxLength = len(splitedFilePath2)
        
        for q in  splitedFilePath1:
            if q not in splitedFilePath2:
                dif+=1
        res.append(dif)

        res.sort()

    return (100*res[-1])/maxLength

def setCheck(filepath,posibleMatchs):
    path1 = getPathWithoutFileName(filepath)
    for path in posibleMatchs:
        path2 = getPathWithoutFileName(path)
        if(path1 in path2):
            continue
        elif(path2 in path1):    
            continue
        else:
            return True    
    return False

def getPathWithoutFileName(path):
    res = ""
    splitedPath = path.split("\\")
    splitedPath.pop()
    for  e in splitedPath:
        res+=e
    return res
             
def isSameModFolder(filepaths):
    fileNames = {}
    for path in filepaths:
        fileNames[path.split("\\")[1]] = None

    return 1 == len(fileNames.keys())



def isSameModFolderMatrix(paths):
    fileNames = {}
    for path in paths:
        for e in path:
            fileNames[e.split("\\")[1]] = None
    return 1 == len (fileNames.keys())

def pause():
   input('Press Enter to close')


def drawbuda():
    print()
    print()
    print("                       _oo0oo_") 
    print("                      o8888888o")
    print("                      8`' . `'8")
    print("                      (| -_- |)")
    print("                      0|  =  |0")
    print("                    ___|`----'|___")
    print("                  .'  |     |  '.")
    print("                 |  |||  :  |||||  ")
    print("                | _||||| -:- |||||- ||")
    print("               |   | |||  -  ||| |   |")
    print("               | |_|  ''|---|''  |_| |")
    print("               |  .-|__  '-'  ___|-. |")
    print("             ___'. .'  |--.--|  `. .'___")
    print("          .`  '<  `.___|_<|>_|___.' >' `.")
    print("         | | :  `- |`.;`| _ |`;.`| - ` : | |")
    print("         |  | `_.   |_ __| |__ _|   .-` |  |")
    print("     =====`-.____`.___ |_____|___.-`___.-'=====")
    print("                       `=---='")
    print()
    print()


def generateReport():
    #print(result)
    #for key in result.keys():
    #    print ("Hash: "+ key+ " found in")
    #    for ocurrence in range(len(result[key]['line'])):
    #        print ( result[key]['filepath'][ocurrence]+ " at line: " + str(result[key]['lineNumber'][ocurrence]) + "  "+ result[key]['line'][ocurrence])
    


    with open("HashConflictReport.html", 'w', encoding="utf-8") as report:
            if(len(result.keys())>0):
                report.write(getHeader(len(result.keys())))

               
                
                report.write(fileSearchPanel())
                orderedItems = orderItems(result)
                report.write(exaustiveSearchPanel(orderedItems))
            
                report.write(getBottom())        
            else:
                report.write(emptyResults())
            report.flush()



    webbrowser.open('file://' + os.path.realpath("HashConflictReport.html"))      

def fileSearchPanel():
    html_template = """<div class="card-body"> <ul class="list-group">"""
    count =1
    for key in folderHasMap:
       # if(len(folderHasMap[key])>1):
       id = str(count)+"id"
       html_template += generateHTMLListElementFiles(folderHasMap[key],key,id) 
       count+=1
    html_template += """</ul></div>"""
    return html_template

def exaustiveSearchPanel (orderedItems):
    html_template = """<br><h3>Hash List</h3><div class="card-body"> <ul class="list-group">""" 
    for key in orderedItems:
        html_template += generateHTMLListElement(result[key['hash']],key['hash'],str(0)) 
    html_template += """</ul></div>"""
    return html_template

def orderItems(items):
    res =[]
    for key in result.keys():
        result[key]['hash'] = key
        res.append(result[key])
    res.sort(reverse=True,key=order)
    return res

def order(res):
    return res['grade']

def getIconCheck(check):
    html_template =""
    if(check):
        html_template ="""<i class="material-icons">warning</i>"""
    
    return html_template

def getListGroup(grade):
    if grade < 25:
        return  """color: AliceBlue;"""
    if grade < 50:
        return  """color: GreenYellow;</i>"""
    else:
        return  """color: IndianRed;</i>"""

def generateHTMLListElementFiles(element,hash,id):
    html_template =  """<li  class="list-group-item d-flex justify-content-between align-items-center" >
    <div id="accordion"""+id+"""">
    Mod: <button class="btn btn-link" data-toggle="collapse" data-target="#"""+id+"""" aria-expanded="false" aria-controls="collapseOne"> """+ hash+"""</button> 
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

def generateHTMLListElement(element,hash,stamp):
    if len(element['iniNames']) > 50:
        element['iniNames'] = element['iniNames'][:50]+"..."
    html_template = """  <li  class="list-group-item d-flex justify-content-between align-items-center" ><div id="accordion"""+hash+stamp+"""">
            
                    
                       Hash:<button class="btn btn-link" data-toggle="collapse" data-target="#"""+hash+stamp+"""" aria-expanded="false" aria-controls="collapseOne"> """+ hash+"""</button> """+element['iniNames']+""" : """+str(len(element['lineNumber']))+""" elements
                    
                <div id="""+hash+stamp+""" aria-labelledby="headingOne" class="accordion-body collapse" data-parent="#accordion"""+hash+stamp+"""" >
                <div class="card-body">
                    <ul class="list-group">"""
    

    
    for ocurrence in range(len(element['line'])):
        html_template += """ <li class="list-group-item fs-6"> Found at line number """+ str(element['lineNumber'][ocurrence]+1)+""": <a href="file:///"""+ element['absolutepaht'][ocurrence]+"""">"""+ element['filepath'][ocurrence]+"""</a></li>"""

    html_template +="</ul></div></div></li>"
    #html_template +="""</button>"""
    return html_template

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


def getHeader(matches):
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
    <p>The process has found """+str(matches)+""" hash.</p>
    <p>This hashes appear on different files, this is not forced a conflict if they are intentionally set by moders or users</p>
    <h3>Mod List</h3>


    
     
  
    """
    return html_template

def getBottom():
    html_template = """ 
    
    </div>
    </div>
    </body> 
    </html> 
    """
    return html_template

main()
pause()
#python -m PyInstaller  --onefile  ModConflictFinder.py   

