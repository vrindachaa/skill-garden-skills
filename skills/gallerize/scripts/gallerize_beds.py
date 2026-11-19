#!/usr/bin/env python3
"""Bed-first botanical gallerize renderer. Focus: soil beds + pretty peony flowers."""
import argparse, json, math, html
from pathlib import Path

def e(x): return html.escape(str(x if x is not None else ''), quote=True)

PALETTES = {
  'creative': ('#9fc6f2','#f2b8cf','#ffd7a8'),
  'research': ('#a7d8cf','#c8b6f2','#ffd2b0'),
  'software-development': ('#9dbdf0','#b8a6ee','#ffc9ac'),
  'productivity': ('#b9a7e8','#f2b8d0','#ffd6a5'),
  'autonomous-ai-agents': ('#a8c6f5','#d0b8f2','#ffc5ae'),
  'media': ('#f2b8d0','#b9c8f5','#ffd8ad'),
  'email': ('#b6c8f2','#f4c0cf','#ffdab0'),
  'note-taking': ('#a7d3e8','#c8b7ef','#ffd0aa'),
  'plugin': ('#b5c8ee','#e9b9dc','#ffd0a8'),
  'web': ('#a9c7ed','#d3b9ee','#ffc9a6'),
  '(uncategorized)': ('#aebcc9','#d3c0d9','#ffd3b1'),
}
DEFAULT = ('#a9c8f2','#d0b8ef','#ffd1ad')

SPECIES = {
  'creative':'peony','research':'daisy','software-development':'rose',
  'productivity':'tulip','autonomous-ai-agents':'daisy','media':'peony',
  'email':'tulip','note-taking':'daisy','plugin':'rose','web':'daisy',
  '(uncategorized)':'peony',
}

def petal(cx, cy, rx, ry, angle, fill, uid, opacity=1, vein=True):
    # organic rounded petal from center to tip
    d = (f'M {cx} {cy} '
         f'C {cx-rx*.42} {cy-ry*.22} {cx-rx*.58} {cy-ry*.70} {cx-rx*.20} {cy-ry*.96} '
         f'C {cx+rx*.02} {cy-ry*1.12} {cx+rx*.46} {cy-ry*.82} {cx+rx*.50} {cy-ry*.42} '
         f'C {cx+rx*.52} {cy-ry*.18} {cx+rx*.28} {cy-ry*.04} {cx} {cy} Z')
    v = f'<path d="M{cx} {cy} Q{cx-rx*.05} {cy-ry*.55} {cx-rx*.04} {cy-ry*.80}" fill="none" stroke="#6f5d5a" stroke-width=".7" opacity=".35"/>' if vein else ''
    return f'<g transform="rotate({angle:.1f} {cx} {cy})" opacity="{opacity}"><path d="{d}" fill="url(#{uid})" stroke="#6f5d5a" stroke-width="1.1" stroke-linejoin="round"/>{v}</g>'

