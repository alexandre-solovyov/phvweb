
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
            st = v + " " + " ".join(forms)
            n = 50-len(st)
            st = st + " " * n
            st = st + " " + " ".join(p)
            s.append(st)
            
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

    def info(self):
        s = ["Info:"]
        s.append("  Verbs: %i" % len(self.verbs))
        cnt = 0
        for v, p in self.verbs.items():
            cnt += len(p)
        s.append("  Variants: %i" % cnt)
        s.append("  Sentences: %i" % len(self.sentences))
        return "\n".join(s)
    

print("Building the database for PhV")

d = DB()
files = glob.glob("verbs/*")
for f in files:
    p = Parser(f)
    isOK = p.perform()
    print(f + "... " + ("OK" if isOK else "Failed"))
    d.add(p.verb)
    d.addSent(p.sentences)

print()
print(d.info())

#print (d.toFile())
d.write("phv2.lang")
print()
print("The database is written")


