import yaml

# TODO: Collect all connectors/branches/connections before render
# TODO: Assume if no receiving side exists that it is a branch. 

with open('test.yaml', 'r') as file:
    boop = yaml.safe_load(file)


out_file = '''
graph {nodesep=.2 ranksep=2 rankdir=LR

node [shape=none];
edge [color="#000000:#0066ff:#000000"];\n
'''

connectors = boop['connectors']
branches = boop['branches']
connections = boop['connections']

def build_connector(c):
    out = f'"{c}" [label = <<TABLE border="0" cellspacing="0" cellborder="1"><TR><TD colspan="2">{c}</TD></TR>'
    for i, p in enumerate(connectors[c]['pins']):
        out += f'<TR><TD PORT="{p}L">{connectors[c]["pinlabels"][i]}</TD><TD PORT="{p}R">{p}</TD></TR>'
    out += "</TABLE>>];"
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
    out = f'"{b}" [label = <<TABLE border="0" cellspacing="0" color="grey" cellborder="1"><TR><TD colspan="2">{b}</TD></TR>'
    for i in range(branches[b]['wirecount']):
        out += f'<TR><TD PORT="{i}L"></TD><TD PORT="{i}R"></TD></TR>'
    out += '</TABLE>>];'
    out_file += out + '\n'

# BUILD CONNECTIONS
for out_dict, in_dict in connections:
    out_key = list(out_dict.keys())[0]
    out_values = out_dict[out_key]
    in_key = list(in_dict.keys())[0]
    in_values = in_dict[in_key]
    
    for out_val, in_val in zip(out_values, in_values):
        out_file += f'"{out_key}":"{out_val}R" -- "{in_key}":"{in_val}L"\n'

out_file += '}'

with open('out.gv', 'w') as file:
    file.write(out_file)
