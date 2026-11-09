/** Validate the real static output: routes, assets, project-base links, and imported content. */
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { load } from 'cheerio';
const root=resolve('dist');
const base=(process.env.BASE_PATH??'/swarmslabpage').replace(/\/$/,'');
const errors=[];
const imageReport=JSON.parse(readFileSync('migration/publication-images.json','utf8'));
const imageExceptions=new Set((imageReport.withoutImages??[]).map(p=>p.slug));
function walk(dir){return readdirSync(dir).flatMap(n=>{const p=join(dir,n);return statSync(p).isDirectory()?walk(p):[p];});}
if(!existsSync(root)){console.error('Build the website first: npm run build');process.exit(1);}
const files=walk(root), html=files.filter(f=>f.endsWith('.html'));
let checked=0, youtubeLinks=0;
for(const f of html){
 const $=load(readFileSync(f,'utf8'));
 const route=base+'/'+f.slice(root.length+1).replace(/index\.html$/,'');
 if(!$('title').text().includes('SwarmsLab'))errors.push(`${route}: missing lab title`);
 if(/Example Laboratory|Jane Doe|John Roe|Research area one/.test($('body').text()))errors.push(`${route}: placeholder content`);
 for(const el of $('a[href]').toArray()){
  const url=new URL(el.attribs.href,'https://site.test'+route);
  if(url.hostname==='youtu.be'||url.hostname.endsWith('.youtu.be')||url.hostname==='youtube.com'||url.hostname.endsWith('.youtube.com')){
   youtubeLinks++;
   const rel=(el.attribs.rel??'').split(/\s+/);
   if(el.attribs.target!=='_blank'||!rel.includes('noopener')||!rel.includes('noreferrer'))errors.push(`${route}: YouTube link must open safely in a new tab/window: ${url.href}`);
  }
 }
 for(const el of $('a[href], img[src], script[src], link[href], source[srcset], img[srcset]').toArray()){
  const attrs=el.attribs;
  const refs=[attrs.href,attrs.src,...(attrs.srcset?.split(',').map(s=>s.trim().split(/\s+/)[0])??[])].filter(Boolean);
  for(const ref of refs){
   if(/^(?:data:|mailto:|tel:|javascript:)/.test(ref)||ref.startsWith('#'))continue;
   const u=new URL(ref,'https://site.test'+route);
   if(u.origin!=='https://site.test'){
    if(el.tagName==='img'&&/swarmslab\.com/.test(u.hostname))errors.push(`${route}: WordPress-dependent image ${ref}`);
    continue;
   }
   if(base&&u.pathname!==base&&!u.pathname.startsWith(base+'/')){errors.push(`${route}: link escapes project path: ${ref}`);continue;}
   const path=decodeURIComponent(u.pathname.slice(base.length));
   const local=join(root,path);
   if(!existsSync(local)&&!existsSync(join(local,'index.html')))errors.push(`${route}: missing ${ref}`);
   checked++;
  }
 }
 for(const im of $('img').toArray())if(im.attribs.alt===undefined)errors.push(`${route}: image missing alt attribute`);
 for(const pub of $('[data-pub]').toArray()){
  const thumb=$(pub).find('img[data-pub-image]');
  const title=$(pub).find('h3').text();
  const imageOptional=imageExceptions.has($(pub).attr('data-pub-id'));
  if(thumb.length!==1&&!imageOptional)errors.push(`${route}: expected one publication thumbnail for ${title}`);
  if(thumb.length>1)errors.push(`${route}: duplicate publication thumbnail for ${title}`);
  if(thumb.length&&!thumb.attr('alt')?.trim())errors.push(`${route}: publication thumbnail missing alt text for ${title}`);
 }
}
const pubs=load(readFileSync(join(root,'publications/index.html'),'utf8'));
const sourceCount=readdirSync('src/content/publications').filter(f=>f.endsWith('.md')).length;
if(pubs('[data-pub]').length!==sourceCount)errors.push('Publication records lost during build');
for(const item of imageReport.images){
 if(pubs('[data-pub]').filter((_,el)=>pubs(el).attr('data-pub-id')===item.slug).find('img[data-pub-image]').length!==1)errors.push(`Missing documented publication thumbnail: ${item.slug}`);
}
const peopleCount=readdirSync('src/content/people').filter(f=>f.endsWith('.md')).length;
const robotData=JSON.parse(readFileSync('src/data/robots.json','utf8'));
const robots=load(readFileSync(join(root,'robots/index.html'),'utf8'));
const expectedRobots=[...robotData].sort((a,b)=>a.year-b.year);
const robotCards=robots('[data-robot]').toArray();
if(robotCards.length!==expectedRobots.length)errors.push('Robot entries lost during build');
for(const [i,robot] of expectedRobots.entries()){
 const card=robots(robotCards[i]);
 if(card.attr('id')!==robot.slug)errors.push(`Robot chronology or identity mismatch: ${robot.slug}`);
 if(card.find('img[data-robot-image]').length!==1)errors.push(`Robot image missing: ${robot.slug}`);
 if(card.find('[data-robot-video]').length!==1)errors.push(`Robot YouTube link missing: ${robot.slug}`);
 const paperIds=card.find('[data-robot-paper]').map((_,el)=>robots(el).attr('data-robot-paper')).get();
 if(JSON.stringify(paperIds)!==JSON.stringify(robot.papers))errors.push(`Robot papers missing or mismatched: ${robot.slug}`);
 const year=robot.endYear?`${robot.year}–${robot.endYear}`:String(robot.year);
 if(card.find('[data-robot-year]').text()!==year)errors.push(`Robot year mismatch: ${robot.slug}`);
}
if(!robots('nav[aria-label="Primary"] a').toArray().some(el=>robots(el).text().trim()==='Our Robots'&&robots(el).attr('href')===`${base}/robots/`))errors.push('Our Robots navigation link missing');
const builtPeople=html.filter(f=>/\/people\/[^/]+\/index\.html$/.test(f)).length;
if(peopleCount!==builtPeople)errors.push(`Expected ${peopleCount} profiles; built ${builtPeople}`);
const redirects=JSON.parse(readFileSync('src/data/redirects.json'));
for(const route of Object.keys(redirects))if(!existsSync(join(root,route,'index.html')))errors.push(`Missing old URL: ${route}`);
const sitemap=readFileSync(join(root,'sitemap-index.xml'),'utf8');
if(sitemap.includes('example.com'))errors.push('Placeholder sitemap origin');
const assetReport=JSON.parse(readFileSync('migration/assets.json'));
for(const path of Object.values(assetReport))if(!existsSync(join(root,path)))errors.push(`Missing migrated asset: ${path}`);
console.log(`${html.length} HTML pages; ${checked} internal links and asset references; ${sourceCount} publications; ${builtPeople} profiles.`);
console.log(`${pubs('img[data-pub-image]').length} publication thumbnails; ${imageExceptions.size} papers intentionally without images.`);
console.log(`${robotCards.length} robots with images, papers, and YouTube links in chronological order.`);
console.log(`${youtubeLinks} YouTube links open in a new tab/window.`);
if(errors.length){console.error([...new Set(errors)].join('\n'));process.exit(1);}
console.log(`✓ Static site checks passed (base: ${base||'/'}).`);
