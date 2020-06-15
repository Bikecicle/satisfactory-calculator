import json
import math

# load json files
with open('input.json', 'r') as in_file:
    input = json.load(in_file)

with open('dependencies.json', 'r') as dep_file:
    dependencies = json.load(dep_file)

# collect resource list {name: [used, extra]}
resources = {}
for dep in dependencies:
    for i in dep['input']:
        resources[i['name']] = [0, 0]
    for o in dep['output']:
        resources[o['name']] = [0, 0]


def find_recipe(item):
    for dep in dependencies:
        for o in dep['output']:
            if o['name'] == item:
                return dep, o['rate']
    return None, 0


def propagate_dependencies(item, rate):
    print(item, rate)
    resources[item][0] += rate

    rec, rec_rate = find_recipe(item)

    if rec is not None:
        m = rate / rec_rate
        for i in rec['input']:
            propagate_dependencies(i['name'], i['rate'] * m)


for t in input['targets']:
    propagate_dependencies(t, input['targets'][t])

report = []
for r in resources:
    if resources[r][0] > 0:
        entry = {
            'item': r,
            'rate': resources[r][0],
        }
        rec, rec_rate = find_recipe(r)
        if rec is not None:
            m = resources[r][0] / rec_rate
            entry['machine'] = rec['machine']
            entry['machine_count'] = math.ceil(m)
            entry['overflow'] = (math.ceil(m) - m) * resources[r][0]
        report.append(entry)

with open('report.json', 'w') as report_file:
    report_file.write(json.dumps(report, indent=4))
