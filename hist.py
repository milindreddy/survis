import bibtexparser, collections, matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path
 
# ---------- load BibTeX ----------------------------------------------------
with open('bib/references.bib', encoding='utf-8') as f:
    entries = bibtexparser.load(f).entries
 
# ---------- collect counts  (year, type) -----------------------------------
types   = set()
matrix  = defaultdict(lambda: defaultdict(int))   # year → type → count
 
for e in entries:
    year = int(e['year'])
    type_tag = next(t.split(':',1)[1] for t in e['keywords'].split(',')
                    if t.startswith('type:')).strip()
    types.add(type_tag)
    matrix[year][type_tag] += 1
 
year_list  = sorted(matrix)
type_list  = sorted(types)                        # fixed order in legend
 
# ---------- colour palette per type ----------------------------------------
type_colour = {
    'temporal'            : '#4e79a7',
    'machine-learning'    : '#f28e2c',
    'text-visualization'  : '#e15759',
    'population-health'   : '#59a14f',
    'cohort-comparison'   : '#b07aa1',
    'patient-similarity'  : '#edc948',
    'survey'              : '#9c755f'
}
 
# ---------- build stacked bars ---------------------------------------------
bottom = [0]*len(year_list)
for t in type_list:
    heights = [matrix[y][t] for y in year_list]
    plt.bar(year_list, heights, bottom=bottom,
            label=t.replace('-',' ').title(),
            color=type_colour.get(t, '#bbbbbb'))
    bottom = [b+h for b,h in zip(bottom, heights)]
 
plt.xlabel('Publication year'); plt.ylabel('Number of papers')
plt.legend(frameon=False)
plt.tight_layout()
 
Path('figs').mkdir(exist_ok=True)
plt.savefig('figs/hist_years.png', dpi=300)
print('hist_years.png saved')