def flower_svg(x, bed, idx):
    outer, mid, inner = PALETTES.get(x.get('nativeBed') or bed, DEFAULT)
    uid = f'g{idx}'
    cx, cy = 80, 86
    scale = .82 + min(1.0, float(x.get('size', .6) or .6)) * .22
    rot = (idx % 7 - 3) * 3
    stem_h = 150 + int(scale * 34)
    # layer rotations/counts create species variation without leaving the peony vibe
    n = 9 + (idx % 3)
    outer_petals = ''.join(petal(cx, cy, 34, 58, rot + i*360/n, outer, uid+'-o', .96) for i in range(n))
    mid_petals = ''.join(petal(cx, cy, 26, 42, rot + 18 + i*360/(n-1), mid, uid+'-m', .98) for i in range(n-1))
    inner_petals = ''.join(petal(cx, cy, 18, 29, rot + 9 + i*360/6, inner, uid+'-i', 1) for i in range(6))
    stamens = ''
    for i in range(12):
        a = math.radians(i*30 + rot)
        x2 = cx + math.cos(a)*13
        y2 = cy + math.sin(a)*10
        stamens += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#f2cf72" stroke-width="1.1"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="1.8" fill="#ffd979" stroke="#6f5d5a" stroke-width=".5"/>'
    spark = ''
    for i,(sx,sy,s) in enumerate([(28,38,5),(130,32,4),(112,118,3),(42,104,3)]):
        if (idx+i)%2==0:
            spark += f'<path d="M{sx} {sy-s} L{sx+s*.3} {sy-s*.3} L{sx+s} {sy} L{sx+s*.3} {sy+s*.3} L{sx} {sy+s} L{sx-s*.3} {sy+s*.3} L{sx-s} {sy} L{sx-s*.3} {sy-s*.3} Z" fill="#fff" opacity=".8"/>'
    return f'''<svg viewBox="0 0 160 260" class="bot" aria-hidden="true">
<defs>
 <linearGradient id="{uid}-o" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{outer}"/><stop offset="1" stop-color="#e7dcf7"/></linearGradient>
 <linearGradient id="{uid}-m" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{mid}"/><stop offset="1" stop-color="#ffd8cf"/></linearGradient>
 <linearGradient id="{uid}-i" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{inner}"/><stop offset="1" stop-color="#fff0dc"/></linearGradient>
 <linearGradient id="{uid}-s" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#86a96a"/><stop offset="1" stop-color="#4d7744"/></linearGradient>
</defs>
<g transform="translate({80-cx} {242-stem_h-cy+40}) scale({scale:.3f})">
 <path d="M80 250 C74 210 86 165 80 {cy+36}" fill="none" stroke="url(#{uid}-s)" stroke-width="5" stroke-linecap="round"/>
 <path d="M80 205 C57 192 49 174 47 157 C69 160 80 177 80 194Z" fill="#8fb477" stroke="#5d7f55" stroke-width="1"/>
 <path d="M80 182 C102 167 111 150 112 135 C91 140 80 156 80 172Z" fill="#a0c187" stroke="#5d7f55" stroke-width="1"/>
 {outer_petals}{mid_petals}{inner_petals}
 <circle cx="{cx}" cy="{cy}" r="8" fill="#ffd786" stroke="#6f5d5a" stroke-width="1"/>
 {stamens}{spark}
</g></svg>'''

