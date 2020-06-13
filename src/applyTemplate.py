import sys
import os
import re

testing = False

dataPath = '../japanese_wiki_corpus_data/'
cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
if testing:
	cats = ['Buddhism']

def filename2keyword(file):
	keyword = os.path.splitext(file)[0]
	#keyword = re.sub("[\(\[].*?[\)\]]", "", keyword)
	keyword = keyword.strip(" .")
	return keyword

def applyPageTemplate():
	templateFile = open('templates/page.html', "r", encoding="utf8")
	template = templateFile.read()
	
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Ashura.html' #testing
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()
			
			name = filename2keyword(file)
			content = template.replace('{{content}}', content)
			content = content.replace('{{name}}', name)
			content = content.replace('{{category}}', cat)
			
			if testing:
				out = open("t.html", "w", encoding="utf8") #test
			else:
				out = open(filepath, "w", encoding="utf8")
	
			out.write(content)
			out.close()
			
			inp.close()
			if testing:
				break #test


applyPageTemplate()
