/** Verify coverage of every fetched Scholar row and preserve the original migration. */
import { readFileSync, readdirSync } from 'node:fs';
import assert from 'node:assert/strict';
const root='migration/scholar/';
const profile=JSON.parse(readFileSync(root+'profile.json'));
const baseline=JSON.parse(readFileSync(root+'existing-before.json'));
const coverage=JSON.parse(readFileSync(root+'coverage.json'));
const parse=file=>Object.fromEntries(readFileSync('src/content/publications/'+file,'utf8').split('---')[1].trim().split('\n').map(line=>{const i=line.indexOf(': ');return [line.slice(0,i),JSON.parse(line.slice(i+2))];}));
const pubs=new Map(readdirSync('src/content/publications').filter(f=>f.endsWith('.md')).map(f=>[f,parse(f)]));
assert.equal(profile.allRowsLoaded,true,'Incomplete Scholar pagination');
const expected=new Set(profile.articles.map(a=>a.id));
const actual=new Map();
const dois=new Map();
for(const [file,p] of pubs){
 for(const id of p.scholarIds??[]){assert(!actual.has(id),`Scholar ID duplicated: ${id}`);actual.set(id,file);}
 if(p.doi){const key=p.doi.toLowerCase();assert(!dois.has(key),`Duplicate DOI: ${key}`);dois.set(key,file);}
 if(p.scholarIds?.length)assert(p.scholarUrl?.includes(p.scholarIds[0]),`Missing canonical Scholar link: ${file}`);
 assert(!p.authors.some(a=>/\.\.\.|…/.test(a)),`Truncated author list: ${file}`);
 assert(p.year>1900&&p.year<2100,`Invalid year: ${file}`);
}
assert.deepEqual(new Set(actual.keys()),expected,'Not all Scholar entries are represented');
assert.equal(coverage.coverage.length,expected.size);
for(const row of coverage.coverage)assert.equal(actual.get(row.scholarId),row.file);
for(const [file,old] of Object.entries(baseline)){
 const p=pubs.get(file);assert(p,`Original record removed: ${file}`);
 assert.equal(p.abstract??'',old.abstract??'',`Original abstract lost: ${file}`);
 for(const r of old.resources??[])assert(p.resources.some(x=>x.url===r.url&&x.label===r.label),`Original resource lost: ${file}`);
}
const merged=coverage.coverage.filter(r=>r.scholarId==='_5tno0g5mFcC'||r.scholarId==='6ZxmRoH8BuwC');
assert.equal(merged.length,2);assert.equal(merged[0].file,merged[1].file,'DARS duplicate not merged');
const thesis=pubs.get(actual.get('IRz6iEL74y4C'));assert.equal(thesis.publicationType,'thesis');assert.deepEqual(thesis.authors,['Kevin Aubert De Luchi Lomellini']);
const sblimp=pubs.get(actual.get('anf4URPfarAC'));assert(sblimp.bibtex.includes(sblimp.authors.join(' and ')),'SBlimp BibTeX author order differs');assert(sblimp.bibtex.includes(sblimp.doi),'SBlimp BibTeX DOI differs');
console.log(`✓ ${expected.size} Scholar entries covered by ${new Set(actual.values()).size} distinct works; ${pubs.size} total publications. Original records, abstracts, and resources retained.`);
