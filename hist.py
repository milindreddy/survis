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
    'cascade'             : '#4e79a7',  # blue
    'contrastive'         : '#f28e2c',  # orange
    'correspondence'      : '#e15759',  # red
    'dynamic-dropping'    : '#76b7b2',  # teal
    'exposure-control'    : '#59a14f',  # green
    'hierarchical-rl'     : '#edc948',  # yellow
    'image-enhancement'   : '#b07aa1',  # purple
    'transformer'         : '#ff9da7',  # pink
    'view-selection'      : '#9c755f',  # brown
    'visual-rl'           : '#bab0ac',  # grey
}

# ---------- start new, wider figure ----------------------------------------
plt.figure(figsize=(12, 6))      # make it wider
bottom = [0]*len(year_list)

# ---------- build stacked bars ---------------------------------------------
for t in type_list:
    heights = [matrix[y][t] for y in year_list]
    plt.bar(year_list, heights, bottom=bottom,
            label=t.replace('-',' ').title(),
            color=type_colour.get(t, '#bbbbbb'))
    bottom = [b+h for b,h in zip(bottom, heights)]

plt.xlabel('Publication year')
plt.ylabel('Number of papers')
plt.xticks(year_list, rotation=45)  # ensure every year tick shows
plt.subplots_adjust(right=0.8)      # give space on the right for the legend
plt.legend(frameon=False,
           loc='center left',
           bbox_to_anchor=(1.0, 0.5))
plt.tight_layout()
plt.savefig('figs/hist_years.png', dpi=300, bbox_inches='tight')
print('hist_years.png saved')