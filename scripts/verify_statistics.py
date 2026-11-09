"""Recompute public paper statistics from minimal numeric data (stdlib only).

No task code, checker, scoring harness, command history, GPU, or network is used.
"""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path

PANELS=('P5','P6.2','P8','P12')

def read(path):return json.loads(path.read_bytes())

def verify_inputs(data_dir):
    provenance=read(data_dir/'provenance.json')
    for name,expected in provenance['export_files'].items():
        path=data_dir/name
        assert path.resolve().is_relative_to(data_dir.resolve()),'input path escapes data directory'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,'input hash mismatch: '+name
    return provenance

def discordant_p(wins,losses):
    n=wins+losses
    return min(1.,2*sum(math.comb(n,k)for k in range(min(wins,losses)+1))/2**n)if n else 1.

def paired(table,first,second):
    pairs=[(task,v[first],v[second])for task,v in table.items()if v[first]is not None and v[second]is not None]
    wins=[task for task,a,b in pairs if a==0 and b==1]
    losses=[task for task,a,b in pairs if a==1 and b==0]
    low=high=0
    for v in table.values():
        a=[v[first]]if v[first]is not None else [0,1]
        b=[v[second]]if v[second]is not None else [0,1]
        possibles=[y-x for x in a for y in b];low+=min(possibles);high+=max(possibles)
    return {'first':first,'second':second,'registered_pairs':len(table),'complete_pairs':len(pairs),
         'wins':wins,'losses':losses,'net_complete_pairs':len(wins)-len(losses),
         'registered_net_bounds':[low,high],'two_sided_exact_discordant_p_unadjusted':discordant_p(len(wins),len(losses))}

def p120_view(cells,decisions=None):
    decisions={x['cell_id']:x['adjudicated_outcome']for x in (decisions or [])}
    table={};counts={a:collections.Counter()for a in ('A','B','C')}
    for cell in cells:
        outcome=decisions.get(cell['cell_id'],cell['original_outcome'])
        table.setdefault(cell['task_id'],{})[cell['arm']]={'PASS':1,'FAIL':0,'UNKNOWN':None}[outcome]
        counts[cell['arm']][outcome]+=1
    assert all(set(v)=={'A','B','C'}for v in table.values()),'incomplete A/B/C triplet'
    return {'tasks':len(table),'cells':len(cells),'arms':{a:{x:counts[a][x]for x in ('PASS','FAIL','UNKNOWN')}for a in counts},
       'contrasts':{b+'-'+a:paired(table,a,b)for a,b in (('A','B'),('B','C'),('A','C'))}}

