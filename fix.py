import sys
import os
import re

testing = False

def removeBlacklistedLinks(content):
	blacklist = [['Court', 'history/Court (local administrative organ).html'], ['Village', 'geographical/Village.html'], ['Castle', 'building/Castle.html']]
	for bl in blacklist:
		keyword = bl[0]
		link = "https://shinsengumi-archives.github.io/japanese-wiki-corpus/"+bl[1]
		content = content.replace('<a href="'+link+'">'+keyword+'</a>', keyword)
		content = content.replace('<a href="'+link+'">'+keyword.lower()+'</a>', keyword.lower())
	return content

def addAnalytics(content):
	if '- Google Analytics -->' in content:
		return content
	analytics = "<!-- Global site tag (gtag.js) - Google Analytics --> \n" \
	+"<script async src='https://www.googletagmanager.com/gtag/js?id=G-7D81XDQSVH'></script> \n" \
	+"<script> \n" \
	+" window.dataLayer = window.dataLayer || []; \n" \
	+" function gtag(){dataLayer.push(arguments);} \n" \
	+" gtag('js', new Date()); \n" \
	+" gtag('config', 'G-7D81XDQSVH'); \n" \
	+"</script>\n"
	content = content.replace('<head>\n', '<head>\n'+analytics)
	return content

def addCharset(content):
	if '<meta charset="UTF-8">' in content:
		return content
	if '<a href="https://shinsengumi-archives.github.io' in content:
		content = content.replace('<head>\n', '<head>\n<meta charset="UTF-8">\n')
	return content

def fixPages():
	cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
	if testing:
		cats = ['person']
	
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			filepath = cat+"/"+file
			if testing:
				filepath = 'Buddhism/Ashura.html' #testing
			inp = open(filepath, "r", encoding="utf8")
			content = inp.read()
			
			#content = removeBlacklistedLinks(content)
			content = addAnalytics(content)
			#content = addCharset(content)
			
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
