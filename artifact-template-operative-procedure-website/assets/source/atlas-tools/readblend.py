import struct,re,json,bisect
from pathlib import Path
class Blend:
 def __init__(self,path):
  self.raw=Path(path).read_bytes();h=self.raw[:12];print('Blend header:',h)
  assert h[:7]==b'BLENDER';self.ptr=8 if h[7:8]==b'-' else 4;self.endian='<' if h[8:9]==b'v' else '>';self.blocks=[];pos=12
  fmt=self.endian+('4sIQII' if self.ptr==8 else '4sIIII');sz=struct.calcsize(fmt)
  while pos+sz<=len(self.raw):
   code,size,addr,dna,count=struct.unpack_from(fmt,self.raw,pos);pos+=sz
   b={'code':code.decode('ascii','replace').rstrip('\0'),'size':size,'addr':addr,'dna':dna,'count':count,'pos':pos};self.blocks.append(b)
   if code==b'DNA1':self.dna(self.raw[pos:pos+size])
   pos+=size
   if code==b'ENDB':break
  self.map={b['addr']:b for b in self.blocks if b['addr']};self.sorted=sorted(self.map);self.bytype={}
  for b in self.blocks:
   b['type']=self.structs[b['dna']]['name']
   self.bytype.setdefault(b['type'],[]).append(b)
 def dna(self,d):
  assert d[:8]==b'SDNANAME';p=8;n=struct.unpack_from(self.endian+'I',d,p)[0];p+=4
  names=[]
  for _ in range(n):q=d.index(0,p);names.append(d[p:q].decode());p=q+1
  p=(p+3)&~3;assert d[p:p+4]==b'TYPE';p+=4;n=struct.unpack_from(self.endian+'I',d,p)[0];p+=4;types=[]
  for _ in range(n):q=d.index(0,p);types.append(d[p:q].decode());p=q+1
  p=(p+3)&~3;assert d[p:p+4]==b'TLEN';p+=4;lens=struct.unpack_from(self.endian+str(n)+'H',d,p);p+=n*2;p=(p+3)&~3
  assert d[p:p+4]==b'STRC';p+=4;n=struct.unpack_from(self.endian+'I',d,p)[0];p+=4
  self.structs=[];self.types={};self.lens=dict(zip(types,lens))
  for i in range(n):
   ti,nf=struct.unpack_from(self.endian+'HH',d,p);p+=4;fields={};off=0
   for _ in range(nf):
    ft,fn=struct.unpack_from(self.endian+'HH',d,p);p+=4;rawname=names[fn];cnt=1
    for a in re.findall(r'\[(\d+)\]',rawname):cnt*=int(a)
    pointer='*' in rawname;size=(self.ptr if pointer else lens[ft])*cnt
    name=re.sub(r'\[.*','',rawname).replace('*','').replace('(','').replace(')','')
    fields[name]={'offset':off,'size':size,'type':types[ft],'pointer':pointer,'count':cnt,'raw':rawname};off+=size
   s={'name':types[ti],'size':lens[ti],'fields':fields,'sumsize':off};self.structs.append(s);self.types[s['name']]=s
 def find(self,addr,owner=None):
  if owner is not None:
   matches=[x for x in self.blocks if x['addr']==addr and x['pos']>owner['pos']]
   if matches:return min(matches,key=lambda x:x['pos']),0
  if addr in self.map:return self.map[addr],0
  i=bisect.bisect_right(self.sorted,addr)-1
  if i>=0:
   b=self.map[self.sorted[i]];o=addr-b['addr']
   if o<b['size']:return b,o
  raise KeyError(hex(addr))
 def fieldpos(self,b,field,index=0,typename=None):
  s=self.types[typename or b['type']];pos=b['pos']+index*s['size'];parts=field.split('.')
  for part in parts:
   f=s['fields'][part];pos+=f['offset']
   if not f['pointer'] and f['type'] in self.types:s=self.types[f['type']]
  return pos,f
 def get(self,b,field,index=0,typename=None):
  p,f=self.fieldpos(b,field,index,typename)
  if f['pointer']:fmt='Q' if self.ptr==8 else 'I';return struct.unpack_from(self.endian+fmt,self.raw,p)[0]
  if f['type']=='char':return self.raw[p:p+f['size']].split(b'\0')[0].decode('utf-8','replace')
  fmt={'short':'h','ushort':'H','int':'i','float':'f','double':'d','int64_t':'q','uint64_t':'Q','uint':'I'}.get(f['type'])
  if fmt:
   v=struct.unpack_from(self.endian+str(f['count'])+fmt,self.raw,p);return v[0] if f['count']==1 else v
  return self.raw[p:p+f['size']]
