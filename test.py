import yaml

with open('test.yaml', 'r') as file:
    boop = yaml.safe_load(file)


out_file = '''
graph {nodesep=.2 ranksep=2 rankdir=LR

node [shape=none];
edge [color="#000000:#0066ff:#000000"];\n
'''

connectors = boop['connectors']
branches = boop['branches']
# loop through connectors
# print(connectors)


# THIS WORKS FOR RECORD TYPE. COLUMNS MISALIGNED THO.
# for c in connectors:
#     if set(['pins', 'pinlabels']).issubset(connectors[c]):
#         if len(connectors[c]['pins']) == len(connectors[c]['pinlabels']):
#             out = c
#             for i, p in enumerate(connectors[c]['pins']):
#                 out += f"|{{<{p}l>{connectors[c]['pinlabels'][i]}|<{p}r>{p}}}"

#             print(out)


def build_connector(c):
    out = f'"{c}" [label = <<TABLE border="0" cellspacing="0" cellborder="1"><TR><TD colspan="2">{c}</TD></TR>'
    for i, p in enumerate(connectors[c]['pins']):
        out += f'<TR><TD PORT="{p}L">{connectors[c]["pinlabels"][i]}</TD><TD PORT="{p}R">{p}</TD></TR>'
    out += "</TABLE>>];"
    global out_file 
    out_file += out + '\n'

def build_branch(b):
    out = f'"{b}" [label = <<TABLE border="0" cellspacing="0" color="grey" cellborder="1"><TR><TD>{b}</TD></TR>'
    for i in range(branches[b]['wirecount']):
        out += f'<TR><TD PORT="{i}"></TD></TR>'
    out += '</TABLE>>];'
    global out_file
    out_file += out + '\n'

# BUILD CONNECTORS
for c in connectors:
    if set(['pins', 'pinlabels']).issubset(connectors[c]):
        if len(connectors[c]['pins']) == len(connectors[c]['pinlabels']):
            build_connector(c)
    elif 'pinlabels' in connectors[c]:
        connectors[c]['pins'] = range(1,len(connectors[c]['pinlabels']) + 1)
        build_connector(c)

# BUILD BRANCHES
for b in branches:
    build_branch(b)

out_file += '}'

with open('out.gv', 'w') as file:
    file.write(out_file)