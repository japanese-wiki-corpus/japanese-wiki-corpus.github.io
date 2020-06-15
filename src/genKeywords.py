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
	words = name.split(' ')
	if words[-1].isupper():
		words.insert(0, words.pop())
	return ' '.join(words)

def getLastname(kw):
	words = kw.split(' ')
	if words[0].isupper():
		return words[0].lower()
	return None

def getPageRank(keywords):
	nproc = 0
	ranks = {}
	for cat in cats:
		print(cat, flush=True)
		files = os.listdir(cat)
		for file in files:
			if testing:
				file = 'Shinsen-gumi.html' #testing
			filepath = cat+"/"+file
			inp = open(dataPath+filepath, "r", encoding="utf8")
			content = inp.read()
			content = content.lower()
			
			for kw in keywords:
				if kw not in ranks:
					ranks[kw] = 0
				ranks[kw] += content.count(' '+kw+' ')
				ranks[kw] += content.count('>'+kw+'</a>')
			
			inp.close()
			nproc+=1
			if nproc % 100 == 0:
				print(nproc, flush=True)
			if testing:
				break
	return ranks

def pageRankIncludeUnorderedNamesAndSynonyms(ranks, additional):
	for kw in synonyms:
		additional[synonyms[kw]] = kw
	print('additional kw', len(additional), flush=True)
	orderedRanks = getPageRank(additional)
	for origName in additional:
		ordered = additional[origName]
		if ordered not in ranks:
			ranks[ordered] = 0
		ranks[ordered] += orderedRanks[origName]
	with open('rank.json', 'w', encoding="utf8") as outfile:
		json.dump(ranks, outfile, ensure_ascii=False)
	return ranks

def run():
	keywords = {}
	orderedNames = {}
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
			if len(kw) < 3:
				continue
			
			ordered = orderName(kw)
			lastname = getLastname(ordered)
			kw = kw.lower()
			ordered = ordered.lower()
			
			if ordered != kw:
				orderedNames[kw] = ordered
			kw = ordered
			
			nlinks = getNLinks(content)
			
			if kw not in keywords:
				keywords[kw] = 1
				#if lastname or cat=='history':
				#	keywords[kw] = 1000 # boost people, history
			keywords[kw] += nlinks
			
			if lastname:
				if len(lastname) < 3:
					continue
				if lastname not in keywords or keywords[lastname] <= nlinks:
					keywords[lastname] = nlinks+2

			inp.close()
			if testing:
				break
	
	ranks = {}
	if not os.path.isfile('rank.json'):
		print('page rank', flush=True)
		ranks = getPageRank(keywords)
		with open('rank.json', 'w', encoding="utf8") as outfile:
			json.dump(ranks, outfile, ensure_ascii=False)
	else:
		with open('rank.json', encoding='utf8') as f:
			ranks = json.load(f)
		
	#ranks = pageRankIncludeUnorderedNamesAndSynonyms(ranks, orderedNames)

	for kw in keywords:
		if kw in ranks:
			keywords[kw] = keywords[kw] + ranks[kw]
		
	for kw in synonyms:
		if kw not in keywords:
			print(kw)
		keywords[synonyms[kw]] = keywords[kw] + 1
	
	nkw = len(keywords)
	print(nkw)
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
	
	out.write('</Autocompletions>\n')
	out.close()


run()
