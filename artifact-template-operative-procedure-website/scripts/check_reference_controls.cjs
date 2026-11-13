// Focused regression check for the actual reference input handlers. Run with Node.js.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = path.resolve(__dirname, '../assets/source');
const runtime = fs.readFileSync(path.join(source, 'assets/app.js'), 'utf8');
const html = fs.readFileSync(path.join(source, 'index.html'), 'utf8');
new vm.Script(runtime);
assert(!/operativeView|setOperativeView/.test(runtime + html), 'Removed camera action must not survive');
const start = runtime.indexOf('    // Pointer input:');
const end = runtime.indexOf("    canvas.addEventListener('webglcontextlost'", start);
assert(start >= 0 && end > start);
const events = {}, windowEvents = {}, turns = [], rolls = [], zooms = [], picks = [];
const canvas = { setPointerCapture() {}, getBoundingClientRect: () => ({left:0, top:0, width:800, height:600}), addEventListener: (k,v) => events[k] = v };
const context = {canvas, window:{addEventListener:(k,v) => windowEvents[k] = v}, host:{clientHeight:600},
  distance:10, scale:1, viewZoom:1, pan:[0,0], available:true,
  stopGlide() {}, render() {}, draw() {}, cacheLabelVisibility() {}, clearSelection() {},
  rotateByDrag:(...a) => turns.push(a), rollView:a => rolls.push(a), zoomBy:a => zooms.push(a),
  pickIdAt:() => 7, select:id => picks.push(id), $:() => ({click(){}})};
vm.runInNewContext(runtime.slice(start,end), context);
const event = (x,y,extra={}) => ({pointerId:1,clientX:x,clientY:y,button:0,buttons:1,altKey:false,shiftKey:false,preventDefault(){},...extra});
const move = (x,y,extra) => canvas.onpointermove(event(x,y,extra));
canvas.onpointerdown(event(0,0));
move(20,30); move(40,50);
assert.equal(turns.length,0,'Plain drag must stay fixed');
move(45,55,{altKey:true});
assert.deepEqual(turns.pop(),[5,5],'Pressing Alt mid-drag must not accumulate prior motion');
move(70,90);
assert.equal(turns.length,0,'Releasing Alt must immediately stop rotation');
move(72,91,{altKey:true});
assert.deepEqual(turns.pop(),[2,1]);
canvas.onpointerup(event(72,91));
assert.equal(picks.length,0,'Dragging must not select');
for(const key of ['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','q','Q','e','E']) canvas.onkeydown({...event(0,0),key});
assert.equal(turns.length+rolls.length,0,'Unmodified keys must not rotate or roll');
canvas.onkeydown({...event(0,0,{altKey:true}),key:'ArrowRight'});
canvas.onkeydown({...event(0,0,{altKey:true}),key:'q'});
assert.equal(turns.length,1); assert.equal(rolls.length,1);
turns.length=rolls.length=0;
canvas.onpointerdown(event(10,10)); move(30,25,{shiftKey:true});
assert(context.pan[0]!==0 && context.pan[1]!==0); assert.equal(turns.length,0);
canvas.onpointerup(event(30,25));
canvas.onpointerdown(event(10,10)); move(20,20,{buttons:2}); canvas.onpointerup(event(20,20,{button:2}));
assert.equal(turns.length,0);
canvas.onpointerdown(event(10,10,{pointerType:'touch'})); move(30,25,{pointerType:'touch'});
assert.equal(turns.length,0,'One finger must not rotate');
canvas.onpointerdown(event(100,25,{pointerId:2,pointerType:'touch'}));
move(120,60,{pointerId:2,pointerType:'touch'});
assert.equal(rolls.length,0,'Unmodified pinch/twist must not roll'); assert(zooms.length>0);
canvas.onpointerup(event(30,25,{pointerType:'touch'})); canvas.onlostpointercapture();
canvas.onpointerup(event(120,60,{pointerId:2,pointerType:'touch'})); assert.equal(picks.length,0);
for(const cancel of [canvas.onpointercancel,canvas.onlostpointercapture,windowEvents.blur]) {
  canvas.onpointerdown(event(0,0,{altKey:true})); cancel(event(0,0)); move(30,40,{altKey:true});
  assert.equal(turns.length,0,'Cancelled/blurred gesture must not rotate');
}
canvas.onpointerdown(event(10,10)); canvas.onpointerup(event(10,10)); assert.deepEqual(picks,[7]);
canvas.onpointerdown(event(10,10,{altKey:true})); canvas.onpointerup(event(10,10,{altKey:true})); assert.deepEqual(picks,[7]);
const prior=zooms.length;
events.wheel({...event(0,0),deltaY:20,deltaMode:0}); canvas.onkeydown({...event(0,0),key:'+'});
assert.equal(zooms.length,prior+2,'Wheel and keyboard zoom must still work');
console.log('PASS: syntax, removed camera action, hold/release/re-press rotation, keyboard, pan, touch, zoom, picking, cancellation and blur');
