import sys
import os
import json
from string import ascii_uppercase

testing = False

dataPath = '../japanese_wiki_corpus_data/'
cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
if testing:
	cats = ['emperor']

catDisplay = {'Buddhism': 'Buddhism', 'building': 'Buildings', 'culture': 'Culture', 'emperor': 'Emperors', 'family': 'Clans', 'geographical': 'Locations', 'history': 'History', 'literature': 'Literature', 'person': 'Historical Figures', 'railway': 'Railways', 'road': 'Roads', 'shrines': 'Shrines', 'school': 'Schools', 'Shinto': 'Shinto', 'title': 'Titles'}
endPrefixes = [] # ['cloistered imperial prince ', 'imperial prince ', 'imperial prince and monk', 'imperial princess ', 'emperor ', 'empress ', 'empress dowager ']
ignorePrefixes = ['the ', 'a ']
ignorePrefixes.extend(endPrefixes)

def filename2keyword(file):
	keyword = os.path.splitext(file)[0]
	#keyword = re.sub("[\(\[].*?[\)\]]", "", keyword)
	keyword = keyword.strip(" .")
	return keyword

def orderName(name):
	roman = ['I', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX']
	words = name.split(' ')
	if words[-1].isupper():
		if words[-1][0] != '(' and words[-1][-1] != ')' and words[-1] not in roman:
			words.insert(0, words.pop())
		elif len(words) > 2 and words[-2].isupper(): 
			words.insert(0, words.pop(-2))
	return ' '.join(words)

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
			
			name = orderName(filename2keyword(file))
			content = template.replace('{{content}}', content)
			content = content.replace('{{name}}', name)
			content = content.replace('{{category}}', cat)
			
			content = content.replace('https://shinsengumi-archives.github.io/japanese-wiki-corpus/', 'https://japanese-wiki-corpus.github.io/')
			
			if testing:
				out = open("t.html", "w", encoding="utf8") #test
			else:
				out = open(filepath, "w", encoding="utf8")
	
			out.write(content)
			out.close()
			
			inp.close()
			if testing:
				break #test
				
	templateFile.close()

def prepPageNameSort(name):
	n = name.lower()
	for prefix in ignorePrefixes:
		if n.startswith(prefix):
			i = len(prefix)
			if prefix in endPrefixes:
				name += ' (' + name[0:i-1] + ')'
			name = name[i:]
	name = name[0].upper() + name[1:]
	return name

def applyCategoryTemplate():
	templateFile = open('templates/category.html', "r", encoding="utf8")
	template = templateFile.read()
	
	listTemplateFile = open('templates/category-list.html', "r", encoding="utf8")
	listTemplate = listTemplateFile.read()
	
	with open('data.json', encoding='utf8') as f:
		data = json.load(f)
	
	for cat in cats:
		print(cat, flush=True)
		
		pages = sorted(data[cat], key=lambda k: prepPageNameSort(k['name']).lower()) 
		
		items = {}
		for page in pages:
			name = prepPageNameSort(page['name'])
			letter = name[0].upper()
			if not letter.isalpha():
				letter = '?'
			
			# <p><a href='school/Kyoto University.html'>Kyoto University</a> (jp name) - University</p>
			line = "<p><a href='"+page['url']+"'>"+name+'</a> ('+page['jp']+') - '+page['desc']+'</p>\n'
			if letter not in items:
				items[letter] = ''
			items[letter] += line
		
		allItems = ""
		letters = ""
		if '?' in items:
			list = listTemplate.replace('{{letter}}', 'other')
			list = list.replace('{{letter-upper}}', '?')
			list = list.replace('{{items}}', items['?'])
			allItems += list
			letters += '<a href="#other" class="page-scroll"><button type="button" class="btn btn-light">?</button></a>\n'
		
		for letter in ascii_uppercase: 
			list = listTemplate.replace('{{letter}}', letter.lower())
			list = list.replace('{{letter-upper}}', letter)
			if letter in items:
				list = list.replace('{{items}}', items[letter])
			else:
				list = list.replace('{{items}}', '')
			allItems += list
			
			# <a href="#other" class="page-scroll"><button type="button" class="btn btn-light">?</button></a>
			letters += '<a href="#'+letter.lower()+'" class="page-scroll"><button type="button" class="btn btn-light">'+letter+'</button></a>\n'

		content = template.replace('{{category}}', cat)
		content = content.replace('{{category-display}}', catDisplay[cat])
		content = content.replace('{{letters}}', letters)
		content = content.replace('{{list}}', allItems)
		
		content = content.replace('https://shinsengumi-archives.github.io/japanese-wiki-corpus/', 'https://japanese-wiki-corpus.github.io/')
		
		if testing:
			out = open("t.html", "w", encoding="utf8") #test
		else:
			out = open(cat+'.html', "w", encoding="utf8")

		out.write(content)
		out.close()

		if testing:
			break #test
	
	listTemplateFile.close()	
	templateFile.close()

applyPageTemplate()
applyCategoryTemplate()
