"""Apply the reviewed Scholar snapshot, preserving existing publication resources.

Uses only local reviewed metadata in migration/scholar. It never fetches or guesses
metadata and refuses to run if any Scholar entry is unaccounted for.
"""
from pathlib import Path
import json,re,unicodedata
ROOT=Path(__file__).resolve().parents[1]
PUBS=ROOT/'src/content/publications'
DATA=ROOT/'migration/scholar'
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def slug(s):return re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
def read(path):
 parts=path.read_text().split('---',2)
 fields={}
 for line in parts[1].strip().splitlines():
  k,v=line.split(': ',1);fields[k]=json.loads(v)
 return fields,parts[2]
def write(path,d,body):path.write_text('---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in d.items())+'\n---'+body)
def scholar_url(key):return 'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=VU1s_Z8AAAAJ&citation_for_view=VU1s_Z8AAAAJ:'+key
def tags(title):
 text=title.lower();result=[]
 terms={'modular-robots':['modular','modquad','multirotor','multi-rotor','reconfigurable','rotor fault'], 'aerial-manipulation':['transportation','airbender','hitch','catenary','manipulation','flysurf'], 'robotic-blimps':['blimp'], 'resilient-swarms':['resilien','malicious','crowd vetting','sensor network','multi-agent model'], 'environmental-monitoring':['perimeter tracking','sensor network'], 'robot-learning':['learning','imitation','turbulent flows']}
 for key,words in terms.items():
  if any(w in text for w in words):result.append(key)
 return result
def bibtex(key,d):
 kind={'journal':'article','conference':'inproceedings','chapter':'incollection','thesis':'mastersthesis','workshop':'misc','report':'techreport'}.get(d['publicationType'],'misc')
 fields={'title':d['title'],'author':' and '.join(d['authors']),'year':str(d['year'])}
 if d.get('journal'):fields['journal' if kind=='article' else 'school' if kind=='mastersthesis' else 'institution' if kind=='techreport' else 'booktitle' if kind in ['inproceedings','incollection'] else 'howpublished']=d['journal']
 for field in ['pages','volume','issue']:
  if d.get(field):fields['number' if field=='issue' else field]=d[field]
 if d.get('doi'):fields['doi']=d['doi']
 if d.get('url'):fields['url']=d['url']
 return '@'+kind+'{'+key+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items())+'\n}'
profile=json.loads((DATA/'profile.json').read_text())
assert profile['allRowsLoaded'], 'Profile pagination was not complete'
rows=profile['articles'];reviewed=json.loads((DATA/'reviewed-metadata.json').read_text())
existing={p:read(p) for p in PUBS.glob('*.md')}
# This snapshot is never overwritten by repeated imports.
if not (DATA/'existing-before.json').exists():
 (DATA/'existing-before.json').write_text(json.dumps({p.name:d for p,(d,_) in existing.items()},ensure_ascii=False,indent=2)+'\n')
by_title={norm(d['title']):p for p,(d,_) in existing.items()}
by_id={sid:p for p,(d,_) in existing.items() for sid in d.get('scholarIds',[])}
meta={sid:d for d in reviewed for sid in d['scholarIds']}
# Every unmatched title must have independently reviewed metadata.
missing=[r['id'] for r in rows if r['id'] not in by_id and norm(r['title']) not in by_title and r['id'] not in meta]
assert not missing, f'Unreviewed entries: {missing}'
plan={};coverage=[]
for r in rows:
 verified=meta.get(r['id'])
 path=by_id.get(r['id']) or by_title.get(norm(r['title']))
 if not path and verified:
  path=next((by_id[x] for x in verified['scholarIds'] if x in by_id),None)
  path=path or PUBS/(str(verified['year'])+'-'+slug(verified['title'])+'.md')
 assert path
 if path not in plan:
  is_new=path not in existing
  if is_new:
   assert verified
   d={k:v for k,v in verified.items() if k!='scholarIds'};body='\n\n';d.setdefault('resources',[]);d['areas']=tags(d['title'])
  else:
   old,body=existing[path];d=dict(old)
   if verified:
    # Only reviewed corrections are applied; preserve existing attachments and abstracts.
    for k in ['authors','year','journal','doi','publicationType','publicationNote','pages','volume','issue']:
     if k in verified:d[k]=verified[k]
    d['metadataSources']=list(dict.fromkeys(d.get('metadataSources',[])+verified.get('metadataSources',[])))
    d['resources']=d.get('resources',[])+[x for x in verified.get('resources',[]) if x not in d.get('resources',[])]
  plan[path]=dict(data=d,body=body,new=is_new,verified=verified)
 d=plan[path]['data'];d['scholarIds']=list(dict.fromkeys(d.get('scholarIds',[])+[r['id']]))
 d.setdefault('scholarUrl',scholar_url(r['id']))
 if not d.get('url') and not d.get('doi'):d['url']=d['scholarUrl']
 d['scholarChecked']='2026-11-08'
 by_id[r['id']]=path
 if verified:
  for x in verified['scholarIds']:by_id[x]=path
 coverage.append(dict(scholarId=r['id'],scholarTitle=r['title'],scholarYear=r['year'],file=path.name))
def patch_bib_field(text,key,value):
 m=re.search(r'(?:^|\n)\s*'+key+r'\s*=\s*\{',text)
 if not m:
  i=text.rfind('}');head=text[:i].rstrip().rstrip(',')
  return head+',\n  '+key+' = {'+value+'}\n'+text[i:]
 start=m.end();end=start;depth=1
 while end<len(text) and depth:
  if text[end]=='{':depth+=1
  elif text[end]=='}':depth-=1
  end+=1
 assert depth==0
 return text[:start]+value+text[end-1:]
for path,p in plan.items():
 d=p['data'];v=p['verified']
 if not d.get('bibtex'):
  d['bibtex']=bibtex(path.stem,d)
 elif v:
  fields={}
  for k in ['year','doi','pages','volume']:
   if k in v:fields[k]=str(d[k])
  if 'authors' in v:fields['author']=' and '.join(d['authors'])
  if 'journal' in v:fields[{'journal':'journal','conference':'booktitle','chapter':'booktitle','thesis':'school','report':'institution','workshop':'howpublished'}.get(d['publicationType'],'howpublished')]=d['journal']
  for k,val in fields.items():d['bibtex']=patch_bib_field(d['bibtex'],k,val)
  if 'publicationType' in v:
   kind={'journal':'article','conference':'inproceedings','chapter':'incollection','thesis':'mastersthesis','workshop':'misc','report':'techreport'}.get(d['publicationType'],'misc')
   d['bibtex']=re.sub(r'^@\w+', '@'+kind,d['bibtex'])
   if re.search(r'tppubtype\s*=',d['bibtex']):d['bibtex']=patch_bib_field(d['bibtex'],'tppubtype',kind)
 write(path,d,p['body'])
# Every Scholar row is mapped, including merged duplicates; original-only records survive.
baseline=json.loads((DATA/'existing-before.json').read_text())
report=dict(profile=profile['profile'],retrieved=profile['retrieved'],scholarRows=len(rows),representedWorks=len(plan),added=sum(path.name not in baseline for path in plan),totalPublications=len(list(PUBS.glob('*.md'))),coverage=coverage,retainedWebsiteOnly=[p.name for p in existing if p not in plan])
(DATA/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='coverage'},indent=2))
