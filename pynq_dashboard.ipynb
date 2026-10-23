import threading, time, webbrowser, re
from datetime import datetime
import serial
import serial.tools.list_ports
from flask import Flask, jsonify, render_template_string

PORT = 'COM3'  # Change to your ESP32 COM port if different
BAUD = 115200
HOST, WEB_PORT = '127.0.0.1', 5000

state = dict(voltage=0.0, current=0.0, temperature=0.0, power=0.0,
             pot_v=0, pot_i=0, pot_t=0, fault=0, sensor_ok=1,
             connected=False, last_update='--:--:--', port=PORT)
lock = threading.Lock()

def autodetect():
    ports = list(serial.tools.list_ports.comports())
    keys = ('CP210','SILICON','CH340','ESP32','ESPRESSIF','USB-SERIAL','FTDI','UART')
    for p in ports:
        s = f'{p.description or ""} {p.manufacturer or ""}'.upper()
        if any(k in s for k in keys): return p.device
    return ports[0].device if len(ports)==1 else None

def parse(line):
    if not line.startswith('V='): return None
    try:
        d={}
        for x in line.split(','):
            if '=' in x:
                k,v=x.split('=',1); d[k]=v
        v=float(d['V'])/1000
        i=float(d['I'])/1000
        t=float(d['T'])/100
        return dict(voltage=v,current=i,temperature=t,
                    power=(float(d['P']) if 'P' in d else v*i),
                    pot_v=int(float(d.get('PV',0))),
                    pot_i=int(float(d.get('PI',0))),
                    pot_t=int(float(d.get('PT',0))),
                    fault=int(float(d.get('F',0))),
                    sensor_ok=int(float(d.get('S',1))),
                    last_update=datetime.now().strftime('%H:%M:%S'),connected=True)
    except (KeyError, ValueError): return None

def reader():
    global PORT
    while True:
        p=PORT or autodetect()
        if not p:
            with lock: state['connected']=False
            time.sleep(2); continue
        try:
            with serial.Serial(p,BAUD,timeout=1) as ser:
                with lock: state['port']=p; state['connected']=True
                while True:
                    b=ser.readline()
                    if not b: continue
                    pkt=parse(b.decode(errors='ignore').strip())
                    if pkt:
                        with lock: state.update(pkt)
        except (serial.SerialException,OSError):
            with lock: state['connected']=False
            time.sleep(2)

