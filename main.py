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
import sqlite3
import mysql.connector

# Grabs API key
load_dotenv("api_key.env")
api_key = os.getenv("API_KEY")
api_key = json.loads(api_key)

# Grabs DB Password
load_dotenv("db_password.env")
db_password = os.getenv("DB_PASSWORD")

# Verses Database Connection
verses_con = mysql.connector.connect(host="192.168.1.100", database="verses_db", user="admin", password=db_password)
verses_cur = verses_con.cursor()
verses_cur.execute("select locations from verses")

# Master Database Connection
master_con = sqlite3.connect("master.db")
master_cur = master_con.cursor()

# Initial window - edit later
root = Tk()
root.geometry("1175x600")
root.title("Starter Page")

# Title
title_label = ttk.Label(root, text="Starter Page", font=("Nevis", 18))
title_label.grid(column=1, row=0, sticky=N)
title_label.configure(anchor="center")

# Time
def update_time():
    now = time.strftime("%I:%M:%S")
    time_label.configure(text=now)
    time_label.after(1000, update_time)

time_label = ttk.Label(root, text=time.strftime("%I:%M:%S"))
time_label.grid(row=0, column=2)
update_time()

# RSS Feed - improve later
def get_articles():
    rss = rss_feed_entry.get()
    master_cur.execute(f"UPDATE user_info SET rss_feed = (?)", (rss,))
    master_con.commit()
    master_cur.execute("select rss_feed from user_info")
    rss_feed = master_cur.fetchall()
    
    row_article = 1
    row_link = 2
    for num in range(0, 6):
        try:
            rss_instructions.grid_forget()
            url = feedparser.parse(rss_feed[0][0])
            rss_feed_entry.grid_forget()
            submit_rss.grid_forget()

            article_title = url["entries"][num]["title_detail"]["value"]
            ttk.Label(root, text=f"{article_title[0:70]}...").grid(row=row_article, column=0)
            row_article += 2
            
            article_link = url["entries"][num]["id"]
            link_label[num] = ttk.Label(root, text=f"{article_link[0:70]}...")
            link_label[num].grid(row=row_link, column=0)
            row_link += 2
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

def enter_key_rss(event):
    get_articles()

link_label = {}
master_cur.execute("SELECT rss_feed FROM user_info")
url = master_cur.fetchall()
if url[0][0] == None:
    rss_feed_entry = ttk.Entry(root)

    rss_instructions = ttk.Label(root, text="(NOTE: As of right now, you cannot change your RSS feed that you use. \nPlease enter an RSS Feed link: ")
    rss_instructions.grid(column=0, row=1)
    rss_feed_entry.grid(column=0, row=2)
    rss_feed_entry.bind("<Return>", enter_key_rss)

    submit_rss = ttk.Button(root, text="Submit", command=get_articles)
    submit_rss.grid(column=0, row=3)
else:
    row_article = 1
    row_link = 2
    for num in range(0, 6):
        try:
            parsed_url = feedparser.parse(url[0][0])

            article_title = parsed_url["entries"][num]["title_detail"]["value"]
            ttk.Label(root, text=f"{article_title[0:70]}...").grid(row=row_article, column=0)
            row_article += 2
            
            article_link = parsed_url["entries"][num]["id"]
            link_label[num] = ttk.Label(root, text=f"{article_link[0:70]}...")
            link_label[num].grid(row=row_link, column=0)
            row_link += 2
        except KeyError:
            continue
        except IndexError:
            continue

    link_label[0].bind("<Button-1>", lambda e: webbrowser.open(parsed_url["entries"][0]["id"]))
    link_label[1].bind("<Button-1>", lambda e: webbrowser.open(parsed_url["entries"][1]["id"]))
    link_label[2].bind("<Button-1>", lambda e: webbrowser.open(parsed_url["entries"][2]["id"]))
    link_label[3].bind("<Button-1>", lambda e: webbrowser.open(parsed_url["entries"][3]["id"]))
    link_label[4].bind("<Button-1>", lambda e: webbrowser.open(parsed_url["entries"][4]["id"]))
    link_label[5].bind("<Button-1>", lambda e: webbrowser.open(parsed_url["entries"][5]["id"]))

# Verses grabber - edit later
verse_location = verses_cur.fetchall()
daily_verse = requests.get(f"https://api.esv.org/v3/passage/text/?q={verse_location[0][0]}", headers=api_key)
daily_verse = json.loads(daily_verse.text)
daily_verse = daily_verse["passages"][0]

ttk.Label(root, text="Daily Verse: ", font=("Cardo", 12)).grid(row=13, column=0)
verse = ttk.Label(root, text=daily_verse[0:80], font=("Cardo", 11))
verse.grid(row=14, column=0)
ttk.Label(root, text=daily_verse[80:160]).grid(row=15, column=0)
ttk.Label(root, text=daily_verse[160:240]).grid(row=16, column=0)

