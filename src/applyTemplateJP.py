import sys
import os
import json
from string import ascii_uppercase

testing = False

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


applyPageTemplate()
