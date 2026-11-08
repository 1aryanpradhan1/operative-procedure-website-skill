#!/usr/bin/env python3
"""Package an adapted procedure project as offline HTML and a compressed static ZIP."""
import argparse,base64,gzip,hashlib,json,mimetypes,re,shutil,zipfile
from pathlib import Path

def inline_assets(text,mapping):
 for name,url in mapping.items():
  for path in [name,'./'+name,'/'+name]:
   for quote in ['"',"'",'`']:
    text=text.replace(quote+path+quote,quote+url+quote)
   text=text.replace('url('+path+')','url('+url+')')
 return text

def inline_data(value,mapping):
 if isinstance(value,str):
  embedded=mapping.get(value,mapping.get(value.removeprefix('./').removeprefix('/'),value))
  if embedded.startswith(('assets/','./assets/','/assets/')):raise SystemExit('Unresolved local data asset: '+value+'. Put it in project/static or embed it explicitly.')
  return embedded
 if isinstance(value,list):return [inline_data(x,mapping)for x in value]
 if isinstance(value,dict):return {k:inline_data(v,mapping)for k,v in value.items()}
 return value

def require_embedded_dependencies(html):
 refs=re.findall(r"\b(?:src|href|poster)=[\"']([^\"']+)[\"']",html)
 refs+=re.findall(r"url\(\s*[\"']?([^\s\"')]+)",html)
 bad=[ref for ref in refs if not ref.startswith(('#','//','data:','https:','http:','mailto:','tel:','blob:'))]
 if bad:raise SystemExit('Unresolved local assets in offline HTML: '+', '.join(sorted(set(bad)))+'. Put media under project/static with matching paths or embed it explicitly.')
 if re.search(r'\bsrcset=',html,re.I):raise SystemExit('Inline responsive image sources explicitly before building; automatic srcset rewriting is unsupported.')

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--project',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
 p.add_argument('--slug',default='procedure')
 p.add_argument('--include-full-text',action='store_true',help='Include article text/PDF payloads in the hosted version only when redistribution is permitted.')
 a=p.parse_args();project=a.project.resolve();out=a.output.resolve()
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',a.slug):raise SystemExit('Use a lowercase hyphenated slug.')
 if out.exists():raise SystemExit('Choose a new output directory; prior outputs are never overwritten.')
 html=(project/'src/index.html').read_text();runtime=(project/'src/app.js').read_text()
 if any(html.count(tag)!=1 for tag in ['<!-- GUIDE_DATA -->','<!-- GUIDE_RUNTIME -->']):raise SystemExit('Expected one data marker and one runtime marker.')
 if '</script' in runtime.lower():raise SystemExit('Escape literal closing script tags in the runtime before embedding.')
 if 'window.__GUIDE_DATA__' not in runtime:raise SystemExit('Keep the dual offline/hosted data reader from materialize_site.py, or adapt this packager to your new reader.')
 data={path.stem:json.loads(path.read_text())for path in sorted((project/'data').glob('*.json'))}
 if not isinstance(data.get('mesh-data'),list) or not data['mesh-data']:raise SystemExit('Provide a nonempty mesh-data array.')
 if len({m['id']for m in data['mesh-data']})!=len(data['mesh-data']):raise SystemExit('Mesh IDs must be unique.')
 static=project/'static';static_files=[];mapping={}
 if static.exists():
  for path in sorted(static.rglob('*')):
   if path.is_symlink():raise SystemExit('Static assets must be regular files, not symlinks.')
   if not path.is_file():continue
   name=path.relative_to(static).as_posix()
   if name in {'index.html','_headers','netlify.toml','assets/app.js','assets/loader.js'}or re.fullmatch(r'assets/anatomy-\d+\.bin',name):raise SystemExit('Static asset conflicts with generated runtime: '+name)
   if path.suffix.lower()in {'.js','.mjs','.css','.html'}:raise SystemExit('Bundle frontend code/styles into src/index.html and src/app.js; static/ is for media and other data assets.')
   mime=mimetypes.guess_type(name)[0]or'application/octet-stream'
   mapping[name]='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
   static_files.append((path,name))
 offline_data=inline_data(data,mapping)
 tags='\n'.join('<script type="application/json" id="'+key+'">'+json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')+'</script>'for key,value in offline_data.items())
 offline_base=inline_assets(html,mapping);offline_runtime=inline_assets(runtime,mapping)
 require_embedded_dependencies(offline_base)
 if re.search(r'''["'`]((?:\./|/)?assets/[^"'`]+)["'`]''',offline_runtime):raise SystemExit('Unresolved local runtime asset. Put exact media paths in project/static; embed computed/dynamic paths explicitly.')
 out.mkdir(parents=True);site=out/'site';assets=site/'assets';assets.mkdir(parents=True)
 offline=offline_base.replace('<!-- GUIDE_DATA -->',tags).replace('<!-- GUIDE_RUNTIME -->','<script>\n'+offline_runtime+'\n</script>')
 (out/f'{a.slug}-anatomy-guide.html').write_text(offline)
 hosted_data=dict(data)
 if not a.include_full_text:
  if 'paper-source-data'in hosted_data:hosted_data['paper-source-data']={}
  if 'pdf-data'in hosted_data:hosted_data['pdf-data']=''
 payload=json.dumps(hosted_data,ensure_ascii=False,separators=(',',':')).encode()
 compressed=gzip.compress(payload,compresslevel=9,mtime=0);chunks=[];chunk_size=7*1048576
 for i,start in enumerate(range(0,len(compressed),chunk_size)):
  name=f'assets/anatomy-{i+1:02d}.bin';(site/name).write_bytes(compressed[start:start+chunk_size]);chunks.append(name)
 assert gzip.decompress(b''.join((site/name).read_bytes()for name in chunks))==payload
 loading='<div id="guide-loading" role="status" aria-live="polite" style="position:fixed;inset:0;z-index:9999;display:grid;place-content:center;background:#101b20;color:#e5efdf;padding:30px;font:16px system-ui;text-align:center"><span id="guide-loading-message">Loading Anatomy…</span></div><noscript>This interactive guide requires JavaScript.</noscript>'
 body_tags=list(re.finditer(r'<body\b[^>]*>',html,re.I))
 if len(body_tags)!=1:raise SystemExit('Expected one body tag; update the loading insertion for this HTML.')
 body_tag=body_tags[0].group(0)
 hosted=html.replace('<!-- GUIDE_DATA -->','').replace('<!-- GUIDE_RUNTIME -->','<script defer src="assets/loader.js"></script>').replace(body_tag,body_tag+loading,1)
 (site/'index.html').write_text(hosted);(assets/'app.js').write_text(runtime)
 for path,name in static_files:
  target=site/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
 loader=r'''(async()=>{'use strict';
const files=__FILES__, expectedMeshCount=__COUNT__, message=document.getElementById('guide-loading-message');
try{
 if(typeof DecompressionStream==='undefined')throw new Error('Please open this guide in a current version of Chrome, Edge, Firefox or Safari.');
 let completed=0;
 const stream=new ReadableStream({async start(controller){try{for(const file of files){const response=await fetch(file);if(!response.ok)throw new Error('Anatomy data could not be loaded ('+response.status+').');const reader=response.body.getReader();while(true){const {done,value}=await reader.read();if(done)break;controller.enqueue(value)}message.textContent='Loading Anatomy… '+Math.round(++completed/files.length*100)+'%'}controller.close()}catch(error){controller.error(error)}}});
 const data=await new Response(stream.pipeThrough(new DecompressionStream('gzip'))).json();
 if(!Array.isArray(data['mesh-data'])||data['mesh-data'].length!==expectedMeshCount)throw new Error('Anatomy data is incomplete. Please refresh the page.');
 window.__GUIDE_DATA__=data;
 const script=document.createElement('script');script.src='assets/app.js';script.onload=()=>document.getElementById('guide-loading')?.remove();script.onerror=()=>{message.textContent='The guide could not be loaded. Please refresh the page.'};document.body.append(script);
}catch(error){message.textContent=error.message||'Anatomy could not be loaded. Please refresh the page.';console.error(error)}
})();'''.replace('__FILES__',json.dumps(chunks)).replace('__COUNT__',str(len(data['mesh-data'])))
 (assets/'loader.js').write_text(loader)
 (site/'_headers').write_text('/assets/anatomy-*.bin\n  Content-Type: application/octet-stream\n  Cache-Control: public, max-age=0, must-revalidate\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n')
 (site/'netlify.toml').write_text('[build]\n  publish = "."\n')
 attribution=project/'ATTRIBUTION.md'
 if attribution.exists():(site/'ATTRIBUTION.md').write_bytes(attribution.read_bytes())
 files=sorted(path for path in site.rglob('*')if path.is_file());archive=out/f'{a.slug}-netlify.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for path in files:z.write(path,path.relative_to(site))
 with zipfile.ZipFile(archive)as z:
  assert z.testzip()is None and 'index.html'in z.namelist()
  assert all(z.read(str(path.relative_to(site)))==path.read_bytes()for path in files)
 report={'siteBytes':sum(path.stat().st_size for path in files),'largestFileBytes':max(path.stat().st_size for path in files),'zipBytes':archive.stat().st_size,'meshCount':len(data['mesh-data']),'dataIds':sorted(data),'hostedFullText':a.include_full_text,'staticAssetCount':len(static_files),'payloadSha256':hashlib.sha256(payload).hexdigest(),'verified':['lossless compression round-trip','ZIP integrity','root index.html','ZIP/source equality'],'notVerified':['anatomical accuracy','procedure adaptation','actual browser rendering'],'adaptationStatus':json.loads((project/'adaptation-status.json').read_text())if(project/'adaptation-status.json').exists()else None}
 (out/'package-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'offline':str(out/f'{a.slug}-anatomy-guide.html'),'zip':str(archive),**report}))
if __name__=='__main__':main()
