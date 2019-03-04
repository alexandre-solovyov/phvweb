
import random
import json

NONE = 0
VERBS = 1
TEXT = 2

VERBS_LINE = "verbs:"
TEXT_LINE = "text:"

COMMENT = "#"
FORMS = ["Inf", "Pr", "PrPart", "P1", "P2"]
NB_FORMS = len(FORMS)
POINTS = "..."

def check(line, start, length):
    if start>=0:
        s = line[start+length]
        if not str.isalpha(s):
            return True
    return False

def special_find(line, subs):
    start = line.find(subs)
    #print (line, subs, start)
    if check(line, start, len(subs)):
        return [(start, len(subs))]
    else:
        parts = subs.split(' ')
        res = []
        i = 0
        for p in parts:
            start = line.find(p, i)
            if check(line, start, len(p)):
                res.append((start, len(p)))
                i = start+len(p)
            else:
                return None
            
        return res
        
def special_replace(line, indices, placeh):
    #print(line, indices)
    for i in indices[::-1]:
        start, length = i
        line = line[:start] + placeh + line[start+length:]
    #print (line)
    return line

class Exercise:
    def __init__(self):
        self.question = ""
        self.answer = ""

class Model:
    def __init__(self, r=None):
        self.__mode = NONE
        self.__verbs = {}
        self.__exercises = []
        if r:
            random.seed(int(r))

    def mode(self):
        return self.__mode

    def nbExercises(self):
        return len(self.__exercises)

    def load(self, filename):
        ok = True
        f = None
        try:
            f = open(filename, 'r')
            if f==None:
                return False
            for line in f:
                self.parse(line)
        except FileNotFoundError:
            ok = False

        if f:
            f.close()
        return ok

    def parse(self, line):
        line = self.simplify(line)
        if len(line)==0:
            return

        if line.lower()==VERBS_LINE:
            self.__mode = VERBS
            return
        if line.lower()==TEXT_LINE:
            self.__mode = TEXT
            return
    
        if self.__mode==VERBS:
            parts = list(filter(lambda x: len(x)>0, line.split(' ')))
            verbs = parts[:NB_FORMS]
            particles = parts[NB_FORMS:]
            #print (verbs)
            #print (particles)
            for p in particles:
                compl_verbs = list(map(lambda x: x + " " + p, verbs))
                main_verb = compl_verbs[0]
                #print("Main verb: " + main_verb)
                self.__verbs[main_verb] = compl_verbs

        if self.__mode==TEXT:
            e = self.parsePhrase(line)
            if e==None:
                print("Warning! No exercise for line: " + line)
            else:
                self.__exercises.append(e)
                #print(e.question, len(self.__exercises))

    def parsePhrase(self, line):
        for pv, forms in self.__verbs.items():
            for f in forms:
                p = special_find(line, f)
                if not p is None:
                    e = Exercise()
                    e.question = special_replace(line, p, POINTS)
                    e.question = e.question.replace(POINTS+".", POINTS)
                    e.answer = f
                    return e
        return None

    def simplify(self, line):
        p = line.find(COMMENT)
        if p>=0:
            line = line[:p]
        line = line.strip()
        return line

    def verbs(self):
        lst = list(self.__verbs.keys())
        lst.sort()
        return lst

    def randomEx(self):
        i = random.randint(0, len(self.__exercises)-1)
        return self.__exercises[i]

    def randomExVars(self, nbVariants):
        e = self.randomEx()
        vars = self.findSimilar(e.answer, False)
        random.shuffle(vars)
        while len(vars) > nbVariants-1:
            i = random.randint(0, len(vars)-1)
            del vars[i]
        vars.append(e.answer)
        random.shuffle(vars)
        return e, vars

    def jsonify(self, e, vars):
        data = {}
        data["question"] = e.question
        data["answer"] = e.answer
        data["variants"] = vars
        return json.dumps(data)

    def findSimilar(self, verb, withItSelf=False):
        vv = None
        i = -1
        for pv, forms in self.__verbs.items():
            try:
                i = forms.index(verb)
            except:
                i = -1
            if i>=0:
                vv = pv
                break
        res = []
        if vv and i>=0:
            for pv, forms in self.__verbs.items():
                if withItSelf or pv!=vv:
                    res.append(forms[i])
        return res
