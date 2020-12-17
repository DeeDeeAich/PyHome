import requests
import urllib
from tkinter import *
from tkinter import ttk
import feedparser
import os
from dotenv import load_dotenv
import json
import webbrowser

# Grabs API key
load_dotenv("api_key.env")
api_key = os.getenv("API_KEY")
api_key = json.loads(api_key)

# Initial window - edit later
root = Tk()
root.geometry("915x600")
root.title("Starter Py")

# Verses grabber - edit later
verses = open("verses.txt", "r")
daily_verse = requests.get(f"https://api.esv.org/v3/passage/text/?q={verses.readline()}", headers=api_key)
daily_verse = json.loads(daily_verse.text)
daily_verse = daily_verse["passages"][0]

# RSS Feed parser - edit later
url = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
for num in range(0, 6):
    try:
        ttk.Label(root, text=url["entries"][num]["title_detail"]["value"]).pack()
        link_label = ttk.Label(root, text=url["entries"][num]["id"])
        link_label.bind("<Button-1>", lambda e: webbrowser.open(url["entries"][num]["id"]))
        link_label.pack()
        label_text = "Published: " + url["entries"][num]["published"]
        ttk.Label(root, text=label_text).pack()
    except KeyError:
        continue
    except IndexError:
        continue

# Shows verses - edit later
ttk.Label(root, text=daily_verse)

# Weather web scraper - edit later

# To-do list - edit later

root.mainloop()
