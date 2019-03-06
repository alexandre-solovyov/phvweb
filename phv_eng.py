
import random
import json
import copy

NONE = 0
VERBS = 1
TEXT = 2

VERBS_LINE = "verbs:"
TEXT_LINE = "text:"

COMMENT = "#"
FORMS = ["Inf", "Pr", "PrPart", "P1", "P2"]
NB_FORMS = len(FORMS)
POINTS = "..."

"""Check that find result is correct, i.e. start index
   is positive and the next symbol is not an alpha, i.e.
   we are searching for complete word"""
def check(line, start, length):
    if start>=0:
        s = line[start+length]
        if (start==0 or not str.isalpha(line[start-1])) and (not str.isalpha(s)):
            return True
    return False

"""Special find supporting separable words"""
def special_find(input_line, subs):
    line = input_line.lower()
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

"""Special replace supporting separable words"""
def special_replace(line, indices, placeh):
    #print(line, indices)
    for i in indices[::-1]:
        start, length = i
        line = line[:start] + placeh + line[start+length:]
    #print (line)
    return line

"""Exercise class"""
class Exercise:
    """Constructor"""
    def __init__(self):
        self.question = ""
        self.answer = ""
    
    """Equality operator"""
    def __eq__(self, other):
        if other is None:
            return False
        return self.question == other.question and self.answer == other.answer

"""Model class"""
class Model:
    """Constructor"""
    def __init__(self, r=None):
        self.__mode = NONE
        self.__mainverbs = {}
        self.__verbs = {}
        self.__exercises = []
        self.__defs = {}
        if r:
            random.seed(int(r))

    """Get current mode"""
    def mode(self):
        return self.__mode

    """Get number of exercises"""
    def nbExercises(self):
        return len(self.__exercises)
        
    """Get one of exercises"""
    def getExercise(self, index):
        return self.__exercises[index]

    """Load data from file"""
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

    """Parse one line"""
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

    """Parse one phrase"""
    def parsePhrase(self, line, isMultiple=False):
        res = [] if isMultiple else None
        for pv, forms in self.__verbs.items():
            for f in forms:
                p = special_find(line, f)
                if not p is None:
                    e = Exercise()
                    e.question = special_replace(line, p, POINTS)
                    e.question = e.question.replace(POINTS+".", POINTS)
                    e.answer = f
                    
                    if line.lower().startswith('if ') or line.lower().startswith('when '):
                        if pv in self.__defs:
                            self.__defs[pv].append(line)
                        else:
                            self.__defs[pv] = [line]
                    
                    if isMultiple:
                        if not e in res:
                            res.append(e)
                    else:
                        return e
        return res

    """Simplify the line removing comments"""
    def simplify(self, line):
        p = line.find(COMMENT)
        if p>=0:
            line = line[:p]
        line = line.strip()
        return line

    """Get all verbs available in the model"""
    def verbs(self):
        lst = list(self.__verbs.keys())
        lst.sort()
        return lst

    """Get random exercise"""
    def randomEx(self):
        i = random.randint(0, len(self.__exercises)-1)
        return self.__exercises[i]

    """Get random exercise with variants"""
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

    """Convert exercise with variants to JSON"""
    def jsonify(self, e, vars):
        data = {}
        data["question"] = e.question
        data["answer"] = e.answer
        data["variants"] = vars
        return json.dumps(data)

    """Find similar verbs"""
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

    """Get definition of a phrasal verb"""
    def getDefinition(self, verb):
        if verb in self.__defs:
            s = []
            i = 1
            for line in self.__defs[verb]:
                s.append("%i. %s" % (i, line))
                i = i + 1
            return "\n".join(s)
        else:
            return ""

    """Get list of verbs"""
    def getVerbs(self):
        if len(self.__mainverbs)==0:
            for v in self.__verbs:
                parts = v.split(" ")
                if parts[0] in self.__mainverbs:
                    self.__mainverbs[parts[0]].append(parts[1])
                else:
                    self.__mainverbs[parts[0]] = [parts[1]]
                    
        return list(self.__mainverbs.keys())
    
    """Get particles of the given verb"""
    def getParticles(self, verb):
        if len(self.__mainverbs)==0:
            self.getVerbs()
            
        if verb in self.__mainverbs:
            lst = copy.deepcopy(self.__mainverbs[verb])
            lst.sort()
            return lst
        else:
            return []

