import requests
from tkinter import *
from tkinter import ttk
import feedparser
import os
from dotenv import load_dotenv
import json
import webbrowser
import time
from bs4 import BeautifulSoup

# Grabs API key
load_dotenv("api_key.env")
api_key = os.getenv("API_KEY")
api_key = json.loads(api_key)

# Initial window - edit later
root = Tk()
root.geometry("1175x600")
root.title("Starter Page")

# Title - edit later
title_label = ttk.Label(root, text="Starter Page", font=("Nevis", 18))
title_label.grid(column=1, row=0, sticky=N)
title_label.configure(anchor="center")

# Time - solve not updating error
def update_time():
    now = time.strftime("%I:%M:%S")
    time_label.configure(text=now)
    time_label.after(1000, update_time)

time_label = ttk.Label(root, text=time.strftime("%I:%M:%S"))
time_label.grid(row=0, column=2)
update_time()

# RSS Feed - improve later
link_label = {}
rss_feed_entry = ttk.Entry(root)
def get_articles():
    for num in range(0, 6):
        try:
            rss_notice.grid_forget()
            rss_feed_entry.grid_forget()
            submit_rss.grid_forget()

            url = feedparser.parse(rss_feed_entry.get())
            label_text = url["entries"][num]["title_detail"]["value"]
            row_num1 = num + 1
            ttk.Label(root, text=f"{label_text[0:70]}...", font=("Times New Roman", 12)).grid(row=row_num1, column=0)
            label_text = url["entries"][num]["id"]
            link_label[num] = ttk.Label(root, text=f"{label_text[0:70]}...", font=("Consolas", 10))
            row_num2 = num + 3
            link_label[num].grid(row=row_num2, column=0)
        except KeyError:
            continue
        except IndexError:
            continue

    # link_label[0].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][0]["id"]))
    # link_label[1].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][1]["id"]))
    # link_label[2].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][2]["id"]))
    # link_label[3].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][3]["id"]))
    # link_label[4].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][4]["id"]))
    # link_label[5].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][5]["id"]))

rss_notice = ttk.Label(root, text="Please enter an RSS Feed Link:")
rss_notice.grid(column=0, row=1)
rss_feed_entry.grid(column=0, row=2)
submit_rss = ttk.Button(root, text="Submit", command=get_articles)
submit_rss.grid(column=0, row=3)
ttk.Label(root, text="").grid(sticky=N, row=16)

# Verses grabber - edit later
verses = open("verses.txt", "r")
daily_verse = requests.get(f"https://api.esv.org/v3/passage/text/?q={verses.readline()}", headers=api_key)
daily_verse = json.loads(daily_verse.text)
daily_verse = daily_verse["passages"][0]

ttk.Label(root, text=" ").grid(row=12, column=0)
ttk.Label(root, text="Daily Verse: ", font=("Cardo", 12)).grid(row=13, column=0)
verse = ttk.Label(root, text=daily_verse[0:80], font=("Cardo", 11))
verse.grid(row=14, column=0)
ttk.Label(root, text=daily_verse[80:160]).grid(row=15, column=0)
ttk.Label(root, text=daily_verse[160:240]).grid(row=16, column=0)

# Weather web scraper - edit and document later
def submit_weather():
    location_file = open("location.txt", "w")
    location_file.write(location.get())
    location_file.close()

    weather_notice.grid_forget()
    submit_weather_button.grid_forget()

    user_location = open("location.txt", "r").read()
    location.grid_forget()

    url = f"https://www.google.com/search?q=weather+{user_location}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    ttk.Label(root, text=soup.find("div", class_="kCrYT").text, font=("Nevis", 15)).grid(row=13, column=2)
    ttk.Label(root, text=soup.find("div", class_="BNeawe iBp4i AP7Wnd").text, font=("Times New Roman", 14)).grid(row=14, column=2)
    ttk.Label(root, text=soup.find("div", class_="BNeawe tAd8D AP7Wnd").text, font=("Times New Roman", 14)).grid(row=15, column=2)

def enter_key_weather(event):
    submit_weather()

if open("location.txt", "r").read() == "":
    weather_notice = ttk.Label(root, text="NOTE: Your location will not be stored. This is for weather information purposes. \nPlease enter a city or zip code.", anchor="center")
    weather_notice.grid(column=2, row=13)
    location = ttk.Entry(root)
    location.grid(column=2, row=14)

    submit_weather_button = ttk.Button(root, text="Submit", command=submit_weather)
    submit_weather_button.grid(row=15, column=2)
    location.bind("<Return>", enter_key_weather)
else:
    user_location = open("location.txt", "r").read()

    url = f"https://www.google.com/search?q=weather+{user_location}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    ttk.Label(root, text=soup.find("div", class_="kCrYT").text, font=("Nevis", 15)).grid(row=13, column=2)
    ttk.Label(root, text=soup.find("div", class_="BNeawe iBp4i AP7Wnd").text, font=("Times New Roman", 14)).grid(row=14, column=2)
    ttk.Label(root, text=soup.find("div", class_="BNeawe tAd8D AP7Wnd").text, font=("Times New Roman", 14)).grid(row=15, column=2)

# To-do list - edit and document later
checklist_items = ttk.Entry(root)
checklist_items.grid(row=1, column=2)

check_variable = [IntVar()]
items = {}
counter = 0
def submit_checklist():
    if checklist_items.get() == "":
        error = Toplevel(root)
        error.title("Error!")
        error.geometry("250x50")
        ttk.Label(error, text="Error, cannot add a blank to-do list item!").pack()
    elif len(items) >= 10:
        error = Toplevel(root)
        error.title("Error!")
        error.geometry("350x50")
        ttk.Label(error, text="Error, you cannot add over 10 items to your To-Do list!").pack()
    elif len(checklist_items.get()) > 40:
        error = Toplevel(root)
        error.title("Error!")
        error.geometry("350x50")
        ttk.Label(error, text="Error, your To-Do list item is too long!").pack()
    # elif item == checklist_items.get():
    #     error = Toplevel(root)
    #     error.title("Error!")
    #     error.geometry("350x50")
    #     ttk.Label(error, text="Error, your To-Do list item is too long!").pack()
    #     # not working
    else:
        global counter
        counter += 1
        check_variable.append(IntVar())
        items[counter] = ttk.Checkbutton(root, text=checklist_items.get(), variable=check_variable[counter])
        checklist_items.delete(0, END)
        row_num = counter + 2
        items[counter].grid(row=row_num, column=2)

    for i in range(0, 10):
        if check_variable[i].get():
            items[i].grid_forget()

def enter_key_checklist(event):
    submit_checklist()

add_item = ttk.Button(root, command=submit_checklist, text="Add Item").grid(row=2, column=2)
checklist_items.bind("<Return>", enter_key_checklist)

root.mainloop()
