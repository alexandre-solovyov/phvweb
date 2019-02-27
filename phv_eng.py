
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
        except:
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
                p = line.find(f)
                if p>=0:
                    e = Exercise()
                    e.question = line.replace(f, POINTS)
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
        i = random.randint(0, len(self.__exercises))
        return self.__exercises[i]

    def randomExVars(self, nbVariants):
        e = self.randomEx()
        vars = self.findSimilar(e.answer, True)
        random.shuffle(vars)
        while len(vars) > nbVariants:
            i = random.randint(0, len(vars))
            del vars[i]
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
