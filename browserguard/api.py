from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from .fixtures import EXTENSIONS
from .engine import assess, blast_radius
from .report import build_report

app=FastAPI(title='BrowserGuard',version='0.2.0')

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
    cards=''.join(
        f"<div class='card ext'><b>{x['name']}</b><span class='pill'>{x['decision']}</span>"
        f"<div class='score'>{x['risk_score']}/100</div>"
        f"<small>Rules {x['rule_score']} · ML {x['ml_anomaly_score']:.1f}p"
        f"{' · outlier' if x['ml_outlier'] else ''}</small>"
        f"<p>{', '.join(x['reasons'][:2]) or 'low-risk baseline'}</p></div>"
        for x in r['assessments']
    )
    return f'''<html><head><title>BrowserGuard</title><style>
body{{font-family:Arial;background:#0b1020;color:#e5e7eb;max-width:1200px;margin:auto;padding:32px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
.card{{background:#131b2e;padding:18px;border:1px solid #26334d;border-radius:12px}}
.ext{{min-height:145px}}h1{{color:#7dd3fc}}small{{color:#a5b4fc}}p{{color:#94a3b8;font-size:13px}}
.score{{font-size:24px;font-weight:700;margin:12px 0}}.pill{{float:right;font-size:11px;color:#bae6fd}}
@media(max-width:800px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body>
<h1>BrowserGuard</h1><p>Hybrid Browser & Extension Detection/Response · Rules + Isolation Forest + blast radius</p>
<div class='grid'>
<div class='card'><b>{s['extensions']}</b><br>Extensions</div>
<div class='card'><b>{s['counts'].get('CRITICAL',0)}</b><br>Critical</div>
<div class='card'><b>{s['ml_outliers']}</b><br>ML outliers</div>
<div class='card'><b>{s['users_behind_high_or_critical']}</b><br>Users exposed</div>
{cards}</div></body></html>'''