app=Flask(__name__)
PAGE=r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Adapter Safety Dashboard</title>
<style>
:root{--bg:#07101d;--panel:#101b2d;--panel2:#142139;--text:#edf3ff;--muted:#8fa0bd;--border:#263754;--green:#2bd7a7;--yellow:#ffc94a;--red:#ff5875;--blue:#55a8ff;--purple:#a98bff}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(circle at 10% 0%,#132541 0,#07101d 38%,#060d18 100%);color:var(--text);font-family:Inter,Segoe UI,Arial,sans-serif}
.wrap{max-width:1240px;margin:auto;padding:26px 20px 40px}
.head{display:flex;justify-content:space-between;align-items:center;gap:15px;margin-bottom:20px}
.title h1{margin:0;font-size:28px;letter-spacing:.2px}
.title p{margin:7px 0 0;color:var(--muted);font-size:13px}
.conn{padding:11px 14px;border:1px solid var(--border);background:rgba(16,27,45,.92);border-radius:13px;text-align:right;min-width:190px;box-shadow:0 10px 28px rgba(0,0,0,.16)}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.dot.on{background:var(--green);box-shadow:0 0 12px rgba(43,215,167,.45)}
.dot.off{background:var(--red)}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.card,.trend-card{background:rgba(16,27,45,.95);border:1px solid var(--border);border-radius:17px;box-shadow:0 14px 32px rgba(0,0,0,.2)}
.card{padding:18px}
.label{font-size:12px;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.7px}
.value{font-size:33px;font-weight:780;line-height:1.1}
.unit{font-size:14px;color:var(--muted)}
h2{margin:0 0 14px;font-size:18px}
.row{display:grid;grid-template-columns:1.2fr .8fr;gap:14px;margin-top:14px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.item{display:flex;justify-content:space-between;align-items:center;background:#142139;border:1px solid var(--border);padding:12px;border-radius:12px}
.badge{font-size:12px;font-weight:750;padding:6px 10px;border-radius:999px}
.good{background:var(--green);color:#042319}
.warn{background:var(--yellow);color:#2b2000}
.bad{background:var(--red);color:#350610}
.neutral{background:var(--blue);color:#041827}

/* Live trend styling */
.trend-section{margin-top:18px}
.trend-section-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:12px}
.trend-section-head h2{margin:0;font-size:21px}
.trend-section-head p{margin:5px 0 0;color:var(--muted);font-size:12px}
.live-pill{display:flex;align-items:center;gap:8px;padding:7px 11px;border:1px solid var(--border);background:rgba(16,27,45,.95);border-radius:999px;color:var(--green);font-size:11px;font-weight:800;letter-spacing:.8px}
.pulse{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 0 rgba(43,215,167,.5);animation:pulse 1.5s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(43,215,167,.5)}70%{box-shadow:0 0 0 8px rgba(43,215,167,0)}100%{box-shadow:0 0 0 0 rgba(43,215,167,0)}}
.trend-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.trend-card{padding:15px;background:linear-gradient(145deg,rgba(20,33,57,.97),rgba(14,26,44,.97))}
.trend-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:10px}
.trend-name{display:block;font-size:15px;font-weight:760}
.trend-head small{display:block;color:var(--muted);font-size:10px;margin-top:3px}
.trend-head b{font-size:18px;white-space:nowrap}
canvas{width:100%;height:auto;background:#091525;border-radius:13px;border:1px solid var(--border);display:block}
.trend-meta{display:flex;justify-content:space-between;align-items:center;padding-top:7px;color:#617494;font-size:10px}
.trend-meta .limit{color:var(--yellow);font-weight:750}
@media(max-width:850px){.cards{grid-template-columns:repeat(2,1fr)}.row{grid-template-columns:1fr}.trend-grid{grid-template-columns:1fr}}
@media(max-width:520px){.head{flex-direction:column;align-items:stretch}.cards{grid-template-columns:1fr}.trend-section-head{align-items:flex-start;flex-direction:column}}
</style></head><body><div class="wrap">
<div class="head"><div class="title"><h1>FPGA Adapter Safety Dashboard</h1><p>Live sensor and safety monitoring via USB Serial</p></div><div class="conn" id="conn">● Disconnected<br><small id="port">Port: --</small></div></div>
<div class="cards"><div class="card"><div class="label">VOLTAGE</div><div class="value" id="v">0.00 <span class="unit">V</span></div></div><div class="card"><div class="label">CURRENT</div><div class="value" id="i">0.000 <span class="unit">A</span></div></div><div class="card"><div class="label">TEMPERATURE</div><div class="value" id="t">0.0 <span class="unit">°C</span></div></div><div class="card"><div class="label">POWER</div><div class="value" id="p">0.000 <span class="unit">W</span></div></div></div>
<div class="row"><div class="card"><h2>Safety Status</h2><div class="grid"><div class="item"><span>Sensor</span><b id="sensor" class="badge good">OK</b></div><div class="item"><span>Fault</span><b id="fault" class="badge good">NO FAULT</b></div><div class="item"><span>Warning</span><b id="warning" class="badge good">NORMAL</b></div><div class="item"><span>Last Update</span><b id="time">--:--:--</b></div></div></div><div class="card"><h2>Fault Test Inputs</h2><div class="grid"><div class="item"><span>Voltage Pot</span><b id="pv">0%</b></div><div class="item"><span>Current Pot</span><b id="pi">0%</b></div><div class="item"><span>Temp Pot</span><b id="pt">0%</b></div><div class="item"><span>USB</span><b id="usb" class="badge bad">OFFLINE</b></div></div></div></div>
<div class="trend-section">
<div class="trend-section-head">
  <div><h2>Live Trends</h2><p>Real-time sensor history · last 80 samples</p></div>
  <div class="live-pill"><span class="pulse"></span> LIVE</div>
</div>
<div class="trend-grid">
  <div class="trend-card">
    <div class="trend-head"><div><span class="trend-name">Voltage</span><small>Adapter output</small></div><b id="tv">0.00 V</b></div>
    <canvas id="cv" width="700" height="250"></canvas>
    <div class="trend-meta"><span>0 V</span><span class="limit">5.5 V limit</span><span>6 V</span></div>
  </div>
  <div class="trend-card">
    <div class="trend-head"><div><span class="trend-name">Current</span><small>Load current</small></div><b id="ti">0.000 A</b></div>
    <canvas id="ci" width="700" height="250"></canvas>
    <div class="trend-meta"><span>0 A</span><span class="limit">7.5 A limit</span><span>8 A</span></div>
  </div>
  <div class="trend-card">
    <div class="trend-head"><div><span class="trend-name">Temperature</span><small>DS18B20 sensor</small></div><b id="tt">0.0 °C</b></div>
    <canvas id="ct" width="700" height="250"></canvas>
    <div class="trend-meta"><span>0 °C</span><span class="limit">40 °C limit</span><span>50 °C</span></div>
  </div>
  <div class="trend-card">
    <div class="trend-head"><div><span class="trend-name">Power</span><small>Calculated V × I</small></div><b id="tp">0.000 W</b></div>
    <canvas id="cp" width="700" height="250"></canvas>
    <div class="trend-meta"><span>0 W</span><span>Calculated live</span><span id="powerScale">10 W</span></div>
  </div>
</div>
</div>
</div><script>
const hist=[];const max=80;
function badge(id,text,cls){const e=document.getElementById(id);e.textContent=text;e.className='badge '+cls}
function drawOne(id,key,unit,minY,maxY,threshold,stroke){
  const c=document.getElementById(id),ctx=c.getContext('2d'),w=c.width,h=c.height;
  ctx.clearRect(0,0,w,h);

  const L=52,R=16,T=16,B=30,plotW=w-L-R,plotH=h-T-B;
  const range=maxY-minY || 1;

  // Grid + Y labels
  for(let n=0;n<=4;n++){
    const y=T+n*plotH/4;
    ctx.strokeStyle='#263754';
    ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(L,y);ctx.lineTo(w-R,y);ctx.stroke();

    const val=maxY-range*n/4;
    ctx.fillStyle='#7183a3';
    ctx.font='11px Segoe UI';
    ctx.textAlign='right';
    ctx.textBaseline='middle';
    ctx.fillText(val.toFixed(key==='temperature'?0:key==='current'?1:key==='power'?1:1),L-8,y);
  }

  // Safety limit
  if(threshold!==null && threshold>=minY && threshold<=maxY){
    const ty=T+(maxY-threshold)/range*plotH;
    ctx.save();
    ctx.setLineDash([7,6]);
    ctx.strokeStyle='#ffc94a';
    ctx.lineWidth=1.4;
    ctx.beginPath();ctx.moveTo(L,ty);ctx.lineTo(w-R,ty);ctx.stroke();
    ctx.restore();
    ctx.fillStyle='#ffc94a';
    ctx.font='bold 10px Segoe UI';
    ctx.textAlign='left';
    ctx.fillText('LIMIT '+threshold+unit,L+7,Math.max(11,ty-7));
  }

  ctx.fillStyle='#617494';
  ctx.font='10px Segoe UI';
  ctx.textAlign='left';
  ctx.fillText('OLDER',L,h-9);
  ctx.textAlign='right';
  ctx.fillText('NOW',w-R,h-9);

  if(hist.length<2)return;

  const visible=hist.slice(-max);
  const step=plotW/(Math.max(2,max)-1);

  // Shaded area
  ctx.beginPath();
  visible.forEach((a,j)=>{
    const x=L+j*step;
    const value=Math.max(minY,Math.min(maxY,a[key]));
    const y=T+(maxY-value)/range*plotH;
    j?ctx.lineTo(x,y):ctx.moveTo(x,y);
  });
  ctx.lineTo(L+(visible.length-1)*step,T+plotH);
  ctx.lineTo(L,T+plotH);
  ctx.closePath();

  // Convert #rrggbb to rgba for fill.
  const hex=stroke.replace('#','');
  const rr=parseInt(hex.substring(0,2),16);
  const gg=parseInt(hex.substring(2,4),16);
  const bb=parseInt(hex.substring(4,6),16);
  const gradient=ctx.createLinearGradient(0,T,0,T+plotH);
  gradient.addColorStop(0,`rgba(${rr},${gg},${bb},0.20)`);
  gradient.addColorStop(1,`rgba(${rr},${gg},${bb},0)`);
  ctx.fillStyle=gradient;
  ctx.fill();

  // Main line with glow
  ctx.beginPath();
  visible.forEach((a,j)=>{
    const x=L+j*step;
    const value=Math.max(minY,Math.min(maxY,a[key]));
    const y=T+(maxY-value)/range*plotH;
    j?ctx.lineTo(x,y):ctx.moveTo(x,y);
  });
  ctx.strokeStyle=stroke;
  ctx.lineWidth=3;
  ctx.lineJoin='round';
  ctx.lineCap='round';
  ctx.shadowColor=stroke;
  ctx.shadowBlur=8;
  ctx.stroke();
  ctx.shadowBlur=0;

  // Current point
  const last=visible[visible.length-1];
  const lastX=L+(visible.length-1)*step;
  const lastValue=Math.max(minY,Math.min(maxY,last[key]));
  const lastY=T+(maxY-lastValue)/range*plotH;

  ctx.beginPath();ctx.arc(lastX,lastY,6,0,Math.PI*2);
  ctx.fillStyle='#091525';ctx.fill();
  ctx.beginPath();ctx.arc(lastX,lastY,4,0,Math.PI*2);
  ctx.fillStyle=stroke;ctx.fill();

  // Current value label
  ctx.fillStyle=stroke;
  ctx.font='bold 11px Segoe UI';
  ctx.textAlign='right';
  ctx.fillText(
    lastValue.toFixed(key==='temperature'?1:key==='current'?3:key==='power'?3:2)+unit,
    w-R,Math.max(12,lastY-11)
  );
}

function drawAll(){
  drawOne('cv','voltage',' V',0,6.0,5.5,'#55a8ff');
  drawOne('ci','current',' A',0,8.0,7.5,'#2bd7a7');
  drawOne('ct','temperature',' °C',0,50,40,'#ffc94a');

  const pMax=Math.max(10,Math.ceil(Math.max(...hist.map(x=>x.power),0)*1.25/5)*5);
  document.getElementById('powerScale').textContent=pMax.toFixed(0)+' W';
  drawOne('cp','power',' W',0,pMax,null,'#a98bff');
}

async function refresh(){try{const d=await (await fetch('/api')).json();
  document.getElementById('v').innerHTML=d.voltage.toFixed(2)+' <span class="unit">V</span>';
  document.getElementById('i').innerHTML=d.current.toFixed(3)+' <span class="unit">A</span>';
  document.getElementById('t').innerHTML=d.temperature.toFixed(1)+' <span class="unit">°C</span>';
  document.getElementById('p').innerHTML=d.power.toFixed(3)+' <span class="unit">W</span>';
  document.getElementById('tv').textContent=d.voltage.toFixed(2)+' V';
  document.getElementById('ti').textContent=d.current.toFixed(3)+' A';
  document.getElementById('tt').textContent=d.temperature.toFixed(1)+' °C';
  document.getElementById('tp').textContent=d.power.toFixed(3)+' W';
  document.getElementById('pv').textContent=d.pot_v+'%';document.getElementById('pi').textContent=d.pot_i+'%';document.getElementById('pt').textContent=d.pot_t+'%';document.getElementById('time').textContent=d.last_update;
  document.getElementById('port').textContent='Port: '+d.port;document.getElementById('conn').innerHTML=(d.connected?'<span class="dot on"></span>Connected':'<span class="dot off"></span>Disconnected')+'<br><small id="port">Port: '+d.port+'</small>';
  document.getElementById('usb').textContent=d.connected?'ONLINE':'OFFLINE';document.getElementById('usb').className='badge '+(d.connected?'good':'bad');
  badge('sensor',d.sensor_ok?'OK':'SENSOR FAULT',d.sensor_ok?'good':'bad');badge('fault',d.fault?'FAULT':'NO FAULT',d.fault?'bad':'good');
  let warn=d.temperature>=32||d.pot_v>=70||d.pot_i>=70||d.pot_t>=70;badge('warning',warn?'WARNING':'NORMAL',warn?'warn':'good');
  hist.push({voltage:d.voltage,current:d.current,temperature:d.temperature,power:d.power});if(hist.length>max)hist.shift();drawAll();
}catch(e){}}
setInterval(refresh,500);refresh();</script></body></html>'''

@app.get('/')
def home(): return render_template_string(PAGE)
@app.get('/api')
def api():
    with lock: return jsonify(dict(state))

if __name__=='__main__':
    threading.Thread(target=reader,daemon=True).start()
    url=f'http://{HOST}:{WEB_PORT}'
    print('ESP32 Adapter Safety Dashboard')
    print('URL:',url)
    print('Serial port:',PORT)
    print('Baud:',BAUD)
    threading.Timer(1,lambda:webbrowser.open(url)).start()
    app.run(host=HOST,port=WEB_PORT,debug=False,use_reloader=False)
