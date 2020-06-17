import sys
import os
import re

testing = True
cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
blacklist = ['Court', 'Village', 'Castle']
aliases = [['Keisuke YAMANAMI', 'Keisuke SANNAN']]

def filename2keyword(file):
	keyword = os.path.splitext(file)[0]
	keyword = re.sub("[\(\[].*?[\)\]]", "", keyword)
	keyword = keyword.strip(" .")
	return keyword

def getKeywords():
	keywords = {}
	for cat in cats:
		files = os.listdir(cat)
		for file in files:
			keyword = filename2keyword(file)
			if len(keyword) < 5 or len(keyword) == 100:
				continue
			if keyword in blacklist:
				continue
			link = "https://japanese-wiki-corpus.github.io/"+cat+"/"+file
			keywords[keyword] = link
			if len(keyword.split()) == 1:
				keyword = keyword.lower()
				keywords[keyword] = "https://japanese-wiki-corpus.github.io/"+cat+"/"+file
	for alias in aliases:
		keywords[alias[0]] = keywords[alias[1]]
	return keywords

def linkPages(keywords):
	keys = list(keywords.keys())
	keys.sort(key=len, reverse=True)
	progress = 0

	cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
	if testing:
		cats = ['person']
	
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Mototoyo HIROHATA.html' #testing
			filepath = cat+"/"+file
			inp = open(filepath, "r", encoding="utf8")
			content = inp.read()
			if '<meta charset="UTF-8">' in content:
				continue
			content = content.replace('<head>\n', '<head>\n<meta charset="UTF-8">\n')
			for keyword in keys:
				if keyword.lower() == filename2keyword(file).lower():
					continue
				content = re.sub(r"([^-{])(\b%s\b)([^}-][^A-Z])" % re.escape(keyword), r'\1{'+keyword+r'}\3', content)
			for keyword in keys:
				content = content.replace("{"+keyword+"}", '<a href="'+keywords[keyword]+'">'+keyword+'</a>')
			if testing:
				out = open("t.html", "w", encoding="utf8") #test
			else:
				out = open(filepath, "w", encoding="utf8")
			out.write(content)
			out.close()
			inp.close()
			progress+=1
			if progress % 10 == 0:
				print(progress, flush=True)
			if testing:
				break #test


keywords = getKeywords()
print(len(keywords), flush=True)
linkPages(keywords)
