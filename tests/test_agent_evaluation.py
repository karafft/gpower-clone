import argparse
import asyncio
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from gpower_clone.agent.evaluate import evaluate_cases, main, score_case

class AgentEvaluationTests(unittest.TestCase):
    def test_scalar_expected_total(self):
        case={"expected_label":"t2-indep","expected_action":"call_tool","expected_tool_input":{"test":"t2-indep"},"expected_n":128,"expected_power":None}
        result={"decision":{"label":"t2-indep","action":"call_tool"},"tool_calls":[{"tool_input":{"test":"t2-indep"},"tool_output":{"n_total":128}}]}
        self.assertTrue(score_case(case,result)["output_correct"])
        result["tool_calls"][0]["tool_output"]["n_total"]=128.0
        self.assertFalse(score_case(case,result)["output_correct"])
    def test_missing_config_produces_no_metrics(self):
        with patch.dict("os.environ",{},clear=True),redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(main([]),2)
        result=json.loads(stream.getvalue())
        self.assertEqual(result["cases_executed"],0)
        self.assertIsNone(result["metrics"])
    def test_mock_scoring_all_public_synthetic_questions(self):
        cases=[json.loads(x) for x in (Path(__file__).parents[1]/"eval/agent_questions_review.jsonl").read_text(encoding="utf-8-sig").splitlines() if x.strip()]
        by_question={x["question"]:x for x in cases}
        async def mock(request,key):
            c=by_question[request.question]
            output={**c.get("expected_n",{}),**c.get("expected_output",{})}
            if "expected_power" in c: output["power"]=c["expected_power"]
            return {"decision":{"label":c["expected_label"],"action":c["expected_action"]},"tool_calls":[{"tool_input":c["expected_tool_input"],"tool_output":output}] if c.get("expected_tool_input") is not None else []}
        result=asyncio.run(evaluate_cases(cases,argparse.Namespace(model="mock-only",endpoint="unused",log="unused"),"mock-key",run_one=mock))
        self.assertEqual(result["completed"],10)
        self.assertTrue(all(v==1 for v in result["metrics"].values()))
        # Explicit mock mechanics test, never a saved live evaluation result.
    def test_null_oracle_is_unknown_not_success(self):
        case={"id":"null-fixture","question":"synthetic null oracle", "expected_label":"t2-indep", "expected_action":"call_tool", "expected_tool_input":{"test":"t2-indep"}, "expected_n":None,"expected_power":None,"expected_output":None}
        async def mock(request,key):
            return {"decision":{"label":"t2-indep","action":"call_tool"},"tool_calls":[{"tool_input":{"test":"t2-indep"},"tool_output":{"power":.8}}]}
        result=asyncio.run(evaluate_cases([case],argparse.Namespace(model="mock-only",endpoint="unused",log="unused"),"mock-key",run_one=mock))
        self.assertIsNone(result["rows"][0]["scores"]["output_correct"])
        self.assertIsNone(result["metrics"]["output_correct"])
        self.assertEqual(result["metric_denominators"]["output_correct"],0)
        self.assertEqual(result["metric_denominators"]["tool_input_correct"],1)

if __name__=="__main__": unittest.main()
