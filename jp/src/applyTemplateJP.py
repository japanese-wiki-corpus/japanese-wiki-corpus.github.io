import sys
import os
import json
from string import ascii_uppercase

testing = False

dataPath = '../../japanese_wiki_corpus_data_jp/'
cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
if testing:
	cats = ['Buddhism']

catDisplay = {'Buddhism': 'Buddhism', 'building': 'Buildings', 'culture': 'Culture', 'emperor': 'Emperors', 'family': 'Clans', 'geographical': 'Locations', 'history': 'History', 'literature': 'Literature', 'person': 'Historical Figures', 'railway': 'Railways', 'road': 'Roads', 'shrines': 'Shrines', 'school': 'Schools', 'Shinto': 'Shinto', 'title': 'Titles'}
endPrefixes = [] # ['cloistered imperial prince ', 'imperial prince ', 'imperial prince and monk', 'imperial princess ', 'emperor ', 'empress ', 'empress dowager ']
ignorePrefixes = ['the ', 'a ']
ignorePrefixes.extend(endPrefixes)
responsiveAd = '\n<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-6625151359627561" data-ad-slot="2955832603" data-ad-format="auto" data-full-width-responsive="true"></ins>\n'

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
	if words[0].isupper() and words[0][0] != '(' and words[0][-1] != ')' and words[0] not in roman:
		words[0] = words[0].capitalize()
	return ' '.join(words)

def applyPageTemplate():
	templateFile = open('templates/page.html', "r", encoding="utf8")
	template = templateFile.read()
	
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if file == 'Shinsen-gumi.html':
				continue
			if testing:
				file = '一心院.html' #testing
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()

			lines = content.split("\n")
			title = lines[0]
			content = "\n".join(lines[1:])
			sanitized = content.replace('"', '&quot;').replace('<p></p>', '')
			
			name = orderName(filename2keyword(file))
			content = template.replace('{{content}}', content)
			content = content.replace('{{name}}', name)
			content = content.replace('{{category}}', cat)
			content = content.replace('{{url}}', 'jp/'+cat+'/'+name+'html')
			content = content.replace('{{category-display}}', catDisplay[cat])
			content = content.replace('{{sanitized}}', sanitized)
			
			content = content.replace('https://shinsengumi-archives.github.io/japanese-wiki-corpus/', 'https://www.japanese-wiki-corpus.org/')
			
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


applyPageTemplate()
