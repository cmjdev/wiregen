import yaml

# TODO: Collect all connectors/branches/connections before render
# TODO: Assume if no receiving side exists that it is a branch.
# TODO: Change to encapsulating TD to get rid of tacking L/R node

with open('test.yaml', 'r') as file:
    boop = yaml.safe_load(file)


out_file = '''
graph {nodesep=.2 ranksep=4 rankdir=LR

node [shape=none fontname="Lucida Console" fontsize=8];
edge [color="#000000:#0066ff:#000000"];\n
'''

# node tuple?
# name, pins, pincount, pinlabels

connectors = {}
branches = {}
connections = []
# Gather all the connectors and verify pin info.
for k,v in boop['connectors'].items():
    if 'pins' in v:
        if 'pinlabels' in v:
            if not len(v['pins']) == len(v['pinlabels']):
                print(f'{k}: pins count does not match pinlabels count')
                continue
        else: 
            v['pinlabels'] = [' ' for _ in v['pins']]
    elif 'pinlabels' in v:
        v['pins'] = [x for x in range(1, len(v['pinlabels']) + 1)]
    else: 
        print(f'{k}: no pins or pinlabels specified)')
        continue
    v['out'] = []
    connectors[k] = v


# Create all connections
for i,k in enumerate(boop['connections']):
    link_from = list(k[0].items())[0]
    link_to = list(k[1].items())[0]
    for j, link in enumerate(link_from[1]):
        connections.append((link_from[0], link, link_to[0], link_to[1][j]))

# Create all branches
for c in connections:
    if c[0] not in connectors:
        if c[0] not in branches:
            branches[c[0]] = {"ports": [c[1]]}
        else: branches[c[0]]['ports'].append(c[1])
    if c[2] not in connectors:
        if c[2] not in branches:
            branches[c[2]] = {"ports": [c[3]]}
        else: branches[c[2]]['ports'].append(c[3])

# Render connectors
for k,v in connectors.items():
    # print(k,v)
    out = f'"{k}" [label = <<TABLE border="0" cellspacing="0" cellborder="1"><TR><TD colspan="2">{k}</TD></TR>'
    for i, p in enumerate(v['pins']):
        out += f'<TR><TD PORT="{p}L">{v["pinlabels"][i]}</TD><TD PORT="{p}R">{p}</TD></TR>'
    out += "</TABLE>>];"
    out_file += out + '\n'

# Render branches
for k,v in branches.items():
    out = f'"{k}" [label = <<TABLE border="1" cellspacing="0" color="grey" cellborder="0"><TR><TD colspan="2">{k}</TD></TR>'
    for i in v['ports']:
        out += f'<TR><TD PORT="{i}L"></TD><TD PORT="{i}R"></TD></TR>'
    out += '</TABLE>>];'
    out_file += out + '\n'
    
# Render edges
for c in connections:
    out_file += f'"{c[0]}":"{c[1]}R" -- "{c[2]}":"{c[3]}L"\n'




# connectors = boop['connectors']
# branches = boop['branches']
# connections = boop['connections']

# def build_connector(c):
#     out = f'"{c}" [label = <<TABLE border="0" cellspacing="0" cellborder="1"><TR><TD colspan="2">{c}</TD></TR>'
#     for i, p in enumerate(connectors[c]['pins']):
#         out += f'<TR><TD PORT="{p}L">{connectors[c]["pinlabels"][i]}</TD><TD PORT="{p}R">{p}</TD></TR>'
#     out += "</TABLE>>];"
#     global out_file 
#     out_file += out + '\n'

# # BUILD CONNECTORS
# for c in connectors:
#     if set(['pins', 'pinlabels']).issubset(connectors[c]):
#         if len(connectors[c]['pins']) == len(connectors[c]['pinlabels']):
#             build_connector(c)
#     elif 'pinlabels' in connectors[c]:
#         connectors[c]['pins'] = range(1,len(connectors[c]['pinlabels']) + 1)
#         build_connector(c)

# # BUILD BRANCHES
# for b in branches:
#     out = f'"{b}" [label = <<TABLE border="1" cellspacing="0" color="grey" cellborder="0"><TR><TD colspan="2">{b}</TD></TR>'
#     for i in range(branches[b]['wirecount']):
#         out += f'<TR><TD PORT="{i}L"></TD><TD PORT="{i}R"></TD></TR>'
#     out += '</TABLE>>];'
#     out_file += out + '\n'

# # BUILD CONNECTIONS
# for out_dict, in_dict in connections:
#     out_key = list(out_dict.keys())[0]
#     out_values = out_dict[out_key]
#     in_key = list(in_dict.keys())[0]
#     in_values = in_dict[in_key]
    
#     for out_val, in_val in zip(out_values, in_values):
#         out_file += f'"{out_key}":"{out_val}R" -- "{in_key}":"{in_val}L"\n'

out_file += '}'

with open('out.gv', 'w') as file:
    file.write(out_file)
