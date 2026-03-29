import json

with open('03_Snipers_Team_ML_Notebook_Final.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

extracted = []
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell.get('source', []))
        extracted.append("\n" + "="*40 + "\n--- MARKDOWN ---\n" + "="*40)
        extracted.append(source)
    elif cell['cell_type'] == 'code':
        outputs = cell.get('outputs', [])
        for out in outputs:
            if 'text' in out:
                text = ''.join(out['text'])
                extracted.append("\n" + "-"*20 + "\n--- OUTPUT ---\n" + "-"*20)
                extracted.append(text)
            elif 'data' in out and 'text/plain' in out['data']:
                text = ''.join(out['data']['text/plain'])
                extracted.append("\n" + "-"*20 + "\n--- DATA OUTPUT ---\n" + "-"*20)
                extracted.append(text)

with open('notebook_extracted.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(extracted))
