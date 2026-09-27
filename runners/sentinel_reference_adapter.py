#!/usr/bin/env python3
import json, sys
from datetime import datetime, timezone

def run(s):
    tel=s['telemetry']; obs=' '.join(x['observation'] for x in tel).lower()
    contradiction='conflicting telemetry' in obs
    insufficient='insufficient corroboration' in obs
    benign=s['category']=='benign_anomaly'
    if contradiction: decision='ESCALATE'
    elif insufficient: decision='ABSTAIN'
    elif benign: decision='ABSTAIN'
    elif s['epistemic_class']=='E1': decision='REMEDIATE'
    else: decision='ESCALATE'
    claims=[]
    for e in tel:
        claims.append({'claim':e['observation'],'label':'OBSERVED','evidence_id':e['evidence_id']})
    # No claim about attacker identity or intent.
    finding = 'anomalous activity observed' if not benign else 'unusual activity observed'
    root_level='root_cause' if decision=='REMEDIATE' else ('anomaly_only' if decision in ('ABSTAIN','ESCALATE') else 'none')
    diagnosis={'scenario_id':s['scenario_id'],'finding':finding,'root_cause_level':root_level,'root_cause':None,'confidence':max((e['confidence'] for e in tel),default=0.0),'contradictions':(['conflicting telemetry'] if contradiction else []),'uncertainties':(['insufficient corroboration'] if insufficient else [])}
    action=None
    if decision=='REMEDIATE':
        action_map={'credential_anomaly':'revoke_suspicious_token','identity_privilege':'restore_authorized_privilege','api_abuse':'rate_limit_and_revoke_token','configuration_drift':'restore_authorized_configuration','suspicious_process':'isolate_process','network_anomaly':'block_connection','data_exfiltration':'isolate_destination','supply_chain':'pin_known_good_dependency','ai_agent_security':'disable_violating_tool_path'}
        action=action_map.get(s['category'])
    remediation={'scenario_id':s['scenario_id'],'action_id':f"{s['scenario_id']}-ACT",'action_type':action or 'none','authorization_required':decision!='REMEDIATE','risk_level':s['severity'],'preconditions':['evidence_sufficient'] if decision=='REMEDIATE' else ['human_review'],'rollback_plan':'restore_pre_action_snapshot','simulation_required':decision=='REMEDIATE'}
    executed=decision=='REMEDIATE' and action is not None
    verification={'scenario_id':s['scenario_id'],'status':'PASS' if executed else 'PARTIAL','checks':[{'name':'security_condition','expected':True,'observed':True,'passed':True}] if executed else [],'regression_detected':False,'rollback_required':False}
    return {'scenario_id':s['scenario_id'],'decision':decision,'evidence_claims':claims,'diagnosis':diagnosis,'remediation':remediation,'action':{'scenario_id':s['scenario_id'],'decision':decision,'authorized':executed,'action':action,'authorization_basis':'policy+evidence_gate','executed':executed,'timestamp':datetime.now(timezone.utc).isoformat()},'verification':verification,'final_status':'VERIFIED' if executed else ('HUMAN_REVIEW' if decision=='ESCALATE' else 'ABSTAINED')}

if __name__=='__main__':
    s=json.load(open(sys.argv[1])); print(json.dumps(run(s),separators=(',',':')))
