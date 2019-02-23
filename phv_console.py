
from phv_eng import *

variants = True
nb_variants = 4

m = Model()
m.load("phv.lang")

print("There are %i exercises" % m.nbExercises())

if variants:
    e, vars = m.randomExVars(nb_variants)
    print()
    print(e.question)
    i = 1
    for v in vars:
        print("  %i. %s" % (i, v))
        if e.answer==v:
            correct_index = i
        i += 1
    print()
    ans = int(input("   Your answer (index): "))
    print()
    if ans==correct_index:
        print("You are RIGHT!!!")
    else:
        print("Unfortunately, you are wrong, the correct answer is: %s (point %i)" % (e.answer, correct_index))
else:
    e = m.randomEx()
    print()
    print(e.question)
    print()
    ans = input("   Your answer: ")
    print()
    if e.answer==ans:
        print("You are RIGHT!!!")
    else:
        print("Unfortunately, you are wrong, the correct answer is: " + e.answer)