def flower_svg_varied(x, bed, idx):
    outer, mid, inner = PALETTES.get(x.get('nativeBed') or bed, DEFAULT)
    species = x.get('species') or SPECIES.get(bed, ['peony','rose','daisy','tulip'][idx % 4])
    uid = f'f{idx}'; cx, cy = 80, 64
    norm = max(.10, min(1.0, float(x.get('size', .5) or .5)))
    H = 150 + int(norm * 120)
    px_h = int(H * .72)
    rot = (idx % 7 - 3) * 3
    if species == 'daisy':
        bloom = ''
        n = 14 + (idx % 3)
        for i in range(n):
            a = rot + i*360/n
            bloom += f'<g transform="rotate({a:.1f} {cx} {cy})"><ellipse cx="{cx}" cy="{cy-34}" rx="8" ry="27" fill="url(#{uid}-o)" stroke="#6f5d5a" stroke-width="1"/><path d="M{cx} {cy-10} Q{cx} {cy-27} {cx} {cy-47}" fill="none" stroke="#6f5d5a" stroke-width=".6" opacity=".3"/></g>'
        bloom += f'<circle cx="{cx}" cy="{cy}" r="16" fill="url(#{uid}-i)" stroke="#6f5d5a" stroke-width="1.2"/>'
        for i in range(9):
            a = math.radians(i*40)
            bloom += f'<circle cx="{cx+math.cos(a)*9:.1f}" cy="{cy+math.sin(a)*8:.1f}" r="1.6" fill="#8a6334" opacity=".7"/>'
    elif species == 'tulip':
        bloom = ''
        for i, a in enumerate([-30, 0, 30]):
            d = f'M{cx} {cy+26} C{cx-34+a} {cy-8} {cx-24+a} {cy-48} {cx+a*.3:.1f} {cy-56} C{cx+24+a} {cy-48} {cx+34+a} {cy-8} {cx} {cy+26}Z'
            bloom += f'<path d="{d}" fill="url(#{uid}-{["o","m","i"][i]})" stroke="#6f5d5a" stroke-width="1.1"/>'
        bloom += f'<path d="M{cx} {cy+26} C{cx-18} {cy+8} {cx+18} {cy+8} {cx} {cy+26}Z" fill="url(#{uid}-m)" stroke="#6f5d5a" stroke-width="1"/>'
    elif species == 'rose':
        bloom = ''
        for li, (rx, ry, n, off) in enumerate([(34,54,10,0),(27,43,8,18),(20,32,7,8),(13,21,5,20)]):
            for i in range(n):
                a = rot + off + i*360/n
                d = f'M{cx} {cy} C{cx-rx} {cy-ry*.25} {cx-rx*.72} {cy-ry} {cx} {cy-ry} C{cx+rx*.72} {cy-ry} {cx+rx} {cy-ry*.25} {cx} {cy}Z'
                bloom += f'<g transform="rotate({a:.1f} {cx} {cy})"><path d="{d}" fill="url(#{uid}-{["o","m","m","i"][li]})" stroke="#6f5d5a" stroke-width="1" opacity="{.96-li*.04:.2f}"/></g>'
        bloom += f'<path d="M{cx-7} {cy+3} C{cx-10} {cy-9} {cx+7} {cy-12} {cx+8} {cy-2} C{cx+8} {cy+7} {cx-5} {cy+7} {cx-3} {cy+1}" fill="none" stroke="#6f5d5a" stroke-width="1.2"/>'
    else:
        n = 9 + (idx % 3)
        bloom = ''.join(petal(cx, cy, 34, 58, rot+i*360/n, outer, uid+'-o', .96) for i in range(n))
        bloom += ''.join(petal(cx, cy, 26, 42, rot+18+i*360/(n-1), mid, uid+'-m', .98) for i in range(n-1))
        bloom += ''.join(petal(cx, cy, 18, 29, rot+9+i*60, inner, uid+'-i', 1) for i in range(6))
        for i in range(12):
            a = math.radians(i*30+rot)
            x2, y2 = cx+math.cos(a)*13, cy+math.sin(a)*10
            bloom += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#f2cf72" stroke-width="1.1"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="1.8" fill="#ffd979" stroke="#6f5d5a" stroke-width=".5"/>'
    spark = ''
    if species != 'tulip':
        for i, (sx, sy, s) in enumerate([(28,34,5),(130,30,4),(112,104,3),(42,96,3)]):
            if (idx+i) % 2 == 0:
                spark += f'<path d="M{sx} {sy-s} L{sx+s*.3} {sy-s*.3} L{sx+s} {sy} L{sx+s*.3} {sy+s*.3} L{sx} {sy+s} L{sx-s*.3} {sy+s*.3} L{sx-s} {sy} L{sx-s*.3} {sy-s*.3}Z" fill="#fff" opacity=".8"/>'
    y1 = 94 + (H-94) * .38
    y2 = 94 + (H-94) * .62
    return f'''<svg viewBox="0 0 160 {H}" class="bot" style="height:{px_h}px" aria-hidden="true">
<defs>
 <linearGradient id="{uid}-o" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{outer}"/><stop offset="1" stop-color="#e7dcf7"/></linearGradient>
 <linearGradient id="{uid}-m" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{mid}"/><stop offset="1" stop-color="#ffd8cf"/></linearGradient>
 <linearGradient id="{uid}-i" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{inner}"/><stop offset="1" stop-color="#fff0dc"/></linearGradient>
 <linearGradient id="{uid}-s" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#86a96a"/><stop offset="1" stop-color="#4d7744"/></linearGradient>
</defs>
 <path d="M80 {H-8} C74 {94+(H-94)*.55} 86 {94+(H-94)*.25} 80 {cy+30}" fill="none" stroke="url(#{uid}-s)" stroke-width="5" stroke-linecap="round"/>
 <path d="M80 {y1:.0f} C57 {y1-14:.0f} 49 {y1-32:.0f} 47 {y1-49:.0f} C69 {y1-46:.0f} 80 {y1-29:.0f} 80 {y1-12:.0f}Z" fill="#8fb477" stroke="#5d7f55" stroke-width="1"/>
 <path d="M80 {y2:.0f} C102 {y2-15:.0f} 111 {y2-32:.0f} 112 {y2-47:.0f} C91 {y2-42:.0f} 80 {y2-26:.0f} 80 {y2-10:.0f}Z" fill="#a0c187" stroke="#5d7f55" stroke-width="1"/>
 <g transform="translate({cx} {cy}) scale(.85) translate(-{cx} -{cy})">{bloom}{spark}</g>
</svg>'''