# Weather web scraper - edit and document later
def submit_weather():
    user_location = location.get()
    master_cur.execute("update user_info set location = (?)", (user_location,))
    master_con.commit()
    master_cur.execute("select location from user_info")
    user_location = master_cur.fetchall()

    weather_notice.grid_forget()
    submit_weather_button.grid_forget()
    location.grid_forget()

    url = f"https://www.google.com/search?q=weather+{user_location}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    ttk.Label(root, text=soup.find("div", class_="kCrYT").text, font=("Nevis", 15)).grid(row=13, column=2)
    ttk.Label(root, text=soup.find("div", class_="BNeawe iBp4i AP7Wnd").text, font=("Times New Roman", 14)).grid(row=14, column=2)
    ttk.Label(root, text=soup.find("div", class_="BNeawe tAd8D AP7Wnd").text, font=("Times New Roman", 14)).grid(row=15, column=2)

def enter_key_weather(event):
    submit_weather()

master_cur.execute("SELECT location FROM user_info")
user_location = master_cur.fetchall()
if user_location[0][0] == None:
    weather_notice = ttk.Label(root, text="Please enter a city or zip code: \n(NOTE: As of right now, you cannot change your location)", anchor="center")
    weather_notice.grid(column=2, row=13)
    location = ttk.Entry(root)
    location.grid(column=2, row=14)

    submit_weather_button = ttk.Button(root, text="Submit", command=submit_weather)
    submit_weather_button.grid(row=15, column=2)
    location.bind("<Return>", enter_key_weather)
else:
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
    else:
        global counter
        counter += 1
        check_variable.append(IntVar())
        items[counter] = ttk.Checkbutton(root, text=checklist_items.get(), variable=check_variable[counter])
        checklist_items.delete(0, END)
        row_num = counter + 2
        items[counter].grid(row=row_num, column=2)

    for i in range(0, 10):
        if IntVar().get() > 1:
            items[i].grid_forget()
        

def enter_key_checklist(event):
    submit_checklist()

add_item = ttk.Button(root, command=submit_checklist, text="Add Item").grid(row=2, column=2)
checklist_items.bind("<Return>", enter_key_checklist)

# Sports scores - edit later
def get_teams():
    count = 0 
    if teams_entry.get() == "":
        error = Toplevel(root)
        error.geometry("250x50")
        ttk.Label(error, text="Error, 0 teams have been added!").pack()
    elif len(teams_entry.get().split(",")) > 3:
        error = Toplevel(root)
        error.geometry("250x50")
        ttk.Label(error, text="Error, cannot add more than 3 teams!").pack()
    else:
        for team in teams_entry.get().split(","):
            master_cur.execute("update user_info set teams = (?)", (teams_entry.get(),))
            master_con.commit()

            team_info = requests.get(f"https://www.google.com/search?q={team}+score")
            soup = BeautifulSoup(team_info.content, "html.parser")

            ttk.Label(root, text=soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd lRVwie")[0].text).grid(column=count, row=18)

            team1 = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd lRVwie")[1]
            score1 = soup.find_all("div", class_="BNeawe deIvCb AP7Wnd")[1]
            team2 = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd lRVwie")[2]
            score2 = soup.find_all("div", class_="BNeawe deIvCb AP7Wnd")[2]

            ttk.Label(root, text=f"{team1.text}\t{score1.text}").grid(column=count, row=19)
            ttk.Label(root, text=f"{team2.text}\t{score2.text}").grid(column=count, row=20)

            count += 1

        submit_teams.grid_forget()
        teams_notice.grid_forget()
        teams_entry.grid_forget()

def enter_key_teams(event):
    get_teams()

master_cur.execute("select teams from user_info")
if master_cur.fetchall()[0][0] == None:
    teams_notice = ttk.Label(root, text="Enter up to 3 teams (Separated by comma) \nFor college teams, please specify the sport.")
    teams_notice.grid(row=18, column=1)
    teams_entry = ttk.Entry(root)
    teams_entry.grid(column=1, row=19)

    teams_entry.bind("<Return>", enter_key_teams)
    submit_teams = ttk.Button(root, text="Submit", command=get_teams)
    submit_teams.grid(column=1, row=20)
else:
    master_cur.execute("select teams from user_info")
    teams = master_cur.fetchall()[0][0].split(",")
    count = 0
    for team in teams:
        team_info = requests.get(f"https://www.google.com/search?q={team}+score")
        soup = BeautifulSoup(team_info.content, "html.parser")

        team1 = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd lRVwie")[1]
        score1 = soup.find_all("div", class_="BNeawe deIvCb AP7Wnd")[1]
        team2 = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd lRVwie")[2]
        score2 = soup.find_all("div", class_="BNeawe deIvCb AP7Wnd")[2]

        ttk.Label(root, text=soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd lRVwie")[0].text).grid(column=count, row=18)
        ttk.Label(root, text=f"{team1.text}\t{score1.text}").grid(column=count, row=19)
        ttk.Label(root, text=f"{team2.text}\t{score2.text}").grid(column=count, row=20)

        count += 1

root.mainloop()
