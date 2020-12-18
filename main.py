import requests
import urllib
from tkinter import *
from tkinter import ttk
import feedparser
import os
from dotenv import load_dotenv
import json
import webbrowser
import time

# Grabs API key
load_dotenv("api_key.env")
api_key = os.getenv("API_KEY")
api_key = json.loads(api_key)

# Initial window - edit later
root = Tk()
root.geometry("915x600")
root.title("Starter Page")

# Title
ttk.Label(root, text="Starter Page", font=("Nevis", 18)).grid()

# Time 

# Verses grabber - edit later
verses = open("verses.txt", "r")
daily_verse = requests.get(f"https://api.esv.org/v3/passage/text/?q={verses.readline()}", headers=api_key)
daily_verse = json.loads(daily_verse.text)
daily_verse = daily_verse["passages"][0]

link_label = {}
interval_1 = 0
interval_2 = 0
url = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
for num in range(0, 6):
    try:
        label_text = url["entries"][num]["title_detail"]["value"]
        ttk.Label(root, text=f"{label_text[0:70]}...", font=("Times New Roman", 12)).grid(sticky=NW, padx=1)
        label_text = url["entries"][num]["id"]
        link_label[num] = ttk.Label(root, text=f"{label_text[0:70]}...", font=("Consolas", 10))
        link_label[num].grid(sticky=NW, padx=2)
    except KeyError:
        continue
    except IndexError:
        continue

link_label[0].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][0]["id"]))
link_label[1].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][1]["id"]))
link_label[2].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][2]["id"]))
link_label[3].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][3]["id"]))
link_label[4].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][4]["id"]))
link_label[5].bind("<Button-1>", lambda e: webbrowser.open(url["entries"][5]["id"]))

# Shows verses - edit later
ttk.Label(root, text=daily_verse)

# Weather web scraper - edit later

# To-do list - edit later

root.mainloop()
