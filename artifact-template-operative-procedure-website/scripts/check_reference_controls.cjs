// Focused regression check for the reference camera and responsive interaction handlers.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = path.resolve(__dirname, '../assets/source');
const runtime = fs.readFileSync(path.join(source, 'assets/app.js'), 'utf8');
const html = fs.readFileSync(path.join(source, 'index.html'), 'utf8');
new vm.Script(runtime);
assert(!/operativeView|setOperativeView/.test(runtime + html), 'Removed camera action must not survive');
const start = runtime.indexOf('    // A plain one-pointer drag');
const end = runtime.indexOf("    canvas.addEventListener('webglcontextlost'", start);
assert(start >= 0 && end > start, 'Camera handlers should be present');
const events = {}, turns = [], tilts = [], yaws = [], rolls = [], zooms = [], picks = [], renders = [];
const canvas = { setPointerCapture() {}, getBoundingClientRect: () => ({left:0,top:0,width:800,height:600}), addEventListener:(k,v)=>events[k]=v };
const context = {canvas, host:{clientHeight:600}, distance:10, scale:1, viewZoom:1, pan:[0,0], available:true,
  stopGlide(){}, markInteraction(){}, render(...a){renders.push(a)}, draw(){}, cacheLabelVisibility(){}, clearSelection(){},
  rotateByDrag:(...a)=>turns.push(a), tiltByDrag:(...a)=>tilts.push(a), yawByDrag:(...a)=>yaws.push(a), rollView:a=>rolls.push(a),
  zoomBy:(...a)=>zooms.push(a), pickIdAt:()=>7, select:id=>picks.push(id), $:()=>({click(){}}), wrapAngle:a=>a};
vm.runInNewContext(runtime.slice(start,end), context);
const event=(x,y,extra={})=>({pointerId:1,clientX:x,clientY:y,button:0,buttons:1,altKey:false,shiftKey:false,preventDefault(){},...extra});
const move=(x,y,extra)=>canvas.onpointermove(event(x,y,extra));
canvas.onpointerdown(event(0,0)); move(20,0); move(30,14);
assert.deepEqual(tilts,[[0],[14]],'Plain drag should tilt only from vertical movement');
assert.equal(yaws.length,0,'Plain horizontal drag must not yaw');
move(36,21,{altKey:true}); assert.deepEqual(yaws,[[6]],'Alt/Option horizontal drag should yaw by only the current delta');
move(38,27); assert.equal(yaws.length,1,'Releasing Alt/Option must stop horizontal yaw');
assert.deepEqual(tilts.at(-1),[6],'Vertical movement without Alt/Option remains available');
canvas.onpointerup(event(38,27)); assert.equal(picks.length,0,'A drag must not select anatomy');
canvas.onpointerdown(event(10,10)); move(30,25,{shiftKey:true}); assert(context.pan[0]!==0 && context.pan[1]!==0,'Shift drag should pan'); canvas.onpointerup(event(30,25));
canvas.onpointerdown(event(10,10)); move(20,20,{buttons:2}); canvas.onpointerup(event(20,20,{button:2})); assert.equal(yaws.length,1);
canvas.onpointerdown(event(10,10,{pointerType:'touch'})); move(30,25,{pointerType:'touch'}); assert.equal(yaws.length,1,'Single-finger horizontal drag must not yaw');
canvas.onpointerdown(event(100,25,{pointerId:2,pointerType:'touch'})); move(120,60,{pointerId:2,pointerType:'touch'});
assert(zooms.some(x=>x[1]===false),'Pinch zoom should avoid an immediate picking refresh');
canvas.onpointerup(event(30,25,{pointerType:'touch'})); canvas.onpointerup(event(120,60,{pointerId:2,pointerType:'touch'})); assert.equal(picks.length,0,'Multi-touch must not select anatomy');
canvas.onpointerdown(event(10,10)); canvas.onpointerup(event(10,10)); assert.deepEqual(picks,[7],'Click selection should remain immediate');
const prior=zooms.length; events.wheel({...event(0,0),deltaY:20,deltaMode:0}); canvas.onkeydown({...event(0,0),key:'+'});
assert.equal(zooms.length,prior+2,'Wheel and keyboard zoom should work');
assert(renders.some(x=>x[0]===false),'Camera movement should render without picking every frame');
console.log('PASS: syntax, removed camera action, vertical tilt, gated side-to-side yaw, pan, touch, zoom, picking and low-latency render path');
