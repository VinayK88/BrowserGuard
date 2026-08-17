from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from .fixtures import EXTENSIONS
from .engine import assess, blast_radius
from .report import build_report
app=FastAPI(title='BrowserGuard',version='0.1.0')
@app.get('/healthz')
def healthz(): return {'status':'ok','service':'browserguard'}
@app.get('/report')
def report(): return build_report()
@app.get('/extensions')
def extensions(): return [assess(e).to_dict() for e in EXTENSIONS]
@app.get('/extensions/{ext_id}')
def extension(ext_id:str):
    e=next((x for x in EXTENSIONS if x.ext_id==ext_id),None)
    if not e: raise HTTPException(404,'extension not found')
    return {'assessment':assess(e).to_dict(),'blast_radius':blast_radius(e)}
@app.get('/',response_class=HTMLResponse)
def home():
    r=build_report(); s=r['summary']
    cards=''.join(f"<div class='card'><b>{x['name']}</b><br>{x['decision']} · {x['risk_score']}/100<br><small>{', '.join(x['reasons'][:2]) or 'low-risk baseline'}</small></div>" for x in r['assessments'])
    return f'''<html><head><title>BrowserGuard</title><style>body{{font-family:Arial;background:#0b1020;color:#e5e7eb;max-width:1100px;margin:auto;padding:32px}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}.card{{background:#131b2e;padding:18px;border:1px solid #26334d;border-radius:12px}}h1{{color:#7dd3fc}}small{{color:#a5b4fc}}</style></head><body><h1>BrowserGuard</h1><p>Browser & Extension Detection/Response</p><div class='grid'><div class='card'><b>{s['extensions']}</b><br>Extensions</div><div class='card'><b>{s['counts'].get('CRITICAL',0)}</b><br>Critical</div><div class='card'><b>{s['counts'].get('HIGH_RISK',0)}</b><br>High risk</div><div class='card'><b>{s['users_behind_high_or_critical']}</b><br>Users exposed</div>{cards}</div></body></html>'''
