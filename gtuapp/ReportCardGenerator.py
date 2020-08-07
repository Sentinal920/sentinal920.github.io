#THIS PROGRAM WON'T RUN WITHOUT URL AND HEADERS
#HEADERS CONTAINS API PRIVATE DATA AND HENCE HAS BEEN REDUCTED FOR PUBLIC DISPLAY




import requests
import json
import webbrowser
import os
import tkinter as tk
from tkinter import *
from tkinterhtml import HtmlFrame
from PIL import ImageTk,Image


def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

gtuapp = Tk()
gtuapp.title("GTU Report Generator")
gtuapp.geometry('650x600')
gtuapp.resizable(width=False, height=False)

url = "URL REMOVED DUE TO PRIVACY RESAONS"
headers = {
    "HEADERS REMOVED DUE TO PRIVACY RESAONS"
}

tkvar1 = StringVar(gtuapp)
tkvar2 = StringVar(gtuapp)
tkvar3 = StringVar(gtuapp)
tkvar4 = StringVar(gtuapp)
tkvar5 = StringVar(gtuapp)
tkvar6 = StringVar(gtuapp)
tkvar7 = StringVar(gtuapp)
tkvar8 = StringVar(gtuapp)


#enrol = int(160120107114)
#enrol = int(187150592020)
#enrol = int(186670307030)
#enrol = input("Enter your Enrol No: ")

def magic():
    global enrolyear
    enrolyear = str(enrol)[0:2]
    collg = str(enrol)[2:5]
    global courseid
    courseid = str(enrol)[5:7]
    # field = str(enrol)[7:9]
    # enrol = str(enrol)[9:12]

    Winter = "W"
    Summer = "S"
    YEAR = "20" + str(enrolyear)
    # print(YEAR)
    global sem1
    sem1 = Winter + str(YEAR)
    YEAR = int(YEAR) + 1
    global sem2
    sem2 = Summer + str(YEAR)
    global sem3
    sem3 = Winter + str(YEAR)
    YEAR = int(YEAR) + 1
    global sem4
    sem4 = Summer + str(YEAR)
    global sem5
    sem5 = Winter + str(YEAR)
    YEAR = int(YEAR) + 1
    global sem6
    sem6 = Summer + str(YEAR)
    global sem7
    sem7 = Winter + str(YEAR)
    YEAR = int(YEAR) + 1
    global sem8
    sem8 = Summer + str(YEAR)

    global course
    if courseid == "00":
        course = "BA"
    elif courseid == "01":
        course = "BE"
    elif courseid == "31":
        course = "BE"
    elif courseid == "03":
        course = "DIPL"
    elif courseid == "05":
        course = "MBA"

def getenrol():
    labelfont = (10)
    label = Label(gtuapp, text="Enrollment No : ")
    label.config(font=labelfont)
    label.place(x=150, y=100)

    global enrol
    enrol = tk.Entry(gtuapp,validate='all')
    enrol.place(x=300, y=100)
    Button(gtuapp, text="Reset", command=restart_program).place(x=480, y=98)
getenrol()




current1 = "1"
current2 = "1"
current3 = "1"
current4 = "1"
current5 = "1"
current6 = "1"
current7 = "1"
current8 = "1"

def selectrecentsem(x):
    xy = semvalues.index(x)
    if xy == int(0):
        global current1
        current1 = "0"
    elif xy == int(1):
        global current2
        current2 = "0"
    elif xy == int(2):
        global current3
        current3 = "0"
    elif xy == int(3):
        global current4
        current4 = "0"
    elif xy == int(4):
        global current5
        current5 = "0"
    elif xy == int(5):
        global current6
        current6 = "0"
    elif xy == int(6):
        global current7
        current7 = "0"
    elif xy == int(7):
        global current8
        current8 = "0"
    #print(xy)
    global enrol
    enrol = enrol.get()
    magic()
    semester1()



semvar = StringVar(gtuapp)
semvalues = ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6", "Sem 7", "Sem 8"]
labelfont = (10)
labelx = Label(gtuapp, text="This Year Result Declared Of ? ")
labelx.config(font=labelfont)
labelx.place(x=100, y=140)
menux = OptionMenu(gtuapp, semvar, *semvalues, command=selectrecentsem)
menux.place(x=370, y=140)



