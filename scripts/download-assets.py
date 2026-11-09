"""Mirror the exact public assets listed by the WordPress import; no credentials needed."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request,urlopen
from urllib.parse import quote
import json,time
ROOT=Path(__file__).resolve().parents[1]
assets=json.loads((ROOT/'migration/assets.json').read_text())
def download(item):
    url,path=item; target=ROOT/'public'/path.lstrip('/')
    if target.exists() and target.stat().st_size: return dict(url=url,path=path,status='cached',bytes=target.stat().st_size)
    for attempt in range(3):
        try:
            req=Request(quote(url,safe=':/?=&%'),headers={'User-Agent':'SwarmsLab-Website-Migration/1.0'})
            with urlopen(req,timeout=40) as response: data=response.read()
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            return dict(url=url,path=path,status='downloaded',bytes=len(data))
        except Exception as e:
            error=str(e)
            if attempt<2:time.sleep(1)
    return dict(url=url,path=path,status='failed',error=error)
with ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(download,assets.items()))
(ROOT/'migration/asset-report.json').write_text(json.dumps(results,indent=2)+'\n')
failed=[r for r in results if r['status']=='failed']
print(json.dumps(dict(assets=len(results),failed=failed,totalBytes=sum(r.get('bytes',0) for r in results)),indent=2))
raise SystemExit(bool(failed))
