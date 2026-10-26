import argparse
import asyncio
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from gpower_clone.agent.agent import chat, main

class AgentTests(unittest.TestCase):
    def test_no_key_no_provider_call(self):
        with patch.dict("os.environ", {}, clear=True), patch("gpower_clone.agent.agent.complete") as provider, redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                main(["--synthetic-case", "--model", "test-model"])
            self.assertEqual(result.exception.code,2)
            provider.assert_not_called()

    def test_mock_provider_real_mcp_loop(self):
        # Provider fixtures are synthetic test doubles, never live LLM evidence.
        responses=[{"id":"mock-call", "choices":[{"message":{"role":"assistant", "content":None,"tool_calls":[{"id":"call1","type":"function","function":{"name":"power_analysis","arguments":json.dumps(dict(test="t2-indep",mode="post-hoc",tails=1,d=.5,alpha=.05,n1=88,n2=88))}}]}}]}, {"id":"mock-final","choices":[{"message":{"role":"assistant","content":"synthetic mock answer"}}]}]
        with tempfile.TemporaryDirectory() as folder:
            log=Path(folder)/"calls.jsonl"
            args=argparse.Namespace(question="Synthetic explicit post-hoc case", endpoint="https://example.invalid",model="mock-only",log=str(log))
            with patch("gpower_clone.agent.agent.complete",side_effect=responses) as provider, redirect_stdout(io.StringIO()) as output:
                asyncio.run(chat(args,"mock-key"))
            self.assertIn("synthetic mock answer",output.getvalue())
            history=provider.call_args_list[1].args[0]
            self.assertTrue(any(x["role"]=="tool" for x in history))
            records=[json.loads(x) for x in log.read_text(encoding="utf-8").splitlines()]
            calls=records
            self.assertEqual(len(calls),1)
            self.assertIsNone(calls[0]["tokens_in"])
            self.assertIsNone(calls[0]["tokens_out"])
            self.assertAlmostEqual(calls[0]["tool_output"]["power"],.9514254482775332)

if __name__=="__main__": unittest.main()
