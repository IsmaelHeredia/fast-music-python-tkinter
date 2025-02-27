#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written by Ismael Heredia

from bs4 import BeautifulSoup
import requests

class googleSearch(object):

    def send_first_result(self,string):

        headers_conf = {
            "Accept" : "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

        content = requests.get("https://www.google.com/search", headers = headers_conf, params = {"q": string}).text
        soup = BeautifulSoup(content, "html.parser")
        links = soup.find(id = "search")
        return links.find("a")["href"]
