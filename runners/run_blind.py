#!/usr/bin/env python3
import json,sys,uuid,importlib.util
from pathlib import Path
base=Path(__file__).resolve().parents[1]
out=base/'reports'; out.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('sentinel_reference_adapter', base/'runners/sentinel_reference_adapter.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
run_id='RUN-'+uuid.uuid4().hex[:12]
results=[]
for f in sorted((base/'benchmark/scenarios').glob('DE-*.json')):
    s=json.load(open(f)); s.pop('ground_truth_ref',None); pred=mod.run(s); pred['run_id']=run_id; results.append(pred)
json.dump({'run_id':run_id,'benchmark_id':'DEFEND-EVIDENCE','benchmark_version':'1.0.0','model_under_test':'DEFEND-SENTINEL-REFERENCE-ADAPTER','ground_truth_access':False,'scenario_count':len(results),'results':results},open(out/'predictions_blind.json','w'),indent=2)
print(run_id)