def build(m):
    beds = {}
    for x in m['items']:
        beds.setdefault(x.get('bed') or x.get('category') or 'uncategorized', []).append(x)
    sections=[]; idx=0
    for bed, items in sorted(beds.items(), key=lambda kv: -len(kv[1])):
        sp = SPECIES.get(bed, 'peony')
        plants=[]
        for x in items:
            n = max(.10, min(1.0, float(x.get('size', .5) or .5)))
            ph = int((150 + int(n*120)) * .72) + 24
            plants.append(f'''<button class="plant" data-title="{e(x.get('title'))}" style="height:{ph}px">
{flower_svg_varied(x,bed,idx)}<span class="label">{e(x.get('title'))}</span></button>''')
            idx += 1
        sections.append(f'''<section class="bed"><div class="bed-label"><h2>{e(bed)}</h2><span>{len(items)} skill{'s' if len(items)!=1 else ''} &middot; { {'peony':'peonies','daisy':'daisies','rose':'roses','tulip':'tulips'}[sp] }</span></div><div class="row">{''.join(plants)}</div><div class="soil"></div></section>''')
    data=json.dumps({'items':m['items'],'relationships':m.get('relationships',[])},ensure_ascii=False).replace('</','<\\/')
    return HTML.replace('%%SECTIONS%%',''.join(sections)).replace('%%DATA%%',data).replace('%%TITLE%%',e(m.get('title','Skill garden'))).replace('%%SUB%%',e(m.get('subtitle','')))

