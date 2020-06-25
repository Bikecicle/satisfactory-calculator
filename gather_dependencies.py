from lxml import html
import requests
import json

dependencies = []


def scrape_recipes(machine):
    page = requests.get('https://satisfactory.gamepedia.com/' + machine.capitalize())
    tree = html.fromstring(page.content)
    recipes = tree.xpath('//*[@id="mw-content-text"]/div/table[@class="wikitable"]/tbody/tr')
    for r in recipes[1:]:
        if r[0].text:
            dep = {
                'machine': machine,
                'name': r[0].text,
                'time': float(r[1].text),
                'input': [],
                'output': []
            }
            for i in range(int(len(r[2])/4)):
                dep['input'].append({
                    'count': float(r[2][i*4].text[:-1]),
                    'name': r[2][i*4+1][1].text,
                    'rate': float(r[2][i*4+2].text[:-4])
                })
            for i in range(int(len(r[3])/4)):
                dep['output'].append({
                    'count': float(r[3][i*4].text[:-1]),
                    'name': r[3][i*4+1][1].text,
                    'rate': float(r[3][i*4+2].text[:-4])
                })
            dependencies.append(dep)


scrape_recipes('constructor')
scrape_recipes('assembler')
scrape_recipes('manufacturer')
scrape_recipes('smelter')
scrape_recipes('foundry')

with open('dependencies.json', 'w') as dep_file:
    dep_file.write(json.dumps(dependencies, indent=2))
