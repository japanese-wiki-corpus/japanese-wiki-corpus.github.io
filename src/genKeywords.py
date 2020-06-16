import sys
import os
import json

testing = False

cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
if testing:
	cats = ['history']

dataPath = '../japanese_wiki_corpus_data/'

illegal = ['(', '[']

synonyms = {'shinsen-gumi': 'shinsengumi', 'sannan': 'yamanami', 'sannan keisuke': 'yamanami keisuke'}
orderedSynonyms = {'yamanami keisuke': 'keisuke yamanami'}
replacePrefixes = {'the ': '', 'a ': '', 'cloistered imperial prince ': 'prince ', 'imperial prince ': 'prince ', 'imperial princess ': 'princess '}
unreplacePrefixes = ['the ']
addedKeywords = ['cloistered imperial prince', 'imperial princess', '53 stations of tokaido road']

def filename2keyword(file):
	keyword = os.path.splitext(file)[0]
	
	for c in illegal:
		i = keyword.find(c)
		if i != -1:
			keyword = keyword[:i]
	
	keyword = keyword.strip(" .")
	return keyword

def getNLinks(content):
	start = 0
	links = set([])
	while True:
		start = content.find('<a href=', start)
		if start == -1 or start > len(content): break

		i1 = content.find('>', start) + 1
		i2 = content.find('</a>', start)
		links.add(content[i1:i2])

		start += 1

	return len(links)

def orderName(name):
	roman = ['I', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX']
	words = name.split(' ')
	if words[-1].isupper():
		if words[-1][0] != '(' and words[-1][-1] != ')' and words[-1] not in roman:
			words.insert(0, words.pop())
		elif len(words) > 2 and words[-2].isupper(): 
			words.insert(0, words.pop(-2))
	return ' '.join(words)

def getLastname(kw):
	words = kw.split(' ')
	if len(words) > 1 and words[0].isupper() and words[0][0] != '(':
		return words[0].lower()
	return None

def getPageRank(keywords, additional):
	keys = set(keywords.keys())
	keys.update(additional.values())
	keys.update(synonyms.values())
	keys.update(orderedSynonyms.values())
	
	ranks = {}
	if os.path.isfile('rank.json'):
		with open('rank.json', encoding='utf8') as f:
			ranks = json.load(f)
	
	for kw in ranks:
		keys.discard(kw)
	
	print(len(keys), 'keys', flush=True)
	
	if len(keys) == 0:
		return ranks
	
	if testing:
		keys = set(synonyms.values())
		keys.update(synonyms.keys())

	nproc = 0
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()
			content = content.lower()
			
			for kw in keys:
				if kw not in ranks:
					ranks[kw] = 0
				ranks[kw] += content.count(' '+kw+' ')
				ranks[kw] += content.count('>'+kw+'</a>')
			
			inp.close()
			nproc+=1
			if nproc % 100 == 0:
				print(nproc, flush=True)

		with open('rank.json', 'w', encoding="utf8") as outfile:
			json.dump(ranks, outfile, ensure_ascii=False)
	
	return ranks

def run():
	keywords = {}
	orderedNames = {}
	
	for kw in addedKeywords:
		keywords[kw] = 1
		
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Shinsen-gumi.html' #testing
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()
			
			kw = filename2keyword(file)
			if len(kw) < 3 or len(kw) > 30:
				continue
			
			ordered = orderName(kw)
			lastname = getLastname(ordered)
			kw = kw.lower()
			ordered = ordered.lower()
			
			if not kw.isascii():
				continue
				
			nlinks = getNLinks(content)
			
			if ordered != kw:
				orderedNames[ordered] = kw
				kw = ordered
			
			for prefix in replacePrefixes:
				if kw.startswith(prefix):
					if prefix in unreplacePrefixes:
						if kw not in keywords:
							keywords[kw] = 1
						keywords[kw] += nlinks
					kw = replacePrefixes[prefix] + kw[len(prefix):]
			
			if kw not in keywords:
				keywords[kw] = 1
			keywords[kw] += nlinks
			
			if lastname:
				if len(lastname) < 3:
					continue
				if lastname not in keywords or keywords[lastname] <= nlinks:
					keywords[lastname] = nlinks+2

			inp.close()
			if testing:
				break
	
	ranks = getPageRank(keywords, orderedNames)

	for kw in keywords:
		sum = ranks[kw]
		if kw in synonyms:
			sum += ranks[synonyms[kw]]
			if synonyms[kw] in orderedSynonyms:
				sum += ranks[orderedSynonyms[synonyms[kw]]]
		if kw in orderedNames:
			sum += ranks[orderedNames[kw]]
		ranks[kw] = sum

	for kw in keywords:
		if kw in ranks:
			keywords[kw] = keywords[kw] + ranks[kw]
	
	for kw in synonyms:
		keywords[synonyms[kw]] = keywords[kw] + 1
	
	with open(dataPath+'suggestions.xml', "r", encoding="utf8") as f:
		oldSuggestions = f.read()
		
	nkw = len(keywords)
	print(nkw)
	
	removedKw = ""
	oldKw = oldSuggestions.split('\n')
	for old in oldKw[2:]:
		i = old.find('"')
		# skip excluded terms '<Autocompletion term="a plot of usa hachiman-gu oracle" type="2" match="1"/>'
		if i == -1 or old.find('score="') == -1:
			continue
		old = old[i+1:]
		i = old.find('"')
		old = old[:i]
		if old not in keywords:
			nkw += 1
			removedKw += '<Autocompletion term="'+old+'" type="1" match="1" score="0"/>\n'

	out = open('keywords.xml', "w", encoding="utf8")	
	out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	out.write('<Autocompletions start="0" num="'+str(nkw)+'" total="'+str(nkw)+'">\n')

	maxscore = 0
	for kw in keywords:
		if keywords[kw] > 10000:
			keywords[kw] = 10000
		if keywords[kw] == 0:
			keywords[kw] = 1
		out.write('<Autocompletion term="'+kw+'" type="1" match="1" score="'+str(keywords[kw])+'"/>\n')
		if keywords[kw] > maxscore:
			maxscore = keywords[kw]
	
	print(maxscore)
	
	
	out.write(removedKw)
	out.write('</Autocompletions>\n')
	out.close()


run()
