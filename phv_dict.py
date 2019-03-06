
import re
import copy
from phv_eng import Model, VERBS_LINE, TEXT_LINE

VERB_P = r'^\w+\s+\w+'

#            present   present_part   part_I   part_II
FORMS = {
	"break": ["breaks", "breaking", "broke", "broken"],
    "call":  ["calls", "calling", "called", "called"],
	"calm":  ["calms", "calming", "calmed", "calmed"],
    "carry": ["carries", "carrying", "carried", "carried"],
    "cheer": ["cheers", "cheering", "cheered", "cheered"],
	"come":  ["comes", "coming", "came", "come"],
    "find":  ["finds", "finding", "found", "found"],
    "give":  ["gives", "giving", "gave", "given"],
	"go":    ["goes", "going", "went", "gone"],
	"take":  ["takes", "taking", "took", "taken"],
    "try":   ["tries", "trying", "tried", "tried"],
	"write": ["writes", "writing", "wrote", "written"],
}


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
        isOK = True
        for line in lines:
            if not self.parseLine(line):
                isOK = False
                
        self.checkOnDouble()
        return isOK
        
    def parseLine(self, text):
        
        #print(text)
        m = re.match(VERB_P, text)
        if m is None:
            return False
        
        self.verb = m.group()
        text = re.sub(VERB_P, "", text)
        groups = re.split("\d+\)", text)
        isOK = True
        for g in groups:
            g = g.strip()
            if len(g)>0:
                if not self.parseGroup(g.strip()):
                    isOK = False
        return isOK
        
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
        return True

    def checkOnDouble(self):
        m = Model()
        m.parse(VERBS_LINE)
        
        vv = self.verb.split(' ')
        ff = FORMS[vv[0]]
        vv = [vv[0]] + ff + [vv[1]]
        vv = " ".join(vv)
        #print(vv)
        
        m.parse(vv)
        m.parse(TEXT_LINE)        
        for s in self.sentences:
            ee = m.parsePhrase(s, True)
            #print(s, ee)
            if len(ee)!=1:
                print ("Warning: %i exercises in\n  %s" % (len(ee), s))

    def __str__(self):
        s = ["PARSE: " + self.verb]
        s.append(str(len(self.sentences)))
        s = s + self.sentences
        return "\n  ".join(s)
    
if __name__ == '__main__':
    p = Parser('verbs/break_down')
    p.perform()
    assert len(p.sentences)==19

    p = Parser('verbs/calm_down')
    p.perform()
    assert len(p.sentences)==9

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

    p = Parser('verbs/call_up')
    p.perform()
    assert len(p.sentences)==8

    p = Parser('verbs/cheer_up')
    p.perform()
    assert len(p.sentences)==5

    p = Parser('verbs/go_out')
    p.perform()
    assert len(p.sentences)==23

    p = Parser('verbs/go_ahead')
    p.perform()
    assert len(p.sentences)==4

    p = Parser('verbs/try_on')
    p.perform()
    assert len(p.sentences)==4

    p = Parser('verbs/carry_on')
    p.perform()
    assert len(p.sentences)==14

    p = Parser('verbs/find_out')
    p.perform()
    #assert len(p.sentences)==14

    print(p)
