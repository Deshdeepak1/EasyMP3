from bs4 import BeautifulSoup
import requests
import os
import sys
import wget
import zipfile

cp=1
while True:
    os.system('clear')
    print()
    print("**********************Welcome to EasyMP3***********************")
    print()
    print("Page ",cp)
    print()
    url = "https://downloadming2.com/category/bollywood-mp3/page/"+str(cp)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all("a",{"class":"more-link"})
    disp = soup.find_all("a",{"rel":"bookmark"})
    cc=0
    while cc<len(disp):
        print(int(cc/2) , " -- ",disp[cc].get_text())
        cc+=2
    print()
    print("Enter choice... or n/p for next/previous page... or e to exit")
    choice = input()
    if choice=="n":
        cp+=1
        continue
    if choice=="p":
        cp=max(1,cp-1)
        continue
    if choice=="e":
        break
    aurl=links[int(choice)]["href"]
    apage=requests.get(aurl)
    asoup = BeautifulSoup(apage.content, 'html.parser')
    songs = asoup.find_all("td")
    songs.pop()
    cs=0
    os.system('clear')
    print()
    print("**********************Welcome to EasyMP3***********************")
    print()
    print(asoup.find("h1").get_text())
    print()
    ls=len(songs)/3 
    ls=ls-1
    for ii in songs:
        if cs>0 and cs%3==0:
            print(ii.get_text())
        cs+=1
    print()
    print("Enter song number to download or c to go back...")
    chosen_song=input()
    if chosen_song=="c":
        continue
    chosen_song=int(chosen_song)
    surl=songs[3*chosen_song+1].find("a")["href"]
    if chosen_song == ls:
        print("Downloading zip file...")
        myfile = requests.get(surl)
        open('/home/amulya/Music/'+ str(asoup.find("h1").get_text()) +'.zip', 'wb').write(myfile.content)
        with zipfile.ZipFile('/home/amulya/Music/'+ str(asoup.find("h1").get_text()) +'.zip', 'r') as zip_ref:
            zip_ref.extractall('/home/amulya/Music')
        os.remove('/home/amulya/Music/'+ str(asoup.find("h1").get_text()) +'.zip')
    else:
        print("Downloading song...")
        myfile = requests.get(surl)
        open('/home/amulya/Music/'+ str(songs[3*chosen_song].get_text()) +'.mp3', 'wb').write(myfile.content)
    print("Download Completed!")
