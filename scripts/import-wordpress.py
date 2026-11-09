"""One-time, reproducible import of the public WordPress snapshot (requires beautifulsoup4).
Run before editorial changes only: this regenerates imported content files.
Download assets separately with scripts/download-assets.py.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json, re, unicodedata
from urllib.parse import urlsplit, unquote
ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT / 'migration/source/pages.json').read_text())
def soup(slug):
    return BeautifulSoup(next(p for p in PAGES if p['slug'] == slug)['content']['rendered'], 'html.parser')
def txt(el): return ' '.join(el.get_text(' ', strip=True).split()) if el else ''
def slugify(s): return re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()).strip('-')
def writejson(path, data):
    (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def md(path, data, body=''):
    (ROOT / path).write_text('---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in data.items())+'\n---\n\n'+body+'\n')
assets={}
def asset(url):
    url=url.strip().replace('http://','https://')
    u=urlsplit(url)
    if u.hostname in ['swarmslab.com','www.swarmslab.com']:
        path=unquote(u.path)
    else: path='/media/'+slugify(u.hostname or 'external')+'/'+unquote(u.path.split('/')[-1])
    assets[url]=path
    return path

def imgurl(img): return img.get('data-image_src') or img.get('data-full_image_src') or img.get('src','')
# Remove only the template's sample content.
for name in ['people','publications','gallery','figures']:
    for f in (ROOT / 'src/content' / name).glob('*.md'): f.unlink()

people=[]
for i,card in enumerate(soup('team').select('.bt_bb_card_image')):
    name=re.sub(r'^Prof\.\s*','',txt(card.select_one('h3')))
    if not name: continue
    slug=slugify(name)
    role=txt(card.select_one('.bt_bb_headline_subheadline'))
    bio=txt(card.select_one('.bt_bb_card_image_text'))
    role=role or bio
    d=dict(name=name,status='current' if i<5 else 'alumni',group='Faculty' if i==0 else ('Students' if i<5 else 'Alumni'),role=role,order=i)
    im=card.select_one('img')
    if im:
        url=imgurl(im)
        # The source uses a stock robot illustration for Sebastian, not a portrait.
        if '/uploads/' in url and 'Robot-ai' not in url: d['headshot']='../../../public'+asset(url)
    a=card.select_one('h3 a[href]'); links={}
    if a and a['href'].startswith('http') and 'swarmslab.com' not in a['href']: links['website']=a['href']
    if i==0: links.update(email='saldana@lehigh.edu',twitter='https://twitter.com/dsaldana1',linkedin='https://www.linkedin.com/in/david-salda%C3%B1a-65200419')
    d['links']=links
    if bio.startswith('Now '): d['title']=bio[4:]
    md('src/content/people/'+slug+'.md',d,bio)
    people.append(dict(slug=slug,**d))

# Parse teachPress's complete BibTeX export, including multiline URL fields.
pubs=[]; bibs=[]
for pre in soup('publications').select('pre'):
    bib=pre.get_text('\n').replace('\r','')
    fields={}
    for m in re.finditer(r'(?:^|\n)\s*(\w+)\s*=\s*\{',bib):
        start=m.end(); depth=1; end=start
        while end<len(bib) and depth:
            if bib[end]=='{': depth+=1
            elif bib[end]=='}': depth-=1
            end+=1
        fields[m.group(1)]=bib[start:end-1].strip()
    if not fields.get('title'): continue
    title=fields['title']; slug=str(fields['year'])+'-'+slugify(title)
    urls=re.findall(r'https?://[^\s<>]+',fields.get('url',''))
    urls=[u.rstrip(',') for u in urls]
    urls=[asset(u) if 'swarmslab.com/wp-content/uploads/' in u else u for u in urls]
    doi=fields.get('doi','').strip()
    doi=re.sub(r'^https?://(?:dx\.)?doi.org/','',doi).strip()
    if doi.startswith('arXiv:'):
        urls.insert(0,'https://arxiv.org/abs/'+doi.split(':')[1]); doi=''
    kind={'article':'journal','inproceedings':'conference','incollection':'chapter','inbook':'chapter'}.get(fields.get('tppubtype'),'other')
    text=(title+' '+fields.get('keywords','')).lower()
    areas=[]
    for area,words in {'modular-robots':['modular','modquad','reconfiguration','self-assembl','multirotor','multi-rotor'], 'aerial-manipulation':['catenary','manipulation','hitch','knot','contact force','gripper'], 'resilient-swarms':['resilien','consensus','surveillance','perimeter','task allocation'], 'environmental-monitoring':['environment','boundary','sensor network'], 'robotic-blimps':['blimp']}.items():
        if any(w in text for w in words): areas.append(area)
    d=dict(title=title,authors=[a.strip() for a in fields.get('author','').split(' and ')],year=int(fields['year']),journal=fields.get('journal') or fields.get('booktitle') or '',publicationType=kind,areas=areas)
    if doi: d['doi']=doi
    ext=[u for u in urls if u.startswith('http')]
    if ext: d['url']=next((u for u in ext if 'youtu' not in u),ext[0])
    d['resources']=[{'label':'Video' if 'youtu' in u else ('PDF' if '.pdf' in u else 'Full text'),'url':u} for u in urls]
    d['abstract']=' '.join(fields.get('abstract','').split())
    d['bibtex']=bib.strip()
    md('src/content/publications/'+slug+'.md',d)
    pubs.append(dict(slug=slug,**d)); bibs.append(bib)

# News: source headings and following descriptive text before the Media section.
s=soup('home-02'); news=[]
for h in s.select('h5,h6'):
    title=txt(h)
    if not title.startswith('–'): continue
    if h.find_previous('h3') and txt(h.find_previous('h3'))=='Media': continue
    a=h.select_one('a[href]')
    if not a: continue
    body=[]
    for el in h.next_siblings:
        if getattr(el,'name',None) in ['h3','h4','h5']: break
        if getattr(el,'name',None)=='h6' and txt(el).startswith('–'): break
        if getattr(el,'name',None) and txt(el): body.append(txt(el))
    news.append(dict(title=title.lstrip('– ').strip(),url=a['href'],body=' '.join(body)))
# News headlines live in separate builder blocks; preserve descriptions explicitly from the source.
news_descriptions=[
 'PI David Saldaña receives the NSF CAREER Award to advance aerial robotics capable of manipulating flexible objects and adapting to shifting forces in midair.',
 'Team Lehigh Swarms wins at Indiana University, where the team first joined the competition two and a half years earlier.',
 'A hands-on introduction to robotics engineering for middle-school girls through the Lehigh CHOICES program.',
 'Lehigh Swarms won MVP at DTR Event 8 among ten universities. Mochi 3.0 demonstrated autonomous collaborative capturing and scoring.',
 'SwarmsLab hosted seven other universities at Lehigh’s Mountaintop campus for the fall blimp competition.',
 'Lehigh’s team qualified ahead of the other teams and placed third in its second appearance at the blimp competition.',
 'A day of talks, posters, and demos at Lehigh AIRLab, featuring five invited research presentations.',
 'Resolve Magazine visits the Autonomous and Intelligent Robotics Laboratory on Lehigh’s Mountaintop campus.'
]
news_images=[imgurl(x) for x in s.select('img')][:9]
for i,n in enumerate(news):
    if i<len(news_descriptions): n['body']=news_descriptions[i]
    if i<len(news_images): n['image']=asset(news_images[i])
# Videos from embeds, builder data, and publication resource links, deduplicated by YouTube ID.
videos=[]; seen=set()
def video(url,title):
    m=re.search(r'(?:youtu\.be/|youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=))([\w-]{11})',url)
    if not m or m[1] in seen:return
    seen.add(m[1]); videos.append(dict(id=m[1],title=title.lstrip('– ').strip()))
for f in s.select('iframe'):
    h=f.find_previous(['h4','h5','h6']); video(f.get('src',''),txt(h))
for pub in pubs:
    for r in pub['resources']: video(r['url'],pub['title'])
vs=soup('videos')
for block in vs.select('.bt_bb_video'):
    raw=str(block)
    for u in re.findall(r'https?[^\s\"<>]+',raw):
        h=block.find_previous(['h4','h5']); video(u,txt(h) or 'SwarmsLab research demonstration')
# Gallery: original event captions retained; no fabricated dates.
gallery=[]
for i,item in enumerate(soup('mediavw2022').select('.gallery-item')):
    im=item.select_one('img'); cap=txt(item.select_one('.gallery-caption'))
    if not im: continue
    path=asset(imgurl(im)); cap=cap or 'Robot Versatility Workshop 2022'
    md('src/content/gallery/workshop-2022-'+str(i+1).zfill(2)+'.md',dict(image='../../../public'+path,caption=cap,date='2022-05-27',featured=i<3))
    gallery.append(path)
project_text=[txt(x) for x in soup('projects').select('.bt_bb_text')]
projects=[]
for i,(sl,title,subtitle,image) in enumerate([
 ('modular-robots','Modular aerial robots','ModQuad & H-ModQuad','https://swarmslab.com/wp-content/uploads/2022/05/mainHModQuad.png'),
 ('aerial-manipulation','Collaborative manipulation','The Catenary Robot','https://swarmslab.com/wp-content/uploads/2022/01/real_robot.jpg'),
 ('resilient-swarms','Resilient robot swarms','Coordination at scale','https://swarmslab.com/wp-content/uploads/2021/11/dense.png')]):
    projects.append(dict(slug=sl,title=title,subtitle=subtitle,body=project_text[i],image=asset(image)))
# Download all meaningful imagery in the active pages, and locally linked attachments.
active=['home-02','team','projects','publications','club','location','videos','mediavw2022','david-saldana','diego-salazardantonio','gustavo-cardona','teaching']
for sl in active:
    for im in soup(sl).select('img'):
        u=imgurl(im)
        if '/uploads/' in u and not any(x in u for x in ['bottom_cover','top_wave','Robot-ai']):asset(u)
# Original homepage background is a real lab photograph.
asset('https://swarmslab.com/wp-content/uploads/2021/11/B1.png')
writejson('src/data/news.json',news)
writejson('src/data/videos.json',videos)
writejson('src/data/projects.json',projects)
writejson('migration/assets.json',assets)
writejson('migration/inventory.json',dict(source='https://swarmslab.com',retrieved='2026-11-08',pages=active,people=len(people),publications=len(pubs),news=len(news),videos=len(videos),gallery=len(gallery),assets=len(assets),excludedDemoPages=[p['slug'] for p in PAGES if p['slug'] not in active]))
(ROOT/'migration/source/publications.bib').write_text('\n\n'.join(bibs))
print(json.dumps(dict(people=len(people),publications=len(pubs),news=len(news),videos=len(videos),gallery=len(gallery),assets=len(assets))))
print('Publication types:', {k:sum(p['publicationType']==k for p in pubs) for k in ['journal','conference','chapter','other']})
