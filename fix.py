import sys
import os
import re

testing = False

def filename2keyword(file):
	keyword = os.path.splitext(file)[0]
	keyword = re.sub("[\(\[].*?[\)\]]", "", keyword)
	keyword = keyword.strip(" .")
	return keyword

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

def addPageTitle(file, content):
	if "<title" in content:
		return content
	title = filename2keyword(file)
	title = "<title>"+title+"</title>\n"
	content = content.replace('<head>\n', '<head>\n'+title)
	return content

def addPageTitleCategory(cat, content):
	if ")</title>" in content:
		return content
	title = " ("+cat+")</title>"
	content = content.replace('</title>', title)
	return content

def replaceAnalyticsTrackingCode(content):
	content = content.replace('G-7D81XDQSVH', 'UA-157500608-2')
	return content

def fixPages():
	cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
	if testing:
		cats = ['Buddhism']
	
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Ashura.html' #testing
			filepath = cat+"/"+file
			inp = open(filepath, "r", encoding="utf8")
			content = inp.read()
			
			#content = removeBlacklistedLinks(content)
			#content = addAnalytics(content)
			#content = addCharset(content)
			#content = addPageTitle(file, content)
			#content = addPageTitleCategory(cat, content)
			content = replaceAnalyticsTrackingCode(content)
			
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
