from bs4 import BeautifulSoup
from clint.textui import progress
import requests
import os
import sys
import wget
os.system('clear')
cp=1
while True:
    print("Page ",cp)
    url = "https://downloadming2.com/category/bollywood-mp3/page/"+str(cp)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all("a",{"class":"more-link"})
    cc=0
    for i in links:
        print(cc , " -- ",i["href"])
        cc+=1
    print("Enter choice... or n/p for next/previous page")
    choice = input()
    if choice=="n":
        cp+=1
        continue
    if choice=="p":
        cp-=1
        continue
    aurl=links[int(choice)]["href"]
    apage=requests.get(aurl)
    asoup = BeautifulSoup(apage.content, 'html.parser')
    songs = asoup.find_all("td")
    songs.pop()
    cs=0
    for ii in songs:
        if cs>0 and cs%3==0:
            print(ii.get_text())
        cs+=1
    print("Enter option...")
    chosen_song=int(input())
    surl=songs[3*chosen_song+1].find("a")["href"]
    print("Downloading...")
    myfile = requests.get(surl)
    open('/home/amulya/Music/'+ str(songs[3*chosen_song].get_text()) +'.mp3', 'wb').write(myfile.content)
    print("Download Completed.")