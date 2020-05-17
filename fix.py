import sys
import os
import re

testing = False
cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
blacklist = [['Court', 'history/Court (local administrative organ).html'], ['Village', 'geographical/Village.html'], ['Castle', 'building/Castle.html']]
aliases = [['Keisuke YAMANAMI', 'Keisuke SANNAN']]

def fixPages():
	cats = ['Buddhism', 'school']
	if testing:
		cats = ['person']
	
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			filepath = cat+"/"+file
			if testing:
				filepath = 't.html' #testing
			inp = open(filepath, "r", encoding="utf8")
			content = inp.read()				
			for bl in blacklist:
				keyword = bl[0]
				link = "https://shinsengumi-archives.github.io/japanese-wiki-corpus/"+bl[1]
				content = content.replace('<a href="'+link+'">'+keyword+'</a>', keyword)
				content = content.replace('<a href="'+link+'">'+keyword.lower()+'</a>', keyword.lower())
			if testing:
				out = open("t.html", "w", encoding="utf8") #test
			else:
				out = open(filepath, "w", encoding="utf8")
			out.write(content)
			out.close()
			inp.close()
			if testing:
				break #test


fixPages()