#labelx = Label(gtuapp, text="This Year Result? ")
# image = Image.open("tick.png")
# image = image.resize((30, 29), Image.ANTIALIAS)
# img = ImageTk.PhotoImage(image)
# panel = Label(gtuapp, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")

def semester1():
    def getresult():
            data1 = "ReqOperation=StudentResult&"
            data2 = "ExamID="
            exami_d = str(finalsem1examid)
            data3 = "&EnrNo="
            data4 = str(enrol)
            data5 = "&DeviceId=3cfe4e8d86634406&OSversion=28&LatLong=0&MobileNo=&IMEI_NO=359849095652100&IPAddress=fe80%3A%3A7410%3A9cff%3Afed4%3Ab798%25dummy0&IsCurrent="
            finaldatababy = data1 + data2 + exami_d + data3 + data4 + data5 + current1
            # print(finaldatababy)
            r = requests.post(url, headers=headers, data=finaldatababy)

            output = json.loads(r.content)
            try:
                panel = Label(gtuapp, text="Done", fg="green")
                panel.place(x=200,y=200)

                totalsubjects = output[0]["TOTSUBCOUNT"]
                global sonesub
                sonesub = []
                global sonesubname
                sonesubname = []
                global sonesubgrade
                sonesubgrade = []

                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sonesub.append(str(output[0]["SUB" + i]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sonesubname.append(str(output[0]["SUB" + i + "NA"]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sonesubgrade.append(str(output[0]["SUB" + i + "GR"]))

                semester2()
            except:
                generate()


    def callbacksem1(submit):
        global finalsem1examid
        sem1examid = sem1exami_d.index(submit)
        finalsem1examid = s1output[sem1examid]["examid"]
        #print(finalsem1examid)
        getresult()
    def getexamidsem1():
        data1 = "ReqOperation=GetExamName&ExSession="
        data2 = str(sem1)
        data3 = "&ExType="
        data4 = course
        finaldatababy = data1 + data2 + data3 + data4
        #print(finaldatababy)
        r = requests.post(url, headers=headers, data=finaldatababy)
        global s1output
        s1output = json.loads(r.content)
        #print(len(s1output))
        global sem1exami_d
        sem1exami_d = []
        for i in range(len(s1output)):
            sem1exami_d.append(str(s1output[i]["exam"]))
        #print(sem1exami_d)
        menu = OptionMenu(gtuapp, tkvar1, *sem1exami_d, command=callbacksem1)
        menu.place(x=300,y=200)
    getexamidsem1()



def semester2():
    def getresult():
            data1 = "ReqOperation=StudentResult&"
            data2 = "ExamID="
            exami_d = str(finalsem2examid)
            data3 = "&EnrNo="
            data4 = str(enrol)
            data5 = "&DeviceId=3cfe4e8d86634406&OSversion=28&LatLong=0&MobileNo=&IMEI_NO=359849095642100&IPAddress=fe80%3A%3A7410%3A9cff%3Afed4%3Ab798%25dummy0&IsCurrent="

            finaldatababy = data1 + data2 + exami_d + data3 + data4 + data5 + current2
            # print(finaldatababy)
            r = requests.post(url, headers=headers, data=finaldatababy)

            output = json.loads(r.content)
            try:
                panel = Label(gtuapp, text="Done", fg="green")
                panel.place(x=200, y=240)

                totalsubjects = output[0]["TOTSUBCOUNT"]
                global stwosub
                stwosub = []
                global stwosubname
                stwosubname = []
                global stwosubgrade
                stwosubgrade = []

                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    stwosub.append(str(output[0]["SUB" + i]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    stwosubname.append(str(output[0]["SUB" + i + "NA"]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    stwosubgrade.append(str(output[0]["SUB" + i + "GR"]))

                semester3()
            except:
                generate()

    def callbacksem2(submit):
        global finalsem2examid
        sem2examid = sem2exami_d.index(submit)
        finalsem2examid = s2output[sem2examid]["examid"]
        #print(finalsem2examid)
        getresult()
    def getexamidsem2():
        data1 = "ReqOperation=GetExamName&ExSession="
        data2 = str(sem2)
        data3 = "&ExType="
        data4 = course
        finaldatababy = data1 + data2 + data3 + data4
        #print(finaldatababy)
        r = requests.post(url, headers=headers, data=finaldatababy)
        global s2output
        s2output = json.loads(r.content)
        #print(len(s2output))
        global sem2exami_d
        sem2exami_d = []
        for i in range(len(s2output)):
            sem2exami_d.append(str(s2output[i]["exam"]))
        #print(sem2exami_d)
        menu = OptionMenu(gtuapp, tkvar2, *sem2exami_d, command=callbacksem2)
        menu.place(x=300,y=240)
    getexamidsem2()



def semester3():
    def getresult():
            data1 = "ReqOperation=StudentResult&"
            data2 = "ExamID="
            exami_d = str(finalsem3examid)
            data3 = "&EnrNo="
            data4 = str(enrol)
            data5 = "&DeviceId=3cfe4e8d86634406&OSversion=28&LatLong=0&MobileNo=&IMEI_NO=359867593182100&IPAddress=fe80%3A%3A7410%3A9cff%3Afed4%3Ab798%25dummy0&IsCurrent="
            finaldatababy = data1 + data2 + exami_d + data3 + data4 + data5 + current3
            #print(finaldatababy)
            r = requests.post(url, headers=headers, data=finaldatababy)

            output = json.loads(r.content)
            try:
                panel = Label(gtuapp, text="Done", fg="green")
                panel.place(x=200, y=280)

                totalsubjects = output[0]["TOTSUBCOUNT"]
                global sthreesub
                sthreesub = []
                global sthreesubname
                sthreesubname = []
                global sthreesubgrade
                sthreesubgrade = []

                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sthreesub.append(str(output[0]["SUB" + i]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sthreesubname.append(str(output[0]["SUB" + i + "NA"]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sthreesubgrade.append(str(output[0]["SUB" + i + "GR"]))

                semester4()
            except:
                generate()

    def callbacksem3(submit):
        global finalsem3examid
        sem3examid = sem3exami_d.index(submit)
        finalsem3examid = s3output[sem3examid]["examid"]
        #print(finalsem3examid)
        getresult()
    def getexamidsem3():
        data1 = "ReqOperation=GetExamName&ExSession="
        data2 = str(sem3)
        data3 = "&ExType="
        data4 = course
        finaldatababy = data1 + data2 + data3 + data4
        #print(finaldatababy)
        r = requests.post(url, headers=headers, data=finaldatababy)
        global s3output
        s3output = json.loads(r.content)
        #print(len(s3output))
        global sem3exami_d
        sem3exami_d = []
        for i in range(len(s3output)):
            sem3exami_d.append(str(s3output[i]["exam"]))
        #print(sem3exami_d)
        menu = OptionMenu(gtuapp, tkvar3, *sem3exami_d, command=callbacksem3)
        menu.place(x=300,y=280)
    getexamidsem3()



def semester4():
    def getresult():
            data1 = "ReqOperation=StudentResult&"
            data2 = "ExamID="
            exami_d = str(finalsem4examid)
            data3 = "&EnrNo="
            data4 = str(enrol)
            data5 = "&DeviceId=3cfe4e8d86634406&OSversion=28&LatLong=0&MobileNo=&IMEI_NO=359849093452100&IPAddress=fe80%3A%3A7410%3A9cff%3Afed4%3Ab798%25dummy0&IsCurrent="

            finaldatababy = data1 + data2 + exami_d + data3 + data4 + data5 + current4
            # print(finaldatababy)
            r = requests.post(url, headers=headers, data=finaldatababy)

            output = json.loads(r.content)
            try:
                panel = Label(gtuapp, text="Done", fg="green")
                panel.place(x=200, y=320)

                totalsubjects = output[0]["TOTSUBCOUNT"]
                global sfoursub
                sfoursub = []
                global sfoursubname
                sfoursubname = []
                global sfoursubgrade
                sfoursubgrade = []

                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sfoursub.append(str(output[0]["SUB" + i]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sfoursubname.append(str(output[0]["SUB" + i + "NA"]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sfoursubgrade.append(str(output[0]["SUB" + i + "GR"]))
                semester5()
            except:
                generate()

    def callbacksem4(submit):
        global finalsem4examid
        sem4examid = sem4exami_d.index(submit)
        finalsem4examid = s4output[sem4examid]["examid"]
        #print(finalsem4examid)
        getresult()
    def getexamidsem4():
        data1 = "ReqOperation=GetExamName&ExSession="
        data2 = str(sem4)
        data3 = "&ExType="
        data4 = course
        finaldatababy = data1 + data2 + data3 + data4
        #print(finaldatababy)
        r = requests.post(url, headers=headers, data=finaldatababy)
        global s4output
        s4output = json.loads(r.content)
        #print(len(s4output))
        global sem4exami_d
        sem4exami_d = []
        for i in range(len(s4output)):
            sem4exami_d.append(str(s4output[i]["exam"]))
        #print(sem4exami_d)
        menu = OptionMenu(gtuapp, tkvar4, *sem4exami_d, command=callbacksem4)
        menu.place(x=300,y=320)
    getexamidsem4()


def semester5():
    def getresult():
            data1 = "ReqOperation=StudentResult&"
            data2 = "ExamID="
            exami_d = str(finalsem5examid)
            data3 = "&EnrNo="
            data4 = str(enrol)
            data5 = "&DeviceId=3cfe4e8d86634406&OSversion=28&LatLong=0&MobileNo=&IMEI_NO=357879093182100&IPAddress=fe80%3A%3A7410%3A9cff%3Afed4%3Ab798%25dummy0&IsCurrent="

            finaldatababy = data1 + data2 + exami_d + data3 + data4 + data5 + current5
            # print(finaldatababy)
            r = requests.post(url, headers=headers, data=finaldatababy)

            output = json.loads(r.content)
            try:
                panel = Label(gtuapp, text="Done", fg="green")
                panel.place(x=200, y=360)

                totalsubjects = output[0]["TOTSUBCOUNT"]
                global sfivesub
                sfivesub = []
                global sfivesubname
                sfivesubname = []
                global sfivesubgrade
                sfivesubgrade = []

                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sfivesub.append(str(output[0]["SUB" + i]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sfivesubname.append(str(output[0]["SUB" + i + "NA"]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    sfivesubgrade.append(str(output[0]["SUB" + i + "GR"]))
                semester6()
            except:
                generate()

    def callbacksem5(submit):
        global finalsem5examid
        sem5examid = sem5exami_d.index(submit)
        finalsem5examid = s5output[sem5examid]["examid"]
        #print(finalsem5examid)
        getresult()
    def getexamidsem5():
        data1 = "ReqOperation=GetExamName&ExSession="
        data2 = str(sem5)
        data3 = "&ExType="
        data4 = course
        finaldatababy = data1 + data2 + data3 + data4
        #print(finaldatababy)
        r = requests.post(url, headers=headers, data=finaldatababy)
        global s5output
        s5output = json.loads(r.content)
        #print(len(s5output))
        global sem5exami_d
        sem5exami_d = []
        for i in range(len(s5output)):
            sem5exami_d.append(str(s5output[i]["exam"]))
        #print(sem3exami_d)
        menu = OptionMenu(gtuapp, tkvar5, *sem5exami_d, command=callbacksem5)
        menu.place(x=300, y=360)
    getexamidsem5()



def semester6():
    def getresult():
            data1 = "ReqOperation=StudentResult&"
            data2 = "ExamID="
            exami_d = str(finalsem6examid)
            data3 = "&EnrNo="
            data4 = str(enrol)
            data5 = "&DeviceId=3cfe4e8d86634406&OSversion=28&LatLong=0&MobileNo=&IMEI_NO=359849565182100&IPAddress=fe80%3A%3A7410%3A9cff%3Afed4%3Ab798%25dummy0&IsCurrent="

            finaldatababy = data1 + data2 + exami_d + data3 + data4 + data5 + current6
            # print(finaldatababy)
            r = requests.post(url, headers=headers, data=finaldatababy)

            output = json.loads(r.content)
            try:
                panel = Label(gtuapp, text="Done", fg="green")
                panel.place(x=200, y=400)

                totalsubjects = output[0]["TOTSUBCOUNT"]
                global ssixsub
                ssixsub = []
                global ssixsubname
                ssixsubname = []
                global ssixsubgrade
                ssixsubgrade = []

                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    ssixsub.append(str(output[0]["SUB" + i]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    ssixsubname.append(str(output[0]["SUB" + i + "NA"]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    ssixsubgrade.append(str(output[0]["SUB" + i + "GR"]))
                semester7()
            except:
                generate()

    def callbacksem6(submit):
        global finalsem6examid
        sem6examid = sem6exami_d.index(submit)
        finalsem6examid = s6output[sem6examid]["examid"]
        #print(finalsem6examid)
        getresult()
    def getexamidsem6():
        data1 = "ReqOperation=GetExamName&ExSession="
        data2 = str(sem6)
        data3 = "&ExType="
        data4 = course
        finaldatababy = data1 + data2 + data3 + data4
        #print(finaldatababy)
        r = requests.post(url, headers=headers, data=finaldatababy)
        global s6output
        s6output = json.loads(r.content)
        #print(len(s6output))
        global sem6exami_d
        sem6exami_d = []
        for i in range(len(s6output)):
            sem6exami_d.append(str(s6output[i]["exam"]))
        #print(sem6exami_d)
        menu = OptionMenu(gtuapp, tkvar6, *sem6exami_d, command=callbacksem6)
        menu.place(x=300, y=400)
    getexamidsem6()

def semester7():
    def getresult():
            data1 = "ReqOperation=StudentResult&"
            data2 = "ExamID="
            exami_d = str(finalsem7examid)
            data3 = "&EnrNo="
            data4 = str(enrol)
            data5 = "&DeviceId=3cfe4e8d86634406&OSversion=28&LatLong=0&MobileNo=&IMEI_NO=359849096752100&IPAddress=fe80%3A%3A7410%3A9cff%3Afed4%3Ab798%25dummy0&IsCurrent="

            finaldatababy = data1 + data2 + exami_d + data3 + data4 + data5 + current7
            # print(finaldatababy)
            r = requests.post(url, headers=headers, data=finaldatababy)

            output = json.loads(r.content)
            try:
                panel = Label(gtuapp, text="Done", fg="green")
                panel.place(x=200, y=440)

                totalsubjects = output[0]["TOTSUBCOUNT"]
                global ssevensub
                ssevensub = []
                global ssevensubname
                ssevensubname = []
                global ssevensubgrade
                ssevensubgrade = []

                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    ssevensub.append(str(output[0]["SUB" + i]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    ssevensubname.append(str(output[0]["SUB" + i + "NA"]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    ssevensubgrade.append(str(output[0]["SUB" + i + "GR"]))
                semester8()
            except:
                generate()

            semester8()
    def callbacksem7(submit):
        global finalsem7examid
        sem7examid = sem7exami_d.index(submit)
        finalsem7examid = s7output[sem7examid]["examid"]
        #print(finalsem7examid)
        getresult()
    def getexamidsem7():
        data1 = "ReqOperation=GetExamName&ExSession="
        data2 = str(sem7)
        data3 = "&ExType="
        data4 = course
        finaldatababy = data1 + data2 + data3 + data4
       # print(finaldatababy)
        r = requests.post(url, headers=headers, data=finaldatababy)
        global s7output
        s7output = json.loads(r.content)
        #print(len(s7output))
        global sem7exami_d
        sem7exami_d = []
        for i in range(len(s7output)):
            sem7exami_d.append(str(s7output[i]["exam"]))
        #print(sem7exami_d)
        menu = OptionMenu(gtuapp, tkvar7, *sem7exami_d, command=callbacksem7)
        menu.place(x=300, y=440)
    getexamidsem7()

def semester8():
    def getresult():
            data1 = "ReqOperation=StudentResult&"
            data2 = "ExamID="
            exami_d = str(finalsem8examid)
            data3 = "&EnrNo="
            data4 = str(enrol)
            data5 = "&DeviceId=3cfe4e8d86634406&OSversion=28&LatLong=0&MobileNo=&IMEI_NO=359876593182100&IPAddress=fe80%3A%3A7410%A9cff%3Afed4%3Ab798%25dummy0&IsCurrent="

            finaldatababy = data1 + data2 + exami_d + data3 + data4 + data5 + current8
            # print(finaldatababy)
            r = requests.post(url, headers=headers, data=finaldatababy)

            output = json.loads(r.content)
            try:
                panel = Label(gtuapp, text="Done", fg="green")
                panel.place(x=200, y=480)

                totalsubjects = output[0]["TOTSUBCOUNT"]
                global seightsub
                seightsub = []
                global seightsubname
                seightsubname = []
                global seightsubgrade
                seightsubgrade = []

                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    seightsub.append(str(output[0]["SUB" + i]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    seightsubname.append(str(output[0]["SUB" + i + "NA"]))
                for i in range(1, int(totalsubjects) + 1):
                    i = str(i)
                    seightsubgrade.append(str(output[0]["SUB" + i + "GR"]))
            except:
                generate()

    def callbacksem8(submit):
        global finalsem8examid
        sem8examid = sem8exami_d.index(submit)
        finalsem8examid = s8output[sem8examid]["examid"]
        #print(finalsem8examid)
        getresult()
    def getexamidsem8():
        data1 = "ReqOperation=GetExamName&ExSession="
        data2 = str(sem8)
        data3 = "&ExType="
        data4 = course
        finaldatababy = data1 + data2 + data3 + data4
        #print(finaldatababy)
        r = requests.post(url, headers=headers, data=finaldatababy)
        global s8output
        s8output = json.loads(r.content)
        #print(len(s8output))
        global sem8exami_d
        sem8exami_d = []
        for i in range(len(s8output)):
            sem8exami_d.append(str(s8output[i]["exam"]))
        #print(sem8exami_d)
        menu = OptionMenu(gtuapp, tkvar8, *sem8exami_d, command=callbacksem8)
        menu.place(x=300, y=480)
    getexamidsem8()

def generate():
    MyButton = Button(gtuapp, text="Submit", width=25, command=generatereport)
    MyButton.place(x=250,y=520)

def generatereport():
    try:
        #print(sonesub)
        #print(stwosub)
        #print(sthreesub)
        #print(sfoursub)
        #print(sfivesub)
        #print(ssixsub)
        #print(ssevensub)
        #print(seightsub)

        label_frame = LabelFrame(gtuapp, text="STUDENT REPORT", bg="grey", fg="black", font="Lato 12", borderwidth=2,relief="groove", padx="2", pady="2")
        label_frame.pack(expand='yes', fill='both')

        global destroy
        destroy = Button(label_frame, text="Back", width=10, command=label_frame.destroy)
        destroy.place(x=0, y=0)
        
        name = Label(label_frame, text=ssixsub, bg="grey", fg="black", font="Lato 12", borderwidth=2,relief="groove", padx="2", pady="2")
        name.place(x=120, y=5)

        enrollment = Label(label_frame, text=sonesubgrade, bg="black", fg="white", font="Lato 12",borderwidth=2, relief="groove", padx="2", pady="2")
        enrollment.place(x=120, y=35)
    except:
        pass

titlefont = ('times', 30, 'bold')
title = Label(gtuapp, text="GTU Report Generator" )
title.config(font=titlefont)
title.place(x=130, y=0)


def senti(url):
    webbrowser.open_new(url)
ref = Label(gtuapp, text="Sentinal920", fg="blue", cursor="hand2")
ref.place(x=290,y=570)
ref.bind("<Button-1>", lambda e: senti("https://sentinal920.github.io/"))

gtuapp.mainloop()
