"""Build a rental scenario from the original workbook; retain suppression reasons."""
import ast, collections, csv, json
from pathlib import Path
import xlrd

root=Path(__file__).resolve().parents[1]
env=json.loads((root/"data/commune_crosswalk.json").read_text(encoding="utf-8"))

def canonical(n):
    n=env['RENAME'].get(n,n)
    return env['MERGE'].get(n,(n,))[0]
w=xlrd.open_workbook(str(root/'data/raw/loyers-apparts-2009-2025.xls'))
geo=json.loads((root/'data/clean/payload.json').read_text(encoding='utf-8'))
names=set(geo['shapes']); years=[]; panel={}; log=[]
for s in w.sheets():
    y=int(s.name); years.append(y); buckets=collections.defaultdict(list)
    for i in range(s.nrows):
        row=s.row_values(i)
        if 'Commune' in row: start=i+1; col=row.index('Commune'); break
    for i in range(start,s.nrows):
        r=s.row_values(i); name=str(r[col]).strip(); target=canonical(name)
        if target not in names:
            if name and not name.startswith(('Source','Moyenne','Total')): raise ValueError((y,name))
            continue
        n=r[col+1]; p=r[col+3]
        buckets[target].append((name,int(n) if isinstance(n,(int,float)) else 0,float(p) if isinstance(p,(int,float)) and p>0 else None))
    assert set(buckets)==names,(y,len(buckets))
    panel[str(y)]={}
    for name,parts in buckets.items():
        n=sum(p[1] for p in parts)
        good=all(p[2] is not None for p in parts)
        rate=sum(p[1]*p[2] for p in parts)/n if good and n else None
        reason='published' if good else ('component unavailable' if len(parts)>1 else 'source suppressed')
        panel[str(y)][name]={'rate':rate,'n':n,'reason':reason,'parts':[p[0] for p in parts]}
        log.append({'year':y,'commune':name,'rate':rate,'n':n,'reason':reason,'components':' | '.join(p[0] for p in parts)})
    print(y,'published',sum(v['rate'] is not None for v in panel[str(y)].values()),'within_fixed_NOMINAL_1200x45_diagnostic',sum(v['rate'] is not None and v['rate']*45<=1200 for v in panel[str(y)].values()))
with (root/'data/clean/rental_scenario.csv').open('w',encoding='utf-8',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(log[0]));wr.writeheader();wr.writerows(log)
out={'years':years,'shapes':geo['shapes'],'vb':geo['vb'],'cent':geo['cent'],'panel':panel}
monthly=collections.defaultdict(dict)
with (root/'data/raw/ipcn_review_5401.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        if r['FREQ']=='M' and r['MEASURE']=='IPCN' and r['ECOICOP_1999']=='CP00' and r['BASE_PERIOD']=='2015':
            monthly[r['TIME_PERIOD'][:4]][r['TIME_PERIOD']]=float(r['OBS_VALUE'])
out['cpi']={str(y):sum(monthly[str(y)].values())/12 for y in years if len(monthly[str(y)])==12}
assert len(out['cpi'])==len(years)
(root/'data/clean/rental_scenario.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(root/'quarto-assets/data.js').write_text('window.rentalData='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
with (root/'data/clean/ipcn_annual.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.writer(f); writer.writerow(['year','ipcn_annual_mean'])
    writer.writerows(out['cpi'].items())
print('Data regenerated; Quarto prose preserved.')
