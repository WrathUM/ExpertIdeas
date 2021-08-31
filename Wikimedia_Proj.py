import pandas as pd
import numpy as np
import xml.etree.ElementTree as etree  #allows streaming instead of loading whole xml file
import codecs
import time
import os
import csv

#paths and filenames
PATH_WIKI_XML = ''
FILENAME_WIKI = ' '
FILENAME_ARTICLES = ' '
FILENAME_REDIRECT = ' '
FILENAME_TEMPLATE = ' '
ENCODING = "utf-8"

# convert into a formated time string to display runtime
def hms_string(sec_elapsed):
    h = int(sec_elpsased/ (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = secsec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


# allows you to strip out the namespace from tags and just keep the tag name itself
def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


pathWikiXML = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
pathArticles = os.path.join(PATH_WIKI_XML, FILENAME_ARTICLES)
pathArticlesRedirect = os.path.join(PATH_WIKI_XML, FILENAME_REDIRECT)
pathTemplateRedirect = os.path.join(PATH_WIKI_XML, FILENAME_REDIRECT)

totalCount = 0
articleCount = 0
redirectCount = 0
templateCount = 0
title = None
start_time = time.time()

with codecs.open(pathArticles, "w", ENCODING) as articlesFH, \
        codecs.open(pathArticlesRedirect, "w", ENCODING) as redirectFH, \
        codecs.open(pathTemplateRedirect, "w", ENCODING) as templateFH:
    articlesWriter = csv.writer(articlesFH, quoting = csv.QUOTE_MINIMAL)
    redirectWriter = csv.writer(redirectFH, quoting = csv.QUOTE_MINIMAL)
    templateWriter = csv.writer(templateFH, quoting = csv.QUOTE_MINIMAL)


    articleWriter.writerow(['id', 'title', 'redirect'])
    redirectWriter.writerow(['id', 'title', 'redirect'])
    templateWriter.writerow(['id', 'title'])
    
    for event, elem in etree.iterparse(pathWikiXML, events = ('start', 'end')):
        tname = strip_tag_name(elem.tag)

        if event == 'start':
            if tname == 'page':
                title = ''
                id = -1
                redirect = ''
                inrevision = False
                ns = 0
            elif tname == 'revision':
                # do not override page id for revision id right now
                inrevision = True
            elif tname == 'title':
                title = elem.text

            elif tname == 'id' and not inrevision and elem.text != None:
                id = int(elem.text)
            elif tname == 'redirect':
                redirect = elem.get('title', '')
            elif tname == 'ns' and elem.text != None:
                ns = int(elem.text)
        elif tname == 'page':
            totalCount += 1

            if ns == 10:
                templateCount += 1
                templateWriter.writerow([id, title])
            elif len(redirect) > 0:
                articleCount += 1
                articlesWriter.writerow([id, title, redirect])
            else:
                redirectCount += 1
                redirectWriter.writerow([id, title, redirect])
            if totalCount > 1 and (totalCount % 100000) == 0:
                print("{:,}".format(totalCount))

        if totalCount > 1000000:
            break
        #clears memory
        elem.clear()

time_took = time.time() - start_time
runtime = hms_string(time_took)
print("Total runtime: " + runtime)


