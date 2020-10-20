"""
Download songs from https://downloadming3.com
"""

import os
import sys
import urllib.request
import zipfile
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

HOME = os.environ.get("HOME")
MusicFolder = os.path.join(HOME, 'Music')
if not os.path.isdir(MusicFolder):
    os.mkdir(MusicFolder)


def download_song(song_url, song_file, is_zip):
    """
    Download the chosen song or all songs.
    """
    hdr = {'Referer': 'https://downloadming3.com/'}
    total = int(requests.head(song_url, headers=hdr).headers['Content-Length'])
    req = urllib.request.Request(song_url, headers=hdr)
    web_file = urllib.request.urlopen(req)
    with open(song_file, 'wb') as file, tqdm(
            desc=os.path.basename(song_file),
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as progress_bar:
        while True:
            data = web_file.read(1024)
            if not data:
                break
            size = file.write(data)
            progress_bar.update(size)
    if is_zip:
        with zipfile.ZipFile(song_file, 'r') as zip_ref:
            zip_ref.extractall(MusicFolder)
        os.remove(song_file)


def show_song_page(page_num, songs_page):
    """
    Shows songs list of the chosen movie and prompts song choice.
    """
    songs_soup = BeautifulSoup(songs_page.content, 'html.parser')
    songs_table = songs_soup.find_all("tr")
    songs_rows = songs_table[1:]
    os.system('clear')
    print()
    print(
        "********************** \
        Welcome to EasyMP3 \
        ***********************")
    print()
    print(songs_soup.find("h1").get_text())
    print()
    songs_nums = len(songs_rows)
    for song_row in songs_rows:
        song = song_row.find_all("td")[0]
        if song_row == songs_rows[-1]:
            print("0"+str(songs_nums) if songs_nums < 10 else str(songs_nums),
                  end=" \u2015 ")
        print(song.get_text())
    print()
    print("Enter song number to download or b to go back or e to exit ")

    def choose_song():
        chosen_song = input()
        if chosen_song == "b":
            main(page_num)
        elif chosen_song == "e":
            sys.exit()
        elif chosen_song.isdigit() and int(chosen_song) <= len(songs_rows):
            return int(chosen_song)
        print("Invalid choice. Please enter choice again.")
        return choose_song()
    chosen_song = choose_song()
    print()
    print("1. 128 Kbps")
    print("2. 320 Kbps")

    def choose_format():
        chosen_format = input("Enter format: ")
        if chosen_format.isdigit() and int(chosen_format) in [1, 2]:
            return int(chosen_format)
        print("Invalid choice. Please enter choice again.")
        return choose_format()
    chosen_format = choose_format()
    song_url = songs_rows[
        chosen_song - 1
    ].find_all("td")[chosen_format].find_next("a")["href"]
    if chosen_song == songs_nums:
        print("Downloading zip file...")
        download_song(song_url,
                      os.path.join(MusicFolder, str(
                          songs_soup.find("h1").get_text()) + '.zip'),
                      is_zip=True)

    else:
        print("Downloading song...")
        download_song(song_url,
                      os.path.join(MusicFolder, str(
                          songs_rows[chosen_song-1].find_all(
                              "td")[0].get_text()) + '.mp3'),
                      is_zip=False)


def main(page_num):
    """
    Shows movies list and prompts movie choice.
    """
    os.system('clear')
    print()
    print(
        "********************** \
        Welcome to EasyMP3 \
        ***********************")
    print()
    print("Page ", page_num)
    print()
    url = "https://downloadming3.com/category/bollywood-mp3-songs/page/" + \
        str(page_num)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    movies_list = soup.find_all("a", {"rel": "bookmark"})
    for movie in enumerate(movies_list):
        print(movie[0], " -- ", movie[1].get_text())
    print()
    print("Enter choice... or n/p for next/previous page... or e to exit")

    def choose_movie():
        choice = input()
        if choice == "e":
            sys.exit()
        elif choice == "n":
            main(page_num+1)
        elif choice == "p":
            main(max(1, page_num-1))
        elif choice.isdigit() and int(choice) < len(movies_list):
            songs_url = movies_list[int(choice)]["href"]
            songs_page = requests.get(songs_url)
            show_song_page(page_num, songs_page)
        else:
            print("Invalid choice. Please enter choice again.")
            choose_movie()
    choose_movie()


if __name__ == "__main__":
    main(1)
