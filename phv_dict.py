
import re
import copy

VERB_P = r'^\w+\s+\w+'

def removeNotEng(s):
	if 'smb.' in s:
		return ''
	if 'smth.' in s:
		return ''
	
	m = re.search('[A-Z]', s)
	if m is None:
		return ''
	else:
		start, end = m.span()
		return s[start:]

class Parser:
	def __init__(self, theFileName):
		self.filename = theFileName
		self.verb = ""
		self.sentences = []
		
	def perform(self):
		f = open(self.filename, "r", encoding='utf-8')
		if f is None:
			return False
		
		lines = f.readlines()
		for line in lines:
			self.parseLine(line)
		
	def parseLine(self, text):
		
		#print(text)
		m = re.match(VERB_P, text)
		if m is None:
			return False
		
		self.verb = m.group()
		text = re.sub(VERB_P, "", text)
		groups = re.split("\d+\)", text)
		for g in groups:
			g = g.strip()
			if len(g)>0:
				self.parseGroup(g.strip())
		
	def parseGroup(self, group):
		group = re.sub("\[[\w\s\(\)/\-\,]*\]", "", group)
		group = re.sub("\([\w\s\(\)/\-\,]*\)", "", group)
		group = re.sub("PHR-[\w\-]+", "", group)
		group = re.sub("Syn:.*$", "", group)
		group = re.sub("Ant:.*$", "", group)
		group = re.sub("->.*$", "", group)
		
		#print(group)
		
		s = group.split(".")
		s = map(lambda x: removeNotEng(x.strip() + "."), s)
		s = filter(lambda x: len(x)>1, s)
		self.sentences = self.sentences + list(s)
		

	def __str__(self):
		s = ["PARSE: " + self.verb]
		s.append(str(len(self.sentences)))
		s = s + self.sentences
		return "\n  ".join(s)
	
	
p = Parser('verbs/break_down')
p.perform()
assert len(p.sentences)==19

p = Parser('verbs/calm_down')
p.perform()
assert len(p.sentences)==7

p = Parser('verbs/come_down')
p.perform()
assert len(p.sentences)==24

p = Parser('verbs/give_out')
p.perform()
assert len(p.sentences)==10

p = Parser('verbs/give_up')
p.perform()
assert len(p.sentences)==12

p = Parser('verbs/take_out')
p.perform()
assert len(p.sentences)==10

p = Parser('verbs/take_up')
p.perform()
assert len(p.sentences)==24

p = Parser('verbs/write_down')
p.perform()
assert len(p.sentences)==3

print(p)
