import sqlite3
from pathlib import Path
import subprocess
import os

dbname = "data.db"
dbfolder = "db/"
Path(dbfolder).mkdir(parents=True, exist_ok=True)

# Connect to the SQL server
def sqlite_connect():
    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)

# Create the SQL database
def init_sqlite():
    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE googles (term text)''')
    conn.close()

# Write phrase to db
def write(term):
    sqlite_connect()
    c = conn.cursor()
    c.execute('''INSERT INTO googles('term') VALUES(?)''', [(term)])
    conn.commit()
    conn.close()



def chromeKill():
    subprocess.run(["taskkill","/f","/im","chrome.exe"])

def getDir():
    stream = os.popen('echo %appdata%')
    dir = stream.read().replace("\\Roaming\n","")
    dir = dir + '\\Local\\Google\\Chrome\\User Data\\Default\\History'
    return dir

def getURLs():
    dir = getDir()
    chromeKill()
    con = sqlite3.connect(dir)
    cursor = con.cursor()
    cursor.execute("SELECT url FROM urls")
    urls = cursor.fetchall()
    return urls

def parseURLs(urls):
    googles = []
    for url in urls:
        if "https://www.google.com/search?q=" in url[0]:
            data = url[0].replace("https://www.google.com/search?q=","")
            data = data.split("&")[0].replace("+"," ")
            if "python" in data:
                googles.append(data)
    for term in googles:
        write(term)
    print("Done.")

def main():
    try:
        init_sqlite()
    except:
        pass
    urls = getURLs()
    parseURLs(urls)

main()
