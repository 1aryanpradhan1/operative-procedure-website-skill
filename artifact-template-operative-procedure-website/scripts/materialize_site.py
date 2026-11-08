#!/usr/bin/env python3
"""Copy the retained working website and expose its editable runtime and JSON data."""
import argparse,gzip,json,re,shutil
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--skill-dir',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 a=p.parse_args();source=a.skill_dir.resolve()/'assets/source';dest=a.output.resolve()
 if dest.exists():raise SystemExit('Choose a new empty project path; existing projects are never overwritten.')
 if not (source/'index.html').is_file():raise SystemExit('Retained website source is missing.')
 html=(source/'index.html').read_text()
 loader=(source/'assets/loader.js').read_text()
 chunks=json.loads(re.search(r'const files=(\[.*?\]), message=',loader,re.S).group(1))
 pieces=[]
 for name in chunks:
  path=(source/name).resolve()
  if not path.is_relative_to(source):raise SystemExit('Invalid retained asset path.')
  pieces.append(path.read_bytes())
 meshes=json.loads(gzip.decompress(b''.join(pieces)))
 payloads={'mesh-data':meshes}
 def remove_payload(m):
  key,text=m.group(1),m.group(2)
  payloads[key]=text if key=='pdf-data' else json.loads(text)
  return ''
 html=re.sub(r'<script type="application/json" id="([a-z0-9-]+)">(.*?)</script>',remove_payload,html,flags=re.S)
 runtime=(source/'assets/app.js').read_text()
 old="read=id=>id==='mesh-data'?window.__PTERIONAL_MESHES__:JSON.parse($('#'+id).textContent)"
 new="read=id=>window.__GUIDE_DATA__?.[id]??JSON.parse($('#'+id).textContent)"
 if runtime.count(old)!=1:raise SystemExit('Unexpected reference runtime; inspect its data reader before adapting.')
 runtime=runtime.replace(old,new)
 runtime_tag='<script defer src="assets/loader.js"></script>'
 if html.count(runtime_tag)!=1:raise SystemExit('Unexpected reference runtime insertion point.')
 html=html.replace(runtime_tag,'<!-- GUIDE_DATA -->\n<!-- GUIDE_RUNTIME -->')
 html=re.sub(r'<div id="anatomy-loading".*?</div>','',html,count=1,flags=re.S)
 html=re.sub(r'<noscript>.*?</noscript>','',html,count=1,flags=re.S)
 (dest/'src').mkdir(parents=True);(dest/'data').mkdir();(dest/'research').mkdir();(dest/'static').mkdir()
 shutil.copytree(source,dest/'baseline')
 (dest/'src/index.html').write_text(html);(dest/'src/app.js').write_text(runtime)
 for key,value in payloads.items():(dest/'data'/f'{key}.json').write_text(json.dumps(value,ensure_ascii=False,separators=(',',':')))
 shutil.copy2(source/'ATTRIBUTION.md',dest/'ATTRIBUTION.md')
 (dest/'adaptation-status.json').write_text(json.dumps({'referenceCase':'Pterional Craniotomy','status':'unadapted reference','required':'Replace procedure content, sources, anatomy, masks, markers, instruments, laterality logic and all case-specific runtime branches before delivering another procedure.'},indent=2))
 print(json.dumps({'project':str(dest),'meshCount':len(meshes),'dataIds':sorted(payloads),'status':'Editable reference copied; no new procedure has been generated.'}))
if __name__=='__main__':main()