HTML=r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%%TITLE%%</title><style>
:root{--bg:#0a1116;--ink:#f4eadb;--muted:#9ba79b;--soil:#3a271c;--soil2:#5a3b27}*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--ink)}body{font-family:Georgia,'Times New Roman',serif;overflow-x:hidden}.sky{min-height:100vh;background:radial-gradient(circle at 85% 4%,#344b59 0,#13252d 13%,transparent 35%),radial-gradient(circle at 6% 3%,#263b31,transparent 28%),linear-gradient(#0b1620 0 16%,#09110e 45%,#0b0e0a)}header{max-width:1500px;margin:auto;padding:17px 5vw 4px;position:relative}.eyebrow{font:10px ui-monospace,monospace;letter-spacing:.18em;color:#e9c57a;text-transform:uppercase}.title{font-size:clamp(34px,5vw,58px);font-weight:400;letter-spacing:-.06em;line-height:.86;margin:13px 0 6px}.sub{font:12px ui-monospace,monospace;color:var(--muted)}.moon{position:absolute;right:6vw;top:20px;width:62px;height:62px;border-radius:50%;background:#f3e2bd;box-shadow:0 0 45px #f0d9a055}.beds{max-width:1500px;margin:0 auto;padding:0 5vw 80px}.bed{position:relative;padding-top:10px}.bed+.bed{margin-top:7px}.bed-label{display:flex;align-items:baseline;gap:12px;margin-bottom:6px}.bed-label h2{font-size:17px;font-weight:400;letter-spacing:-.02em;margin:0}.bed-label span{font:10px ui-monospace,monospace;color:var(--muted);letter-spacing:.08em}.row{display:grid;grid-auto-flow:column;grid-template-rows:repeat(2,auto);gap:8px;align-items:end;overflow-x:auto;overflow-y:hidden;padding:0 0 2px;scrollbar-width:thin;scrollbar-color:#3d4b3b transparent}.plant{flex:0 0 auto;width:108px;height:165px;background:none;border:0;padding:0;color:var(--ink);cursor:pointer;position:relative;transform:scale(var(--s));transform-origin:bottom center}.plant:hover{filter:drop-shadow(0 0 12px #f3d4b088)}.bot{display:block;width:108px;height:128px}.label{display:block;font:9px ui-monospace,monospace;line-height:1.15;color:#e7dfd0;margin-top:-4px;white-space:nowrap;text-align:center;overflow:hidden;text-overflow:ellipsis}.soil{height:16px;margin-top:-3px;background:linear-gradient(var(--soil),#1b120d);border-top:2px solid var(--soil2);box-shadow:inset 0 5px 8px #0006}.soil:after{content:"";display:block;height:6px;background:repeating-linear-gradient(93deg,transparent 0 19px,#6d4930 20px 22px,transparent 23px 38px);opacity:.55}.overlay{display:none;position:fixed;inset:0;background:#030708cc;backdrop-filter:blur(9px);z-index:10;align-items:stretch;justify-content:flex-end}.overlay.show{display:flex}.modal{width:min(460px,100%);height:100%;overflow:auto;background:linear-gradient(180deg,#1a2b20,#111a15 46%,#0d130f);border-left:1px solid #6b8662;box-shadow:-20px 0 80px #000c;animation:slidein .32s cubic-bezier(.2,.8,.2,1)}@keyframes slidein{from{transform:translateX(40px);opacity:.4}to{transform:none;opacity:1}}.modal-hero{height:230px;position:relative;display:flex;align-items:flex-end;justify-content:center;background:radial-gradient(circle at 50% 30%,#3b5140,#16241b 68%);border-bottom:1px solid #415540;overflow:hidden}.modal-hero .bot{width:180px!important;height:215px!important}.modal-body{padding:24px 26px 40px}.close{position:absolute;right:15px;top:15px;background:#101b14;border:1px solid #506550;color:var(--ink);width:34px;height:34px;cursor:pointer;z-index:2}.modal h2{font-size:42px;font-weight:400;letter-spacing:-.05em;line-height:.95;margin:8px 0 6px}.modal p{color:var(--muted);font-size:15px;line-height:1.6;margin:16px 0}.tag{font:10px ui-monospace,monospace;color:#e9c57a;text-transform:uppercase;letter-spacing:.14em}.stats{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid #3e563f;margin-top:22px}.stat{padding:13px 11px;border-right:1px solid #3e563f}.stat:last-child{border-right:0}.stat b{display:block;font:21px Georgia,serif;color:var(--ink)}.stat span{font:9px ui-monospace,monospace;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}.relations{margin-top:22px;border-top:1px solid #3e563f;padding-top:15px}.relations .tag{color:#a9c187}.rel{padding:8px 0;border-bottom:1px solid #2b3b2c;font:12px ui-monospace,monospace;color:#dbe5d2}.rel:before{content:'↳ ';color:#e9c57a}.read{margin-top:22px;border:1px solid #e9c57a;background:transparent;color:#e9c57a;padding:10px 14px;font:11px ui-monospace,monospace;cursor:pointer}.read:hover{background:#e9c57a;color:#132018}.full{display:none;white-space:pre-wrap;word-break:break-word;margin-top:14px;padding:14px;background:#0c130e;border:1px solid #30422f;color:#cbd7c5;font:11px/1.55 ui-monospace,SFMono-Regular,monospace;max-height:50vh;overflow:auto}.full.show{display:block}@media(max-width:650px){header{padding:20px 18px 4px}.moon{width:44px;height:44px;right:18px}.beds{padding:0 18px 60px}.plant{width:106px}.bot{width:106px;height:220px}.label{font-size:9px}}
</style></head><body><main class="sky"><header><div class="eyebrow">BOTANICAL INDEX</div><h1 class="title" id="title">%%TITLE%%</h1><div class="sub" id="sub">%%SUB%%</div><div class="moon"></div></header><section class="beds" id="beds">%%SECTIONS%%</section></main><div class="overlay" id="overlay"><article class="modal" id="modal"></article></div><script type="application/json" id="data">%%DATA%%</script><script>(()=>{const D=JSON.parse(data.textContent),esc=s=>{let d=document.createElement('div');d.textContent=s??'';return d.innerHTML};document.querySelectorAll('.plant').forEach(b=>b.onclick=()=>{let x=D.items.find(i=>i.title===b.dataset.title),flower=b.querySelector('.bot').outerHTML,links=(x.relationships||[]).map(l=>esc(typeof l==='string'?l:(l.to||l.title))),extra=(D.relationships||[]).filter(l=>l.to===x.title).map(l=>esc(l.from));let rel=[...links,...extra];modal.innerHTML=`<button class="close">×</button><div class="modal-hero">${flower}</div><div class="modal-body"><div class="tag">${esc(x.bed||x.category||'skill')} / ${esc(x.stage||'bloom')}</div><h2>${esc(x.title)}</h2><p>${esc(x.summary||x.subtitle||'')}</p><div class="stats"><div class="stat"><b>${esc(x.lines||'—')}</b><span>SKILL.md lines</span></div><div class="stat"><b>${esc(x.family||'—')}</b><span>family</span></div><div class="stat"><b>${esc(x.bed||'—')}</b><span>bed</span></div></div>${rel.length?`<div class="relations"><div class="tag">GROWS WITH</div>${rel.map(r=>`<div class="rel">${r}</div>`).join('')}</div>`:''}</div><button class="read">Read full skill ↗</button><pre class="full">${esc(x.full||'Full source not available in this export.')}</pre></div>`;overlay.classList.add('show');modal.querySelector('.close').onclick=()=>overlay.classList.remove('show');const rb=modal.querySelector('.read');rb.onclick=()=>{const f=modal.querySelector('.full');f.classList.toggle('show');rb.textContent=f.classList.contains('show')?'Hide skill':'Read full skill ↗'}});overlay.onclick=e=>e.target===overlay&&overlay.classList.remove('show')})();</script></body></html>'''

def main():
    p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('-o','--out',required=True);a=p.parse_args()
    m=json.loads(Path(a.manifest).read_text(encoding='utf8'));Path(a.out).write_text(build(m),encoding='utf8');print(f'wrote {a.out} ({len(m["items"])} flowers)')
if __name__=='__main__':main()
