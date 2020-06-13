import sys
import os
import re
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
lastmod = yesterday.strftime('%Y-%m-%d')

testing = False

dataPath = '../japanese_wiki_corpus_data/'
cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
if testing:
	cats = ['Buddhism']

def run():
	sitemap = open("sitemap.xml", "w", encoding="utf8")

	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Ashura.html' #testing
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()
			
			
			sitemap.write("<url><loc>https://shinsengumi-archives.github.io/japanese-wiki-corpus/"+file+"</loc><lastmod>"+lastmod+"T03:17:57+00:00</lastmod><priority>0.64</priority></url>\n")
			
			inp.close()
			if testing:
				break #test

	sitemap.close()

run()
