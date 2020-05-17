import sys
import os

import xml.etree.ElementTree as ET

def get_sentences(sa, sens):
	first_id = None
	for sen in sens:
		txt = sen.findall("e")[-1].text
		if txt is not None:
			id = int(sen.attrib["id"])
			sa[id] = txt
			if not first_id:
				first_id = id
	return first_id

def write_sentence(out, id, txt, pars, prev_is_br):
	if id in pars:
		out.write("</p>\n<p>")
		prev_is_br = True
	if txt[-1] == '.' or txt[-2:] == '."':
		out.write(txt+" ")
		prev_is_br = False
	else:
		if not prev_is_br:
			out.write("\n<br/>")
		out.write(txt+"<br/>\n")
		prev_is_br = True
	return prev_is_br

def parse(fn, jp, cat):
	inp = open("../japanese_wiki_corpus_2/"+fn[0:3]+"/"+fn, "r", encoding="utf8")
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
	out = open(outfn, "w", encoding="utf8")
	out.write("<html>\n")
	
	out.write("<head>\n");
	analytics = "<!-- Global site tag (gtag.js) - Google Analytics --> \n" \
	+"<script async src='https://www.googletagmanager.com/gtag/js?id=UA-157500608-2'></script> \n" \
	+"<script> \n" \
	+" window.dataLayer = window.dataLayer || []; \n" \
	+" function gtag(){dataLayer.push(arguments);} \n" \
	+" gtag('js', new Date()); \n" \
	+" gtag('config', 'UA-157500608-2'); \n" \
	+"</script>\n"
	out.write(analytics)
	out.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
	out.write('<link rel="stylesheet" type="text/css" href="../style.css">\n')
	out.write('<link rel="shortcut icon" type="image/x-icon" href="../logo.ico" />\n')
	out.write("</head>\n")
	out.write("<body>\n")
	out.write("<a href='https://shinsengumi-archives.github.io/japanese-wiki-corpus/'>Home</a>\n")
	
	out.write("<h1>"+engl+" ("+jp+")</h1>\n")
	
	sa = {}
	pars = {}
	secs = {}
	_ = get_sentences(sa, root.findall("sen"))
	for par in root.findall("par"):
		id = get_sentences(sa, par.findall("sen"))
		if id:
			pars[id] = True
	for sec in root.findall("sec"):
		first = None
		for par in sec.findall("par"):
			id = get_sentences(sa, par.findall("sen"))
			if id:
				pars[id] = True
				if not first:
					first = id
		sub = sec.find("tit").findall("e")[-1].text
		if first:
			secs[first] = sub

	ln1 = list(sa.values())[0]
	first_sec = None
	if secs:
		first_sec = list(secs.keys())[0]
	prev_is_br = True
	
	# intro
	out.write("<p>")
	for id,txt in sa.items():
		if first_sec and id >= first_sec:
			break
		prev_is_br = write_sentence(out, id, txt, pars, prev_is_br)
	out.write("</p>\n")
	
	# sections
	if first_sec:
		out.write("<p>")
		for id,txt in sa.items():
			if id < first_sec:
				continue
			if id in secs:
				out.write("<h3>"+secs[id]+"</h3>\n")
				prev_is_br = True
			prev_is_br = write_sentence(out, id, txt, pars, prev_is_br)
		out.write("</p>\n")
	
	out.write("</body>\n")
	out.write("</html>\n")
	out.close()
	
	# index
	cat_file = open(cat+".html", "a", encoding="utf8")
	cat_file.write("<p><a href='"+outfn+"'>"+engl+"</a> ("+jp+") - "+ln1+"</p>\n")
	cat_file.close()
	
	sitemap = open("sitemap.xml", "a", encoding="utf8")
	sitemap.write("<url><loc>https://shinsengumi-archives.github.io/japanese-wiki-corpus/"+outfn+"</loc><lastmod>2020-02-05T03:17:57+00:00</lastmod><priority>0.64</priority></url>\n")
	sitemap.close()

illegal = ['NUL','\',''//',':','*','"','<','>','|', '/', "'"]

file = open("../japanese_wiki_corpus_2/Wiki_Corpus_List_2.01.csv", "r", encoding="utf8")

sitemap = open("sitemap.xml", "w", encoding="utf8")
sitemap.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
sitemap.close()

cats = ['Buddhism', 'building', 'culture', 'emperor', 'family', 'geographical', 'history', 'literature', 'person', 'railway', 'road', 'shrines', 'school', 'Shinto', 'title']
for cat in cats:
	out = open(cat+".html", "w", encoding="utf8")
	out.write("<html>\n")
	out.write("<head>\n")
	out.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
	out.write('<link rel="stylesheet" type="text/css" href="style.css">\n')
	out.write('<link rel="shortcut icon" type="image/x-icon" href="logo.ico" />\n')
	out.write('<title>'+cat+'</title>\n')
	out.write("</head>\n")
	out.write("<body>\n")
	out.write("<a href='https://shinsengumi-archives.github.io/japanese-wiki-corpus/'>Home</a>\n")
	out.write("<h1>"+cat+"</h1>\n")
	out.close()
	if not os.path.exists(cat):
		os.mkdir(cat)

for line in file:
	val = line.split(',')
	fn = val[0]
	jp = val[2]
	cat = val[3].split(' ')[0]

	parse(fn, jp, cat)


for cat in cats:
	out = open(cat+".html", "a", encoding="utf8")
	out.write("</body>\n")
	out.write("</html>\n")
	out.close()

sitemap = open("sitemap.xml", "a", encoding="utf8")
sitemap.write("</urlset>\n")
sitemap.close()

file.close()
