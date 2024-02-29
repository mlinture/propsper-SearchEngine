from flask import Flask, render_template, request
import query
import summary
from bs4 import BeautifulSoup

app = Flask(__name__)

queryList = []
queryInput = ""
timer = 0
summaryList = []


@app.route('/', methods =["GET", "POST"])
def index():
    global queryInput
    global queryList
    global timer
    global summaryList
    if request.method == "POST":
       # getting input with name = fname in HTML form
        try:
            queryInput = request.form.get("queryInput")
            queryList = query.search(queryInput)
            print(queryList)
            if len(queryList) == 0:
                queryList.append("No Results Found for the Given Query!")
                return render_template('index.html', queryInput = queryInput, queryList=queryList,timer=0.0)

            timer = query.getTime()
            timer = round(timer*100,4)
            summaryList = []
            
            print(len(queryList))
            #title = soup.find("meta", property="og:title")
            # print(queryList)
            for i in queryList:
                # print('ham')
                print(i)
                # print(queryList[i])
                sum=summary.generate_openai_summary(i)
                sum+="..."
                summaryList.append(sum)
                print("Summary: ",sum,'\n')
            
        except: 
            pass
        
   
    return render_template('index.html', queryInput = queryInput, queryList=queryList,timer=timer,summaryList=summaryList)
    #return render_template('index.html', queryInput = queryInput, queryList=queryList,timer=timer,summaryList=summaryList)

