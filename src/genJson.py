import sys
import os
import re
from datetime import datetime, timedelta
import math

testing = False

yesterday = datetime.now() - timedelta(days=1)
lastmod = yesterday.strftime('%Y-%m-%d')

maxlen = 179707.0
dataPath = '../japanese_wiki_corpus_data/'
cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
if testing:
	cats = ['Buddhism']

def run():
	sitemap = open("sitemap.xml", "w", encoding="utf8")
	sitemap.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')

	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Ashura.html' #testing
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()
			
			priority = math.exp(len(content)/maxlen) / math.e
			sitemap.write("<url><loc>https://shinsengumi-archives.github.io/japanese-wiki-corpus/"+file+"</loc><lastmod>"+lastmod+"T03:17:57+00:00</lastmod><priority>"+str(priority)+"</priority></url>\n")
			
			inp.close()
			if testing:
				break #test

	sitemap.write("</urlset>\n")
	sitemap.close()

run()
