"""
MIT License
Copyright (c) 2017 Uka Osim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import sys
import urllib2
import re
import json

# Used the regex library to make it easier for third party to test the main code
# there are python libraries that make it easier to parse html file
# e.g BeautifulSoup (Third Party), HTMLParser etc...


# a regular to capture the headline of the html page
title_regex = re.compile("<title>(.+?)</title>")

# a regular expression to capture image links and caption on the html page
image_caption_regex = re.compile("(<img.+?src=[\"'](.+?)[\"'].*?>)|(<img.+?alt=[\"'](.+?)[\"'].*?>)")

# a regular expression to capture image links
image_regex = re.compile("<img.+?src=[\"'](.+?)[\"'].*?>")

# a regular expression to capture image caption
caption_regex = re.compile("<img.+?alt=[\"'](.+?)[\"'].*?>")


def process_image_regex(result):
    image = re.findall(image_regex, result)
    if image:
        # should only contain one list item
        return image[0]


def process_caption_regex(result):
    # should only contain one list item
    caption = re.findall(caption_regex, result)
    if caption:
        # should only contain one list item
        return caption[0]


def url_scraper(urls):

    # make sure that a list of urls is used at all times, e.g if a string was passed as an argument
    if not isinstance(urls, list):
        urls = urls.split()
    # a python list to store all the python dictionaries in the json structure
    json_container = []
    # a container to store the header containers (urls, headline, images)
    header_container = {}
    # a container which stores the images with the best caption
    img_container = {}
    for url in urls:
        url = url.replace("\n", "")
        response = urllib2.urlopen(url)
        # returns html string
        html = response.read()
        title = re.findall(title_regex, html)
        # a set is used here to remove duplicates
        image_urls = list(set(re.findall(image_caption_regex, html)))
        header_container["url"] = url
        header_container["headline"] = title[0]
        # initial the image list containing the image URL and caption
        header_container["images"] = []
        for image_info in image_urls:
            # when we have no caption for the image url, skip it, i.e. None value
            if not process_caption_regex(image_info[0]):
                continue
            img_container["url"] = process_image_regex(image_info[0])
            img_container["caption"] = process_caption_regex(image_info[0])
            if img_container not in header_container["images"]:
                header_container["images"].append(img_container)
            # reset 'img_container' keys to null(None) for the next image (url,caption)
            img_container = {"url": None, "caption": None}
        json_container.append(header_container)
        # reset the header container keys to null(None) for the next url
        header_container = {
            "url": None,
            "headline": None,
            "image": None
        }
    return json_container


def json_output(l):
    with open('data.json', 'w') as outfile:
        json.dump(l, outfile, indent=2)


if __name__ == "__main__":
    stream = sys.stdin
    urls = stream.readlines()
    json_list = url_scraper(urls)
    json_output(json_list)

# ------ testing ------
# python url_site_scraping.py < urls.txt
