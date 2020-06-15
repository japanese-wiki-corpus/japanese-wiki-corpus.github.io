import sys
import os
import xml.etree.ElementTree as ET
import json

testing = False

cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
if testing:
	cats = ['school']

dataPath = '../japanese_wiki_corpus_data/'

def filename2keyword(file):
	keyword = os.path.splitext(file)[0]
	keyword = re.sub("[\(\[].*?[\)\]]", "", keyword)
	keyword = keyword.strip(" .")
	return keyword

def getPageRank(content):
	start = 0
	links = {}
    while True:
        start = content.find('<a href=', start)
        if start == -1 or start > len(content): return
		
		i1 = content.find('>', start) + 1
		i2 = content.find('</a>', start)
		links.add(content[i1:i2])

        start += 1

	return len(links)

def getLastname(kw):
	words = kw.split(' ')
	if words[-1].isupper():
		return words[-1]
	return None

def run():
	keywords = {}
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Ashura.html' #testing
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()
			
			kw = filename2keyword(file)
			rank = getPageRank(content)
			
			lastname = getLastname(kw)
			kw = kw.lower()
			if kw not in keywords:
				keywords[kw] = 1
			keywords[kw] += rank
			
			if lastname:
				if lastname not in keywords:
					keywords[lastname] = 2
				keywords[lastname] += rank
			inp.close()
			
			if testing:
				break
	
	nkw = len(keywords)
	print(nkw)
	out = open('keywords.xml', "w", encoding="utf8")	
	out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	out.write('<Autocompletions start="0" num="'+str(nkw)+'" total="'+str(nkw)+'">\n')

	for kw in keywords.keys():
		if keywords[kw] > 10000:
			keywords[kw] = 10000
		out.write('<Autocompletion term="'+kw+'" type="1" match="1" score="'+str(keywords[kw])+'"/>\n')
	
	out.write('</Autocompletions>\n')
	out.close()


run()
