#!/usr/bin/python
# -*- coding: utf8 -*-

import json, sys, os
import nltk
import newspaper
from newspaper import Article
from datetime import datetime
import lxml, lxml.html
from playwright.sync_api import sync_playwright

sys.stdout = open(os.devnull, "w") #To prevent a function from printing in the batch console in Python

url = functionName = sys.argv[1]

def accept_cookies_and_fetch_article(url):
    # Using Playwright to handle login and fetch article
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to watch the browser actions
        page = browser.new_page()

        # create a new incognito browser context
        context = browser.new_context()
        # create a new page inside context.
        page = context.new_page()

        page.goto(url)

        # Automating iframe button click
        page.frame_locator("iframe[title=\"SP Consent Message\"]").get_by_label("Essential cookies only").click()

        content = page.content()
        # dispose context once it is no longer needed.
        context.close()
        browser.close()

    # Using Newspaper4k to parse the page content
    article = newspaper.article(url, input_html=content, language='en')
    article.parse() #Parse the article
    article.nlp()#  Keyword extraction wrapper

    return article

article = accept_cookies_and_fetch_article(url)

# article.download() #Downloads the link’s HTML content
# 1 time download of the sentence tokenizer
# perhaps better to run from command line as we don't need to install each time?
#nltk.download('all') 
#nltk.download('punkt')

sys.stdout = sys.__stdout__

data = article.__dict__
del data['config']
del data['extractor']

for i in data:
    if type(data[i]) is set:
        data[i] = list(data[i])
    if type(data[i]) is datetime:
        data[i] = data[i].strftime("%Y-%m-%d %H:%M:%S")
    if type(data[i]) is lxml.html.HtmlElement:
        data[i] = lxml.html.tostring(data[i])
    if type(data[i]) is bytes:
        data[i] = str(data[i])

print(json.dumps(data))