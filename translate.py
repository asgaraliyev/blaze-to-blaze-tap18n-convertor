import json
import os
import requests
import uuid
import numpy as np
import re
import codecs
from bs4 import BeautifulSoup, Comment
azJsonFileName="az.i18n.json"
enJsonFileName="en.i18n.json"
resutlFileName="result.html"
f = codecs.open("translate.html", "r")
html=f.read()
soup = BeautifulSoup(html, 'html.parser')
elements=["a",
"abbr",
"acronym",
"address",
"applet",
"area",
"article",
"aside",
"audio",
"b",
"base",
"basefont",
"bdi",
"bdo",
"bgsound",
"big",
"blink",
"blockquote",
"body",
"br",
"button",
"canvas",
"caption",
"center",
"cite",
"code",
"col",
"colgroup",
"content",
"data",
"datalist",
"dd",
"decorator",
"del",
"details",
"dfn",
"dir",
"div",
"dl",
"dt",
"element",
"em",
"embed",
"fieldset",
"figcaption",
"figure",
"font",
"footer",
"form",
"frame",
"frameset",
"h1",
"h2",
"h3",
"h4",
"h5",
"h6",
"head",
"header",
"hgroup",
"hr",
"html",
"i",
"input",
"ins",
"isindex",
"kbd",
"keygen",
"label",
"legend",
"li",
"link",
"listing",
"main",
"map",
"mark",
"marquee",
"menu",
"menuitem",
"meta",
"meter",
"nav",
"nobr",
"noframes",
"object",
"ol",
"optgroup",
"option",
"output",
"p",
"param",
"plaintext",
"pre",
"progress",
"q",
"rp",
"rt",
"ruby",
"s",
"samp",
"section",
"select",
"shadow",
"small",
"source",
"spacer",
"span",
"strike",
"strong",
"sub",
"summary",
"sup",
"table",
"tbody",
"td",
"template",
"textarea",
"tfoot",
"th",
"thead",
"time",
"title",
"tr",
"track",
"tt",
"u",
"ul",
"var",
"video",
"wbr",
"xmp"]
def readJson(fileName):
    with open("i18n/"+fileName) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
        return jsonObject

def editJson(fileName,data):
    with open("i18n/"+fileName, 'w',) as f:
        json.dump(data, f,ensure_ascii=False)  
def updateJson(fileName,data):
    obj=readJson(fileName)
    keys=data.keys()
    for key in keys:
        obj[key]=data[key]
    editJson(fileName, obj)
def editFile(fileName,text):
    try:
        # os.remove("i18n/"+fileName)
        f = open(f"i18n/"+fileName, "w")
        f.write(text)
        f.close()
    except:
        print("something went wrong 193")

apiUrl = 'http://localhost:4000/?q={}&from={}&to={}'
def translate(text):
    try:
        response=requests.get(apiUrl.format(text,"en","az"))
        return response.json()["text"]
    except:
        print("sea")
def mainConvert(string):
    return "{{"+"""_ '{}'""".format(string)+"}}"
def removeDataIds():
    allElements=soup.find_all()
    for el in allElements:
        del el["data-asgar-id"]
allElements=[]
for element in elements:
    els=soup.find_all(element)
    for i in els:
        i["data-asgar-id"]=uuid.uuid1()
        allElements.append(i)
dataIds=[]
for i in allElements:
    stringOfElement=i.string
    if(stringOfElement is not None):
        dataIds.append(i["data-asgar-id"])
azJson={}
enJson={}
for id in dataIds:
    try:
        elem=soup.find_all(attrs={"data-asgar-id" : id})[0]
        del elem["data-asgar-id"]
        if(elem is not None):
            textForCheck=str(elem.string).strip()
            text=str(elem.string).strip().lower().replace(" ", "_")
            text=re.sub(r'\W+', '', text)
            length=len(text)
            if length!=0 and (">" not in textForCheck and "{{" not in textForCheck and "}}" not in textForCheck) and not elem.has_attr('dontranslate'):
                print(elem,textForCheck,"{{" not in textForCheck )
                elem.string=mainConvert(text)
                transed=translate(textForCheck)
                enJson[text]=textForCheck
                azJson[text]=translate(transed)
    except:
        print("something went wrong 210")
updateJson(enJsonFileName, enJson)
updateJson(azJsonFileName, azJson)
removeDataIds()
editFile(resutlFileName, str(soup.prettify()).replace("&gt;", ">"))
