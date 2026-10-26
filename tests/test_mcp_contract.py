import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from datetime import timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPContractTests(unittest.TestCase):
    def test_real_stdio_handshake_list_call_cli_parity(self):
        asyncio.run(self.check_protocol())

    async def check_protocol(self):
        params=StdioServerParameters(command=sys.executable,args=["-m","gpower_clone.mcp_server"],env=dict(os.environ))
        vectors=Path(__file__).parents[1]/"public_vectors.jsonl"
        if vectors.exists():
            rows=[json.loads(line) for line in vectors.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
            inputs=[row["input"] for row in rows]
        else:
            inputs=[dict(test="t2-indep",mode="post-hoc",tails=1,d=.5,alpha=.05,n1=88,n2=88)]
        inputs += [dict(test="t2-indep",mode="post-hoc"),dict(test="other",mode="post-hoc"),dict(test="t2-indep",mode="other"),dict(test="t2-indep",mode="post-hoc",extra=1)]
        base=dict(test="t2-indep",mode="post-hoc",tails=1,d=.5,alpha=.05,n1=88,n2=88)
        inputs += [dict(base,d="wrong"),dict(base,n1=2.0),dict(base,tails=3),dict(base,alpha=0)]
        async with stdio_client(params) as (read,write):
            async with ClientSession(read,write,read_timeout_seconds=timedelta(seconds=30)) as session:
                handshake=await session.initialize()
                self.assertEqual(handshake.serverInfo.name,"gpower-clone")
                tools=await session.list_tools()
                self.assertEqual([t.name for t in tools.tools],["power_analysis"])
                self.assertIn("test",tools.tools[0].inputSchema["properties"])
                records=[]
                for data in inputs:
                    args=[item for k,v in data.items() for item in ("--"+k,str(v))]
                    cli=await asyncio.to_thread(subprocess.run,[sys.executable,"-m","gpower_clone",*args],capture_output=True,text=True,timeout=20)
                    result=await session.call_tool("power_analysis",data)
                    text="".join(x.text for x in result.content if x.type=="text")
                    self.assertEqual(text,cli.stdout.rstrip("\r\n"),data)
                    self.assertEqual(bool(result.isError),cli.returncode!=0)
                    self.assertEqual(cli.stderr,"")
                    records.append({"input":data,"cli_exit":cli.returncode,"mcp_is_error":bool(result.isError),"output":text,"exact_text_parity":True,"synthetic":True,"source":"scripted public contract vector; not LLM or GPower observation"})
                destination=Path(os.environ.get("GPOWER_MCP_REPORT",str(Path(__file__).parents[1]/"logs/mcp_parity.jsonl")))
                destination.parent.mkdir(parents=True,exist_ok=True)
                destination.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in records),encoding="utf-8")

if __name__=="__main__": unittest.main()
