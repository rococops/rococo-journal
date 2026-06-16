import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from build_pages import load_all_rows_by_category, load_mcolumn_rows
from collections import defaultdict
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), '..')

with open(os.path.join(BASE, 'sitecontents.sql'), encoding='utf-8') as f:
    sql = f.read()
with open(os.path.join(BASE, 'mcolumn.sql'), encoding='utf-8') as f:
    mcolumn_sql = f.read()

by_cat = load_all_rows_by_category(sql)
mcolumn_rows = load_mcolumn_rows(mcolumn_sql)
mcolumn_by_loc = defaultdict(list)
for r in mcolumn_rows:
    mcolumn_by_loc[r['cat_path'], r['sub_dir']].append(r)

targets = [
    (['0101000000'], 'cheekbone', 'quick'),
    (['0203000000'], 'nose', 'rib-cartilage'),
    (['0301000000'], 'nostril', 'alar-lowering'),
    (['0201000000'], 'nose', 'column'),
]

for codes, cat, sub in targets:
    rows = []
    for c in codes:
        rows.extend(by_cat.get(c, []))
    rows += mcolumn_by_loc.get((cat, sub), [])
    rows = sorted(rows, key=lambda r: r['date'], reverse=True)
    if rows:
        r = rows[0]
        d = r['date'].strftime('%Y-%m-%d') if r['date'] != datetime.min else '?'
        print(cat + '/' + sub + '/' + r['slug'] + '/  [' + d + ']  ' + r['subject'][:50])