def compute(data_dir):
    provenance=verify_inputs(data_dir)
    historical=read(data_dir/'historical.json');episodes=historical['episodes'];events=historical['events'];units=historical['candidate_units']
    assert len(episodes)==180 and len(events)==716 and len(units)==314
    assert sum(e['original_event_count']for e in episodes)==2451
    assert all(e['source_changed']or e['test_executed']for e in events)
    assert len({e['task_id']for e in episodes})==21
    byepisode=collections.defaultdict(list)
    for event in events:byepisode[event['episode_id']].append(event)
    episode_ids={e['episode_id']for e in episodes};assert len(episode_ids)==180 and set(byepisode)<=episode_ids
    assert len({u['unit_id']for u in units})==314
    assert len({u['frozen_unit_identity_sha256']for u in units})==314
    table1={};table2={};table3={};figure2={};members=[]
    for panel in PANELS:
        rows=[e for e in episodes if e['panel']==panel]
        table1[panel]={a:{'historical_resolved':sum(e['historical_resolved']is True for e in rows if e['arm']==a),
                         'scheduled':sum(e['arm']==a for e in rows)}for a in sorted({e['arm']for e in rows})}
        changed=[];strict=[]
        for episode in rows:
            ev=byepisode[episode['episode_id']]
            positions=[x['position']for x in ev if x['source_changed']]
            after=bool(positions)and any(x['test_executed']and x['exit_code']==0 and x['position']>max(positions)for x in ev)
            if positions:changed.append(episode)
            if after:strict.append(episode)
            members.append({'episode_id':episode['episode_id'],'panel':panel,'task_id':episode['task_id'],
                'source_changed':bool(positions),'strict_post_last_change_zero':after,
                'resolved_inside_strict':after and episode['score_valid']and episode['final_resolved']is True,
                'score_valid':episode['score_valid'],'final_resolved':episode['final_resolved']})
        valid_changed=[e for e in changed if e['score_valid']];valid_strict=[e for e in strict if e['score_valid']]
        table2[panel]={'actual_new_source_change':len(changed),
           'independent_outcomes':{'PASS':sum(e['score_valid']and e['final_resolved']is True for e in rows),
              'FAIL':sum(e['score_valid']and e['final_resolved']is False for e in rows),'UNKNOWN':sum(not e['score_valid']for e in rows)},
           'FAIL_among_changed':[sum(e['final_resolved']is False for e in valid_changed),len(valid_changed)],
           'FAIL_after_last_change_zero_exit':[sum(e['final_resolved']is False for e in valid_strict),len(valid_strict)]}
        figure2[panel]={'episode_total':len(rows),'source_changed':len(changed),'strict_post_last_change_zero':len(strict),
           'resolved_inside_strict':sum(e['score_valid']and e['final_resolved']is True for e in strict),
           'strict_final_FAIL':sum(e['score_valid']and e['final_resolved']is False for e in strict),
           'strict_final_UNKNOWN':sum(not e['score_valid']for e in strict)}
        failed_units={};mappings=[]
        for unit in units:
            assert unit['source_preservation_qualified']is True
            selected=[m for m in unit['historical_mappings']if m['panel']==panel and m['historical_final_score_valid']and m['historical_final_resolved']is False]
            if selected:failed_units[unit['unit_id']]=unit;mappings.extend((unit,m)for m in selected)
        zero=[u for u in failed_units.values()if u['exits']['candidate']==0]
        allzero=[u for u in zero if all(u['exits'][x]==0 for x in ('original','candidate','reference'))]
        last=[(u,m)for u,m in mappings if m['historical_timing']=='AFTER_LAST_SOURCE_CHANGE']
        table3[panel]={'candidate_zero_units':[len(zero),len(failed_units)],
           'all_three_zero_among_candidate_zero':[len(allzero),len(zero)],
           'covered_historically_failed_episodes':len({m['episode_id']for u,m in mappings}),
           'post_last_change_candidate_zero_events':[sum(u['exits']['candidate']==0 for u,m in last),len(last)],
           'full_subset_candidate_zero_events':[sum(u['exits']['candidate']==0 for u,m in mappings),len(mappings)]}
    loss=historical['loss_units'];n=sum(x['n_loss']for x in loss)
    baseline=sum(x['base_nll_total']for x in loss)/n;lora=sum(x['lora_nll_total']for x in loss)/n
    local_metrics={'P5_NLL':{'units':len(loss),'target_tokens':n,'BASE':baseline,'LORA':lora,'relative_reduction':1-lora/baseline},
         'P6_exploration':historical['feedback_exploration'],'P8_generated_check_execution':historical['generated_check_gate'],
         'P12_input_reduction':{a:1-v['input_tokens']/historical['native_history_tokens']['BASE']['input_tokens']for a,v in historical['native_history_tokens'].items()if a!='BASE'}}
    cells=read(data_dir/'p120.json')['cells'];adjudication=read(data_dir/'p120_adjudication.json')
    assert len(cells)==72 and len({x['task_id']for x in cells})==24 and len({x['repository_id']for x in cells})==24
    original=p120_view(cells);new=p120_view(cells,adjudication['decisions'])
    strata={name:{'original':p120_view([x for x in cells if x['exposure_stratum']==name]),
             'adjudicated':p120_view([x for x in cells if x['exposure_stratum']==name],adjudication['decisions'])}
             for name in sorted({x['exposure_stratum']for x in cells})}
    result={'status':'PASS','scope':'Offline numerical recomputation, not new agent experiments or task scoring.',
         'table1':{'historical_interventions':table1,'local_metrics':local_metrics,'P120_original':original['arms']},
         'table2':table2,'table3':table3,'figure2':figure2,'figure2_episode_subsets':members,
         'p120':{'original':original,'posthoc_source_adjudicated':new,'exposure_strata':strata,
             'original_strict_valid_scores':adjudication['original_strict_valid_scores'],
             'source_attributed_FAIL_decisions':adjudication['additional_source_attributed_FAIL_decisions'],
             'new_strict_valid_score_receipts':adjudication['new_strict_valid_score_receipts']},
         'qualified_triples':len(units),'canonical_state_executions':len(units)*3,
         'historical_original_tool_events':sum(e['original_event_count']for e in episodes),
         'published_numeric_source_or_check_events':len(events),
         'historical_check_mappings':sum(len(u['historical_mappings'])for u in units),
         'covered_episodes':len({m['episode_id']for u in units for m in u['historical_mappings']}),
         'public_export_file_hashes_checked':len(provenance['export_files']),
         'new_agent_experiments':0,'GPU_calls':0,'scoring_calls':0}
    abjad=data_dir/'abjad_results.json'
    if abjad.exists():
        case=read(abjad)
        result['abjad_figure3']={k:case[k]for k in ('original_agent_results','cpu_ablations','timeline')}
        for row in case['original_agent_results']+case['cpu_ablations']:
            assert row['score_valid']is True and row['errors']==0
            assert (row['failed']==0)is row['resolved']
    else:result['abjad_figure3']=None
    supplement=data_dir/'supplementary_counts.json'
    if supplement.exists():
        extra=read(supplement);panels=extra['state_alignment']['panels']
        assert {x['panel']for x in panels}==set(PANELS)
        assert all(x['last_check_version_mismatch'][1]==x['episodes_with_checks']for x in panels)
        totals={'check_events':sum(x['check_events']for x in panels),
          'check_source_differs_from_archived_final':sum(x['check_source_differs_from_archived_final']for x in panels),
          'last_check_version_mismatch':[sum(x['last_check_version_mismatch'][i]for x in panels)for i in (0,1)]}
        result['supplementary']={'state_alignment':{'panels':panels,'recomputed_totals':totals,
          'workspace_identity_is_conditional':extra['state_alignment']['workspace_identity_is_conditional']},
          'retained_aggregate_summaries':extra['retained_aggregate_summaries'],
          'recomputation_boundary':extra['recomputation_boundary']}
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parents[1]/'data')
    parser.add_argument('--output',type=Path,help='Optional output JSON; inputs are never modified.')
    args=parser.parse_args();result=compute(args.data_dir.resolve())
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        assert not args.output.resolve().is_relative_to(args.data_dir.resolve()),'output must not overwrite public inputs'
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
