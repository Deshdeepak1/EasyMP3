from bs4 import BeautifulSoup
import requests
import os
import urllib
import sys
import wget
import zipfile

HOME = os.environ.get("HOME")
MusicFolder = os.path.join(HOME,'Music')
if not os.path.isdir(MusicFolder):
    os.mkdir(MusicFolder)
cp=1
while True:
    os.system('clear')
    print()
    print("**********************Welcome to EasyMP3***********************")
    print()
    print("Page ",cp)
    print()
    url = "https://downloadming3.com/category/bollywood-mp3-songs/page/"+str(cp)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    disp = soup.find_all("a",{"rel":"bookmark"})
    cc=0
    while cc<len(disp):
        print(int(cc) , " -- ",disp[cc].get_text())
        cc+=1
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
    aurl=disp[int(choice)]["href"]
    apage=requests.get(aurl)
    asoup = BeautifulSoup(apage.content, 'html.parser')
    songs_table = asoup.find_all("tr")
    songs_rows = songs_table[1:]
    os.system('clear')
    print()
    print("**********************Welcome to EasyMP3***********************")
    print()
    print(asoup.find("h1").get_text())
    print()
    ls=len(songs_rows)
    for song_row in songs_rows:
        song = song_row.find_all("td")[0]
        if song_row == songs_rows[-1]:
            print("0"+str(ls) if ls < 10 else str(ls),end=" \u2015 ")
        print(song.get_text())
    print()
    print("Enter song number to download or c to go back...")
    chosen_song=input()
    if chosen_song=="c":
        continue
    chosen_song=int(chosen_song)
    print()
    print("1. 128 Kbps")
    print("2. 320 Kbps")
    chosen_format = int(input("Enter format: "))
    surl = songs_rows[chosen_song-1].find_all("td")[chosen_format].find_next("a")["href"]
    req = urllib.request.Request(surl,headers={'Referer': 'https://downloadming3.com/'})
    myfile = urllib.request.urlopen(req)      
    if chosen_song == ls:
        print("Downloading zip file...")
        zip_file = os.path.join(MusicFolder, str(asoup.find("h1").get_text()) +'.zip')
        open(zip_file, 'wb').write(myfile.read())
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(MusicFolder)
        os.remove(zip_file)
    else:
        print("Downloading song...")
        print(surl)
        song_file = os.path.join(MusicFolder, str(songs_rows[chosen_song-1].find_all("td")[0].get_text()) +'.mp3')
        open(song_file, 'wb').write(myfile.read())
    print("Download Completed!")
