import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from browserguard.report import build_report

expected=json.loads((ROOT/'reports/baseline.json').read_text())
actual=build_report()
if actual!=expected:
    raise SystemExit('reports/baseline.json is stale; regenerate it from browserguard.report.build_report()')
print('baseline report matches executable hybrid ML output')
