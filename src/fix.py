import sys
import os
import re

testing = False
replaceFile = True
dataPath = '../japanese_wiki_corpus_data/'

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
		content = re.sub("<title>.*</title>\n", "", content)
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

def getData(content):
	istart = content.find('<body>')
	if istart == -1:
		return content
	iend = content.find('</body>')
	content = content[istart+7:iend]
	content = content.replace("<a href='https://shinsengumi-archives.github.io/japanese-wiki-corpus/'>Home</a>\n", '')
	return content

def orderName(content):
	istart = content.find('<h1>')
	if istart == -1:
		return content
	istart+=4
	iend = content.find('</h1>')
	name = content[istart:iend]
	
	roman = ['I', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX']
	
	words = name.split(' ')
	if len(words) > 2 and words[-2].isupper():
		if words[-1][0] != '(' and words[-1][-1] != ')' and words[-1] not in roman:
			words.insert(0, words.pop(-2))
		elif len(words) > 3 and words[-3].isupper(): 
			words.insert(0, words.pop(-3))
			
	name = ' '.join(words)
	return content[:istart]+name+content[iend:]

def fixPages():
	cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
	if testing:
		cats = ['person']
		
	maxlen = 0
	
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Toshizo HIJIKATA.html' #testing
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()
			
			#content = removeBlacklistedLinks(content)
			#content = addAnalytics(content)
			#content = addCharset(content)
			#content = addPageTitle(file, content)
			#content = addPageTitleCategory(cat, content)
			#content = replaceAnalyticsTrackingCode(content)
			
			#content = getData(content)
			
			#if content == "":
			#	print(filepath)
			
			#contentlen = len(content)
			#if contentlen > maxlen:
			#	maxlen = contentlen
			
			content = orderName(content)

			if replaceFile:
				if testing:
					out = open("t.html", "w", encoding="utf8") #test
				else:
					out = open(filepath, "w", encoding="utf8")
		
				out.write(content)
				out.close()
				
			inp.close()
			if testing:
				break #test

	print(maxlen)

fixPages()
