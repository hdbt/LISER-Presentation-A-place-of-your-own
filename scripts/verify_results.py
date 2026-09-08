import hashlib,json,math
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data/clean/rental_scenario.json').read_text(encoding='utf-8'))
expected=json.loads((root/'reference/expected_results.json').read_text())
for key in ['shapes','vb','cent','panel','cpi']:
    digest=hashlib.sha256(json.dumps(d[key],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    assert digest==expected[key], 'Snapshot mismatch: '+key
for year in d['years']: assert len(d['panel'][str(year)])==100
available=[r for r in d['panel']['2025'].values() if r['rate'] is not None]
assert len(available)==34
assert sum(r['rate']*45<=1200 for r in available)==14
common=[n for n in d['shapes'] if all(d['panel'][y][n]['rate'] is not None for y in ['2010','2025'])]
counts=[sum(d['panel'][y][n]['rate']*45<=1200*d['cpi'][y]/d['cpi']['2025'] for n in common) for y in ['2010','2025']]
assert len(common)==29 and counts==[29,11]
e=json.loads((root/'data/raw/leaving_home_eurostat.json').read_text())
assert e['value'][str(e['dimension']['time']['category']['index']['2025'])]==26.6
c=json.loads((root/'reference/hand_transcribed_claims.json').read_text())
for age,value in zip(['20-24','25-29','30-34'],[78.6,37.7,13.1]):
    assert math.isclose(sum(c['census_2021']['components_percent'][age]),value)
assert sum(c['schifflange_2022'][k] for k in ['municipal','fonds','other'])==246
print('PASS: regenerated map equals supplied snapshot; 2025 14/34, matched endpoints 29 -> 11, Eurostat and census checks')
