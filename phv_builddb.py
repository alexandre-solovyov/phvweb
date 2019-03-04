
import glob
import logging
from phv_dict import Parser, FORMS

class DB:
	def __init__(self):
		self.verbs = {}
		self.sentences = []

	def add(self, verb):
		parts = verb.split(" ")
		if len(parts)!=2:
			logging.error("Verb '%s' is incorrect" % verb)

		v = parts[0]
		p = parts[1]
		if not v in self.verbs:
			self.verbs[v] = []
		self.verbs[v].append(p)

	def addSent(self, sent_list):
		self.sentences = self.sentences + sent_list
		self.sentences.append("")
		
	def toFile(self):
		s = []
		s.append("verbs:")
		s.append("")
		s.append("# infinitive  present   present_part   part_I   part_II    particle")
		for v, p in self.verbs.items():
			forms = FORMS[v]
			s.append("%s %s   %s" % (v, " ".join(forms), " ".join(p)))
			
		s.append("")
		s.append("")
		s.append("text:")
		s.append("")
		s = s + self.sentences
		return "\n".join(s)
		
	def write(self, filename):
		f = open(filename, "w")
		f.write(self.toFile())
		f.close()

print("Building the database for PhV")

d = DB()
files = glob.glob("verbs/*")
for f in files:
	p = Parser(f)
	isOK = p.perform()
	print(f + "... " + ("OK" if isOK else "Failed"))
	d.add(p.verb)
	d.addSent(p.sentences)

#print (d.toFile())
d.write("phv2.lang")
print("The database is written")


