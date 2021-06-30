import requests
import uuid
import numpy as np
import re
from bs4 import BeautifulSoup
f = open("Index.html", "r")
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
    elem=soup.find_all(attrs={"data-asgar-id" : id})[0]
    del elem["data-asgar-id"]
    if(elem is not None):
        textForCheck=str(elem.string).strip()
        text=str(elem.string).strip().lower().replace(" ", "_")
        text=re.sub(r'\W+', '', text)
        length=len(text)
        if length!=0 and ("{{" not in textForCheck or "}}" not in textForCheck) and not elem.has_attr('dontranslate'):
            elem.string=mainConvert(text)
            transed=translate(textForCheck)
            enJson[text]=textForCheck
            azJson[text]=translate(transed)
removeDataIds()
print(enJson)
print(azJson)
