import requests
from bs4 import BeautifulSoup

verbs_url = 'https://jlptsensei.com/jlpt-n5-verbs-vocabulary-list/'

response = requests.get(verbs_url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

verbs_table = soup.find('table', {'id': 'jl-vocab'})
rows = verbs_table.find_all('tr')[1:]

verbs_dict = {}
for row in rows:
    try:
        cells = row.find_all('td')
        verbs_dict[cells[1].text.strip()] = cells[-1].text.strip('\u200b')
    except IndexError:
        continue

###############################################################################################
nouns_url = 'https://jlptsensei.com/jlpt-n5-nouns-vocabulary-list/'

response = requests.get(nouns_url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

nouns_table = soup.find('table', {'id': 'jl-vocab'})
rows = nouns_table.find_all('tr')[1:]

nouns_dict = {}
for row in rows:
    try:
        cells = row.find_all('td')
        nouns_dict[cells[1].text.strip()] = cells[-1].text.strip('\u200b')
    except IndexError:
        continue

###############################################################################################
adverbs_url = 'https://jlptsensei.com/jlpt-n5-adverbs-list/'

response = requests.get(adverbs_url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

adverbs_table = soup.find('table', {'id': 'jl-grammar-all'})
rows = adverbs_table.find_all('tr')[1:]

adverbs_dict = {}
for row in rows:
    try:
        cells = row.find_all('td')
        adverbs_dict[cells[2].text.strip()] = cells[-1].text.strip('\u200b')
    except IndexError:
        continue

###############################################################################################
adjectives_url = 'https://jlptsensei.com/jlpt-n5-adjectives-vocabulary-list/'

response = requests.get(adjectives_url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

adjectives_table = soup.find('table', {'id': 'jl-vocab'})
rows = adjectives_table.find_all('tr')[1:]

adjectives_dict = {}
for row in rows:
    try:
        cells = row.find_all('td')
        adjectives_dict[cells[1].text.strip()] = cells[-1].text.strip('\u200b')
    except IndexError:
        continue

###############################################################################################
pna_url = 'https://jlptsensei.com/jlpt-n5-pre-noun-adjectival-list/'

response = requests.get(pna_url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

pna_table = soup.find('table', {'id': 'jl-grammar-all'})
rows = pna_table.find_all('tr')[1:]

pna_dict = {}
for row in rows:
    try:
        cells = row.find_all('td')
        pna_dict[cells[2].text.strip()] = cells[-2].text.strip('\u200b')
    except IndexError:
        continue

###############################################################################################
particles_url = 'https://jlptsensei.com/jlpt-n5-particles-list/'

response = requests.get(particles_url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

particles_table = soup.find('table', {'id': 'jl-grammar-all'})
rows = particles_table.find_all('tr')[1:]

particles_dict = {}
for row in rows:
    try:
        cells = row.find_all('td')
        particles_dict[cells[2].text.strip()] = cells[-2].text.strip('\u200b')
    except IndexError:
        continue

###############################################################################################
katakana_url = 'https://jlptsensei.com/jlpt-n5-katakana-words-list/'

response = requests.get(katakana_url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

katakana_table = soup.find('table', {'id': 'jl-grammar-all'})
rows = katakana_table.find_all('tr')[1:]

katakana_dict = {}
for row in rows:
    try:
        cells = row.find_all('td')
        katakana_dict[cells[2].text.strip()] = cells[-2].text.strip('\u200b')
    except IndexError:
        continue


# print("nouns dictionary:\n", nouns_dict)
# print()
# print("verbs dictionary:\n", verbs_dict)
# print()
# print("adverbs dictionary:\n", adverbs_dict)
# print()
# print("adjectives dictionary:\n", adjectives_dict)
# print()
# print("pre-noun adjectivals dictionary:\n", pna_dict)
# print()
# print("particles dictionary:\n", particles_dict)
# print()
# print("katakana dictionary:\n", katakana_dict)
# print()