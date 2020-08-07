#THIS PROGRAM WON'T RUN WITHOUT URL AND HEADERS

#HEADERS CONTAINS API PRIVATE DATA AND HENCE HAS BEEN REDUCTED FOR PUBLIC DISPLAY



import requests
import json
import tkinter as tk
from tkinter import *
from tkinterhtml import HtmlFrame
from PIL import ImageTk,Image
import webbrowser
import os

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

gtuapp = Tk()
gtuapp.title("GTU History Fetcher")
gtuapp.geometry('650x600')
gtuapp.resizable(width=False, height=False)

def getresult():

    url = "URL REMOVED DUE TO PRIVACY RESAONS"

    cookievalues = "ASP.NET_SessionId=" + cookievalue

    headers = {
       " HEADER REMOVED DUE TO PRIVACY RESAONS"
    }

    data1 = "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTI3MDg3Nzc0MmQYBAUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFGGN0bDAwJE1haW5Db250ZW50JGltZ3JlZgUbY3RsMDAkTWFpbkNvbnRlbnQkR3JpZFZpZXcxD2dkBR1jdGwwMCRNYWluQ29udGVudCRncmR2TGFzdEV4bQ9nZAUXY3RsMDAkTWFpbkNvbnRlbnQkZ3JkdjIPZ2Qh9RpX7IvJH9Ix62%2FdB5pN%2BNc8jr%2FiM4PVTxNf2wZmYA%3D%3D&__VIEWSTATEGENERATOR=A71F3F29&ctl00%24MainContent%24txtEnrollNo="
    data2 = str(enrol.get())

    data3 = str(data2)
    data4 = "&ctl00%24MainContent%24CodeNumberTextBox="
    data5 = str(captha.get())

    data6 = str(data5)
    data7 = "&ctl00%24MainContent%24btnSubmit=Search"

    data8 = data1 + data3 + data4 + data6 + data7
    global r
    r = requests.post(url, headers=headers, data=data8, allow_redirects=True)

    # try:
    #     MyButton2.destroy()
    # except:
    #     pass

    displayresult()
    #print(r.content)

def displayresult():
    frame = HtmlFrame(gtuapp, horizontal_scrollbar="auto",vertical_scrollbar="auto",width=500,height=500)
    frame.set_content(r.content)
    frame.pack(expand = 'yes', fill = 'both')

    global MyButton2
    MyButton2 = Button(frame, text="Back", width=10, command=frame.destroy)
    MyButton2.place(x = 0, y = 0)

def callback():
    MyButton = Button(gtuapp, text="Submit", width=25, command=getresult)
    MyButton.place(x=300,y=300)


def get_cookies_captha():
    x = requests.get('http://www.students.gtu.ac.in/Handler.ashx')
    open('ImageVerify.jpg', 'wb').write(x.content) #Captha_Saved
    cookie = x.cookies.get_dict()
    global cookievalue #Cookie_Value_Saved
    cookie, cookievalue = (list(cookie.items())[0])


def getenrol():
    global enrol

    labelfont = (10)
    label = Label(gtuapp, text="    Enrollment No : ")
    label.config(font=labelfont)
    label.place(x=100, y=150)

    enrol = tk.Entry(gtuapp)
    enrol.place(x=300,y=150, width=200, height=30)
getenrol()

def getcaptha():
    get_cookies_captha()
    global captha
    #capthalabel = Label(gtuapp, text="Enter Captha: ")
    #capthalabel.place(x=170, y=40)

    captha = tk.Entry(gtuapp)
    captha.place(x=300,y=220, width=200, height=30)
    callback()
getcaptha()





titlefont = ('times', 30, 'bold')
title = Label(gtuapp, text="GTU History Fetcher",  )
title.config(font=titlefont)
title.place(x=130, y=50)

canvas = Canvas(gtuapp, width = 150, height = 50)
canvas.place(x=120,y=200)
img = ImageTk.PhotoImage(Image.open("ImageVerify.jpg"))
canvas.create_image(5, 5, anchor=NW, image=img)

# reset = Button(gtuapp, text="Reset", width=5, command=reset)
# reset.place(x=550,y=220)


Button(gtuapp, text="Reset", command=restart_program).place(x=550,y=220)

def senti(url):
    webbrowser.open_new(url)
ref = Label(gtuapp, text="Sentinal920", fg="blue", cursor="hand2")
ref.place(x=290,y=570)
ref.bind("<Button-1>", lambda e: senti("https://sentinal920.github.io/"))

gtuapp.mainloop()
