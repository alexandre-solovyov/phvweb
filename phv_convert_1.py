
f = open('phv_db_1.txt')
lines = f.readlines()

lines = list(map(lambda x: '' if len(x)==1 else x[0] + x[1:-1].lower(), lines))
lines = list(filter(lambda x: len(x)>0, lines))
#print(lines)

verbs = {}
output = []
examples = []

prev = ''
n = len(lines)//3
for i in range(0, n):
    verb = lines[3*i].lower()
    example = lines[3*i+2]
    if not verb==prev:
        examples.append('')
        prev = verb
        parts = verb.split(' ')
        v = parts[0]
        p = parts[1]
        if not v in verbs:
            verbs[v] = set()
        verbs[v].add(p)
    examples.append(example)

output.append("verbs:")
output.append("")
output.append("# infinitive  present   present_part   part_I   part_II    particle")

for v in verbs.keys():
    par = list(verbs[v])
    par.sort()
    output.append(v + " " + " ".join(par))

output.append("")
output.append("")
output.append("text:")
for e in examples:
    output.append(e)

f = open("result.lang", "w")
for o in output:
    f.write(o+"\n")
f.close()

