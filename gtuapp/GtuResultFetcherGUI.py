#THIS PROGRAM WON'T RUN WITHOUT URL AND HEADERS
#HEADERS CONTAINS API PRIVATE DATA AND HENCE HAS BEEN REDUCTED FOR PUBLIC DISPLAY



import requests
import json
from tkinter import *
import tkinter as tk
import webbrowser


gtuapp = Tk()
gtuapp.title("GTU Result Fetcher")
gtuapp.geometry('650x600')
gtuapp.resizable(width=False, height=False)

url = "URL REMOVED DUE TO PRIVACY RESAONS"
headers = {
    "HEADERS REMOVED DUE TO PRIVACY RESAONS"
}

#scrollbar = Scrollbar(gtuapp)
#scrollbar.pack(side = RIGHT, fill = Y )

tkvar = StringVar(gtuapp)
tkvar2 = StringVar(gtuapp)
tkvar3 = StringVar(gtuapp)
tkvar4 = StringVar(gtuapp)
tkvar5 = StringVar(gtuapp)


titlefont = ('times', 30, 'bold')
title = Label(gtuapp, text="GTU Result Fetcher",  )
title.config(font=titlefont)
title.place(x=150, y=30)

def getenrol():
    global enrol
    labelfont = (10)
    label = Label(gtuapp, text="Enrollment No : ")
    label.config(font=labelfont)
    label.place(x=150, y=130)

    enrol = tk.Entry(gtuapp)
    enrol.place(x=300, y=130, width=200, height=30)
getenrol()

def callback(submit):
    global finalexamid
    gexamid = values3.index(submit)
    finalexamid = output[gexamid]["examid"]

    MyButton = Button(gtuapp, text="Submit", width=10, command=getresult)
    MyButton.place(x=300,y=290)

def getresult():
    data1 = "ReqOperation=StudentResult&"
    data2 = "ExamID="
    global exami_d
    exami_d = finalexamid
    data3 = "&EnrNo="
    enroll = enrol.get()
    data4 = "&DeviceId=3cge4e8d88856309&OSversion=32&LatLong=0&MobileNo=&IMEI_NO=989549075873199&IPAddress=fe80%3A%3A7410%3A9cff%3Afed4%3Ab798%25dummy0"
    if kp == 0:
        data5 = "&IsCurrent=0"
    else:
        data5 = "&IsCurrent=1"
    finaldatababy = data1 + data2 + exami_d + data3 + enroll + data4 + data5
    print(finaldatababy)
    r = requests.post(url, headers=headers, data=finaldatababy)
    output = json.loads(r.content)

    if output[0]["RESULT"] == "PASS":
        color = "green"
    else:
        color = "red"

    label_frame = LabelFrame(gtuapp, text="GTU RESULT", bg="grey", fg="black", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    label_frame.pack(expand='yes', fill='both')

    global destroy
    destroy = Button(label_frame, text="Back", width=10, command=label_frame.destroy)
    destroy.place(x=0, y=0)

    name = Label(label_frame, text=output[0]["name"], bg="grey", fg="black", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    name.place(x=120, y=5)

    enrollment = Label(label_frame, text=output[0]["MAP_NUMBER"], bg="black", fg="white", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    enrollment.place(x=120, y=35)

    totalsubjects = output[0]["TOTSUBCOUNT"]
    sub = []
    subname=[]
    subgrade=[]

    for i in range(1, int(totalsubjects) + 1):
        i = str(i)
        sub.append(str(output[0]["SUB" + i]))
    for i in range(1, int(totalsubjects) + 1):
        i = str(i)
        subname.append(str(output[0]["SUB" + i + "NA"]))
    for i in range(1, int(totalsubjects) + 1):
        i = str(i)
        subgrade.append(str(output[0]["SUB" + i + "GR"]))

    labl0 = Label(label_frame, font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    labl0.config(text="Subject Code")
    labl0.place(x=75, y=90)
    subs = Label(label_frame, font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    subs.config(text=("\n".join(sub)))
    subs.place(x=90, y=130)

    labl = Label(label_frame, font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    labl.config(text="Subject Name")
    labl.place(x=235, y=90)
    subsname = Label(label_frame, font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    subsname.config(text=("\n".join(subname)))
    subsname.place(x=200, y=130)

    labl2 = Label(label_frame, font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    labl2.config(text="Subject Grade")
    labl2.place(x=400, y=90)
    subsgrade = Label(label_frame, font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    subsgrade.config(text=("\n".join(subgrade)))
    subsgrade.place(x=440, y=130)

    cpis = Label(label_frame, text="Your CPI is" + " " + output[0]["CPI"], bg="black", fg="white", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    cpis.place(x=300,y=320)

    spis = Label(label_frame, text="Result: " + output[0]["RESULT"], bg=color, fg="white", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    spis.place(x=300,y=360)


def getexamid(value):
    data1 = "ReqOperation=GetExamName&"
    data2 = "ExSession="
    session2 = session
    data3 = "&ExType="
    global course
    course = value
    finaldatababy = data1 + data2 + session2 + data3 + course
    r = requests.post(url, headers=headers, data=finaldatababy)
    global output
    output = json.loads(r.content)
    print(finaldatababy)
    global values3
    values3 = []
    for i in range(len(output)):
        values3.append(str(output[i]["exam"]))

    labelfont = (10)
    label = Label(gtuapp, text="Select Exam: ")
    label.config(font=labelfont)
    label.place(x=150, y=250)
    menu3 = OptionMenu(gtuapp, tkvar3, *values3, command=callback)
    menu3.place(x=300, y=250)


def getcourse(value):
    data1 = "ReqOperation=GetCourse&"
    data2 = "ExSession="
    global session
    session = value  # Change this
    finaldatababy = data1 + data2 + session
    r = requests.post(url, headers=headers, data=finaldatababy)
    output = json.loads(r.content)
    global kp
    kp = values.index(value)
    print(kp)
    values2 = []

    for i in range(len(output)):
        values2.append(str(output[i]["branchShort"]))

    print(finaldatababy)
    labelfont = (10)
    label = Label(gtuapp, text="Select Branch : ")
    label.config(font=labelfont)
    label.place(x=150, y=210)
    global menu2
    menu2 = OptionMenu(gtuapp, tkvar2, *values2, command=getexamid)
    menu2.place(x=300, y=210)


def getsession():
    data = "ReqOperation=GetSession"
    r = requests.post(url, headers=headers, data=data)
    global output
    output = json.loads(r.content)
    global values
    values = []

    for i in range(len(output)):
        values.append(str(output[i]["ExSession"]))

    labelfont = (10)
    label = Label(gtuapp, text="Select Year : ")
    label.config(font=labelfont)
    label.place(x=150,y=170)
    menu = OptionMenu(gtuapp, tkvar, *values, command=getcourse)
    #menu.config(width=20, height=1, text="Year")
    menu.place(x=300,y=170)


getsession()

def senti(url):
    webbrowser.open_new(url)
ref = Label(gtuapp, text="Sentinal920", fg="blue", cursor="hand2")
ref.place(x=290,y=570)
ref.bind("<Button-1>", lambda e: senti("https://sentinal920.github.io/"))

gtuapp.mainloop()
