import sys
import os
import json
import re
from string import ascii_uppercase

testing = False

dataPath = '../japanese_wiki_corpus_data/'
cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']


def revert():
	
	with open('data.json', encoding='utf8') as f:
		data = json.load(f)
	
	for cat in cats:
		print(cat, flush=True)
		pages = data[cat]
		for page in pages:

			output = '<h1>'+page['name']+' ('+page['jp']+')</h1>\n'
			pageFile = open(page['url'], "r", encoding="utf8")
			pageContent = pageFile.read()
			
			istart = pageContent.index('<div class="social"')
			pageContent = pageContent[istart:]
			istart = pageContent.index('</div>') + 6
			pageContent = pageContent[istart:]
			istart = pageContent.index('</div>') + 6
			content = pageContent[istart:]
			
			istart = content.find('<ins')
			if istart >= 0:
				iend = content.index('</ins>') + 6
				content = content[:istart]+content[iend:]
				
			iend = content.index('<div class="social"')
			content = content[:iend]
			
			content = content.replace('\n\n\n', '')
			content = content.replace('\n\n', '')
			
			output = output + content + '\n'
			
			filepath = page['url']
			out = open(dataPath+filepath, "w", encoding="utf8")	
			out.write(output)
			out.close()
			
revert()
