import yaml

# TODO: Collect all connectors/branches/connections before render
# TODO: Assume if no receiving side exists that it is a branch.
# TODO: Change to encapsulating TD to get rid of tacking L/R node

with open('test.yaml', 'r') as file:
    boop = yaml.safe_load(file)


out_file = '''
graph {nodesep=.1 ranksep=2 rankdir=LR

node [shape=none fontname="Lucida Console" fontsize=8];
edge [color="#000000:#0066ff:#000000"];\n
'''

connectors = {}
branches = {}
connections = []

# Create connectors and verify pin info.
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

# TODO: Branch info partially broken.. ins OR outs work, not both
for c in connections:
    print(c)
    if c[0] not in connectors:
        if c[0] not in branches:
            branches[c[0]] = {"ports": [c[1]], "in": {}, "out": {c[1]: f"{c[2]}:{c[3]}"}}
        elif c[1] not in branches[c[0]]['ports']:
            branches[c[0]]['ports'].append(c[1])
            branches[c[0]]["out"][c[1]] = f"{c[2]}:{c[3]}"
        else: branches[c[0]]["out"][c[1]] = f"{c[2]}:{c[3]}"
    if c[2] not in connectors:
        if c[2] not in branches:
            branches[c[2]] = {"ports": [c[3]], "in": {c[3]: f"{c[0]}:{c[1]}"}, "out": {}}
        elif c[3] not in branches[c[2]]['ports']:
            branches[c[2]]['ports'].append(c[3])
            branches[c[2]]["in"][c[3]] = f"{c[0]}:{c[1]}"
        else: branches[c[2]]["in"][c[3]] = f"{c[0]}:{c[1]}"

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
    print(v['out'])
    for i in v['ports']:
        in_link = v["in"][i] if i in v["in"] else ""
        out_link = v["out"][i] if i in v["out"] else ""
        out += f'<TR><TD PORT="{i}L">{in_link}</TD><TD PORT="{i}R">{out_link}</TD></TR>'
        # try: out += f'{v["in"][i]}</TD><TD PORT="{i}R">{v["out"]}</TD></TR>'
        # except: out += f'</TD><TD PORT="{i}R">{v["out"]}</TD></TR>'
    out += '</TABLE>>];'
    out_file += out + '\n'
    
# Render edges
for c in connections:
    out_file += f'"{c[0]}":"{c[1]}R" -- "{c[2]}":"{c[3]}L"\n'

out_file += '}'

with open('out.gv', 'w') as file:
    file.write(out_file)

print(branches)