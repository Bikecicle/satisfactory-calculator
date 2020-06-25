import json
import math

# load json files
with open('input.json', 'r') as in_file:
    input = json.load(in_file)

with open('dependencies.json', 'r') as dep_file:
    dependencies = json.load(dep_file)

# collect resource list {name: [used, extra]}
resource_rates = {}
resources = []
for dep in dependencies:
    for i in dep['input']:
        resource_rates[i['name']] = [0, 0]
        if i['name'] not in resources:
            resources.append(i['name'])
    for o in dep['output']:
        resource_rates[o['name']] = [0, 0]
        if o['name'] not in resources:
            resources.append(o['name'])


def find_recipe(item):
    for dep in dependencies:
        for o in dep['output']:
            if o['name'] == item:
                return dep, o['rate']
    return None, 0


def propagate_dependencies(item, rate, map):
    if item not in map:
        map[item] = 0
    map[item] += rate

    rec, rec_rate = find_recipe(item)

    if rec is not None:
        m = rate / rec_rate
        for i in rec['input']:
            propagate_dependencies(i['name'], i['rate'] * m, map)


matrix = []
for item in resources:
    row = []
    map = {}
    propagate_dependencies(item, 1.0, map)
    for i in range(len(resources)):
        if resources[i] in map:
            if item == 'Iron Ingot':
                print(resources[i], map[resources[i]])
            row.append(map[resources[i]])
        else:
            row.append(0.0)
    matrix.append(row)

l = len(resources)

with open('resource_indices.csv', 'w') as resources_file:
    for i in range(l):
        _, rate = find_recipe(resources[i])
        resources_file.write(str(i+1) + ',' + resources[i] + ',' + str(rate) + '\n')

with open('matrix.csv', 'w') as matrix_file:
    for i in range(l):
        for j in range(l):
            matrix_file.write(str(matrix[i][j]))
            if j < l - 1:
                matrix_file.write(',')
        matrix_file.write('\n')
