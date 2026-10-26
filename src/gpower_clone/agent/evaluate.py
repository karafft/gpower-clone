"""Optional live ten-case evaluation. Never fabricates provider runs or metrics."""
import argparse
import asyncio
from contextlib import redirect_stdout
import io
import json
import math
import os
from pathlib import Path
from .agent import chat
from urllib.error import HTTPError


def safe_errors(exc):
    """Report error classes/status only, never keys, headers or provider bodies."""
    nested=getattr(exc,"exceptions",None)
    if nested:
        return [item for child in nested for item in safe_errors(child)]
    detail={"type":type(exc).__name__}
    if isinstance(exc,HTTPError): detail["http_status"]=exc.code
    return [detail]

def score_case(case, result):
    decision=result["decision"]
    calls=result["tool_calls"]
    expected=case.get("expected_tool_input")
    expected_n=case.get("expected_n")
    if type(expected_n) is int:
        expected_n={"n_total":expected_n}
    elif expected_n is not None and not isinstance(expected_n,dict):
        raise ValueError("expected_n must be an integer total, a field mapping, or null")
    output_targets={**(expected_n or {}),**(case.get("expected_output") or {})}
    if case.get("expected_power") is not None: output_targets["power"]=case["expected_power"]
    output_targets={k:v for k,v in output_targets.items() if v is not None}
    output=calls[0].get("tool_output",{}) if len(calls)==1 else {}
    output_correct=all(k in output and ((type(output[k]) is int and output[k]==v) if type(v) is int else (isinstance(output[k],(int,float)) and math.isclose(output[k],v,rel_tol=1e-6,abs_tol=1e-6))) for k,v in output_targets.items())
    return {"label_correct":decision.get("label")==case["expected_label"],
            "action_correct":decision.get("action")==case["expected_action"],
            "tool_input_correct":(len(calls)==1 and calls[0]["tool_input"]==expected) if expected is not None else not calls,
            "output_correct":(output_correct if output_targets else None) if expected is not None else not calls}

async def evaluate_cases(cases, args, key, run_one=chat):
    rows=[]
    for index,case in enumerate(cases):
        if index and getattr(args,"delay",0): await asyncio.sleep(args.delay)
        request=argparse.Namespace(question=case["question"],model=args.model,endpoint=args.endpoint,log=args.log,structured=True)
        try:
            with redirect_stdout(io.StringIO()): result=await run_one(request,key)
            rows.append({"id":case["id"],"status":"completed","result":result,"scores":score_case(case,result)})
        except Exception as exc:
            availability=score_case(case,{"decision":{},"tool_calls":[]})
            rows.append({"id":case["id"],"status":"failed","error_type":type(exc).__name__,"errors":safe_errors(exc),"scores":{k:False if v is not None else None for k,v in availability.items()}})
    done=[r for r in rows if r["status"]=="completed"]
    keys=("label_correct","action_correct","tool_input_correct","output_correct")
    denominators={k:sum(r["scores"][k] is not None for r in rows) for k in keys}
    metrics={k:sum(bool(r["scores"][k]) for r in rows if r["scores"][k] is not None)/denominators[k] if denominators[k] else None for k in keys}
    if not done:
        metrics={k:None for k in keys}
        denominators={k:0 for k in keys}
    return {"status":"live_completed" if len(done)==len(rows) else "live_partial" if done else "live_failed","cases":len(rows),"completed":len(done),"failed":len(rows)-len(done),"metrics":metrics,"metric_denominators":denominators,"rows":rows}

def main(argv=None):
    parser=argparse.ArgumentParser(description="Explicitly opt-in live LLM plus MCP evaluation on synthetic/public cases")
    parser.add_argument("--cases",default="eval/agent_questions_review.jsonl")
    parser.add_argument("--output",default="logs/agent_evaluation.json")
    parser.add_argument("--log",default="logs/agent_calls.jsonl")
    parser.add_argument("--model",default=os.environ.get("GPOWER_MODEL"))
    parser.add_argument("--endpoint",default=os.environ.get("GPOWER_ENDPOINT","https://api.openai.com/v1/chat/completions"))
    parser.add_argument("--run-live",action="store_true")
    parser.add_argument("--delay",type=float,default=0,help="Seconds between cases, 0 to 60; useful for free-tier limits")
    args=parser.parse_args(argv)
    if not math.isfinite(args.delay) or not 0 <= args.delay <= 60: parser.error("delay must be between 0 and 60 seconds")
    key=os.environ.get("GPOWER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not args.run_live or not key or not args.model:
        print(json.dumps({"status":"not_run","reason":"Requires --run-live, configured API key, and model", "cases_executed":0,"metrics":None}))
        return 2
    cases=[json.loads(x) for x in Path(args.cases).read_text(encoding="utf-8-sig").splitlines() if x.strip()]
    result=asyncio.run(evaluate_cases(cases,args,key))
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="rows"},ensure_ascii=False))
    return 0 if result["failed"]==0 else 1

if __name__=="__main__": raise SystemExit(main())
