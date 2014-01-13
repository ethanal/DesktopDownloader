#!/usr/local/bin/python3

import html.parser
import os
import re
import requests


h = html.parser.HTMLParser()

def clean_filename(filename):
    return h.unescape(filename).replace("/", "-")

def add_suffix(n, filename):
    if suffix == 0:
        return filename

    name = ".".join(filename.split(".")[:-1])
    extension = filename.split(".")[-1]
    return name + " " + str(suffix) + "." + extension

image_dir = "Desktops"

os.system("mkdir -p {}".format(image_dir))

if os.path.exists("last_downloaded"):
    with open("last_downloaded", "r+") as f:
        last_downloaded = f.read().strip()
else:
    last_downloaded = ""

new_last_downloaded = ""
page_number = 1
finished = False

while not finished:
    browse_page = "".join(requests.get("http://simpledesktops.com/browse/{}".format(page_number)).text.split("\n"))
    images = re.findall(r"(http://static\.simpledesktops\.com/uploads/desktops/[0-9]{4}/[0-9]{2}/[0-9]{2}/[^\"]*)\" title=\"([^\"]*)\"", browse_page)
    if len(images):
        for url, name in images:
            url = ".".join(url.split(".")[:-2])  # Remove thumbnail dimensions
            if url == last_downloaded:
                finished = True
                break

            if new_last_downloaded == "":
                new_last_downloaded = url

            filename = name + "." + url.split("/")[-1].split(".")[-1]

            suffix = 0
            while os.path.isfile(os.path.join(image_dir, clean_filename(add_suffix(suffix, filename)))):
                suffix += 1
            filename = clean_filename(add_suffix(suffix, filename))

            img_response = requests.get(url, stream=True)
            print("Downloading \"{}\"".format(filename))

            with open(os.path.join(image_dir, filename), "wb") as img_file:
                img_file.write(img_response.content)
        page_number += 1
    else:
        finished = True

if new_last_downloaded != "":
    with open("last_downloaded", "w") as f:
        f.write(new_last_downloaded)

print("All desktops downloaded")
