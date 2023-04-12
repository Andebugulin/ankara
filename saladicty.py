import pandas as pd

with open('saladict.txt', 'r', encoding='utf-8') as file:
    df = pd.DataFrame(columns=['Word', 'translations', 'node', 'contex'])
    data = list(map(lambda x: x.split('^'), file.read().split('\n\n')))
    data = list(filter(lambda x: len(x) == 4, data))

    words, translations, nodes, contexts = [], [], [], []
    for _1, _2, _3, _4 in data:
        try:
            words.append(_1 if _1 != '' else '')
            translations.append(_2 if _2 != '' else '')
            nodes.append(_4 if _4 != '' else '')
            contexts.append(_3 if _3 != '' else '')
        except:
            pass

    df['Word'] = words
    df['translations'] = translations
    df['ocntexts'] = contexts
    df['node'] = nodes

    df.to_excel('wordss.xlsx')