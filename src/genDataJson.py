import sys
import os
import xml.etree.ElementTree as ET
import json

testing = False

cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
if testing:
	cats = ['school']

illegal = ['NUL','\',''//',':','*','"','<','>','|', '/', "'"]

def get_sentences(sa, sens):
	first_id = None
	for sen in sens:
		txt = sen.findall("e")[-1].text
		if txt is not None:
			id = int(sen.attrib["id"])
			sa[id] = txt
			if not first_id:
				first_id = id
			break
	return first_id

def orderName(name):
	roman = ['I', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX']
	words = name.split(' ')
	if words[-1].isupper():
		if words[-1][0] != '(' and words[-1][-1] != ')' and words[-1] not in roman:
			words.insert(0, words.pop())
		elif len(words) > 2 and words[-2].isupper(): 
			words.insert(0, words.pop(-2))
	return ' '.join(words)

def parse(fn, jp, cat):
	inp = open("../japanese_wiki_corpus_orig/"+fn[0:3]+"/"+fn, "r", encoding="utf8")
	xml = inp.read()
	xml = xml.replace('&i', "")
	parser = ET.XMLParser(encoding="utf-8")
	root = ET.fromstring(xml, parser=parser)
	
	# title
	tit = root.find("tit")
	e = tit.findall("e")[-1]
	engl = e.text
	outfn = engl
	for i in illegal:
		outfn = outfn.replace(i, '')
	if len(outfn) > 100:
		outfn = outfn[:100]
	outfn = cat+"/"+outfn+".html"
	
	if not os.path.isfile(outfn):
		print(outfn)
	
	sa = {}
	_ = get_sentences(sa, root.findall("sen"))
	for par in root.findall("par"):
		_ = get_sentences(sa, par.findall("sen"))
	for sec in root.findall("sec"):
		for par in sec.findall("par"):
			_ = get_sentences(sa, par.findall("sen"))

	ln1 = list(sa.values())[0]
	
	engl = engl.replace('"', '')
	return outfn, engl, jp, ln1

illegal = ['NUL','\',''//',':','*','"','<','>','|', '/', "'"]


file = open("../japanese_wiki_corpus_orig/Wiki_Corpus_List_2.01.csv", "r", encoding="utf8")

data = {}
for line in file:
	val = line.split(',')
	fn = val[0]
	jp = val[2]
	cat = val[3].split(' ')[0]

	outfn, engl, jp, ln1 = parse(fn, jp, cat)
	
	engl = orderName(engl)
	
	if cat not in data:
		data[cat] = []
		
	data[cat].append({
		'name': engl,
		'jp': jp,
		'url': outfn,
		'desc': ln1,
	})
	
	if testing:
		break

file.close()

with open('data.json', 'w', encoding="utf8") as outfile:
	json.dump(data, outfile, ensure_ascii=False)
