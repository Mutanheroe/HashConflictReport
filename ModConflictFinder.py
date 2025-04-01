# Written by Mutanheroe

import os
import argparse
import magic
import ReportGenerator as rg
from GlobalVariables import  *  



#Main
def main(rg):
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
    rg.generateReport()

#Recursive search
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

#Open File
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
    modName=  filepath.split("\\")[1]
    for line in content:
        linecontent  = line.split()
        for i in range(len(linecontent)):            
            if i+2<len(linecontent) and linecontent[i].rstrip('\n')=='hash' and linecontent[i+1].rstrip('\n')=='=' :
                hash = linecontent[i+2].rstrip('\n')
                hashMap = checkHash(hashMap,hash,filepath, counter,line)
        if(len(linecontent)>0):
            setModInfo(linecontent,modName)
        counter+=1    
    content.close()
   

    return hashMap

#Extract Mod Info
def setModInfo(linecontent,modName):
    
    toggels = []
    if (linecontent[0] =="key" ):
        toggels.append(linecontent)
    pushModInfo(modName, toggels)     

#Insert Mod Info
def  pushModInfo(name, toggels) :
    extractedToggels = []
    for t in toggels:
        toggel =""
        keySet = False
        remove = ["key","KEY","=","alt","ALT","ctrl","CTRL","shift","SHIFT","up","UP","VK_UP","down","DOWN","VK_DOWN" ,"right","RIGHT","VK_RIGHT","left","LEFT","VK_LEFT", "no_alt", "NO_ALT", "no_shif", "NO_SHIFT", "no_ctrl", "NO_CTRL"]
        if("alt" in t or "ALT" in t):
            toggel+= "alt " 
        if("ctrl" in t or "CTRL" in t):
            toggel+= "control " 
        if("shift" in t or "SHIFT" in t):
            toggel+= "shift " 
        if("up" in t or "UP" in t or "VK_UP" in t ):
            toggel+= "up " 
            keySet = True
        if("down" in t or "DOWN" in t or "VK_DOWN" in t ):
            toggel+= "down "
            keySet = True
        if("right" in t or "RIGHT" in t or "VK_RIGHT" in t ):
            toggel+= "right "
            keySet = True
        if("left" in t or "LEFT" in t or "VK_LEFT" in t ):
            toggel+= "left "
            keySet = True
       
        result = [e for e in t if e not in remove]    
       
        if(len(result)==1):
           toggel+=result[0] 
           keySet = True     
        if(keySet):
            extractedToggels.append(toggel) 

       
    if not name in modInfoHashMap.keys():
        modInfoHashMap[name] = {'toggels':[]}


    if(len(extractedToggels) >0):
        for e in extractedToggels:
           if not e in modInfoHashMap[name]['toggels']:
               modInfoHashMap[name]['toggels'].append(e) 
            
    

#Extract Hash Info
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
                    if(folderHashMap.get(key)==None  ):
                         folderHashMap[key] =[result[hash]]
                    else:
                        folderHashMap[key].append(result[hash])
                
               
            



    return hashMap    

#Sort Info
def mergeFileHash2():
    popPila = []
    for key in folderHashMap.keys():
        for element in folderHashMap[key]:
            if(element['sameMod'] ):
                folderHashMap[key].remove(element)
        if len(folderHashMap[key])==0:
            popPila.append(key)

    for e in popPila:
        folderHashMap.pop(e) 

#Sort Info
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

#Setter
def getPathWithoutFileName(path):
    res = ""
    splitedPath = path.split("\\")
    splitedPath.pop()
    for  e in splitedPath:
        res+=e
    return res

#Return if an array of filepath shares the same root             
def isSameModFolder(filepaths):
    fileNames = {}
    for path in filepaths:
        fileNames[path.split("\\")[1]] = None

    return 1 == len(fileNames.keys())


#Return if a matrix of filepath shares the same root
def isSameModFolderMatrix(paths):
    fileNames = {}
    for path in paths:
        for e in path:
            fileNames[e.split("\\")[1]] = None
    return 1 == len (fileNames.keys())

#Pause
def pause():
   input('Press Enter to close')

#Buda
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






#pause()
#python -m PyInstaller  --onefile  ModConflictFinder.py   

