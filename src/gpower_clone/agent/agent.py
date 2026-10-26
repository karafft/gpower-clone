"""API-backed LLM tool loop over a real MCP stdio ClientSession."""
import argparse
import asyncio
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SYSTEM = """TÃ¼rkÃ§e klinik araÅŸtÄ±rma gÃ¼Ã§ analizi yardÄ±mcÄ±sÄ±sÄ±n. HesaplarÄ± yalnÄ±z power_analysis aracÄ±yla yap; sayÄ± uydurma.
YalnÄ±z t2-indep ve beÅŸ mod desteklenir. Alanlar: a-priori tails,d,alpha,power,ratio;
post-hoc tails,d,alpha,n1,n2; compromise tails,d,beta_alpha_ratio,n1,n2;
criterion tails,d,power,n1,n2; sensitivity tails,alpha,power,n1,n2.
Her Ã§aÄŸrÄ±da test ve mode belirt. TÃ¼m deÄŸerler kullanÄ±cÄ± tarafÄ±ndan aÃ§Ä±kÃ§a verilmiÅŸ veya Ã¶nce kullanÄ±cÄ±ya sunulup onaylanmÄ±ÅŸ olmalÄ±.
Eksik veya belirsiz bilgi varsa sor; sessiz varsayÄ±lan kullanma. 'Orta etki' gibi ifadeleri sayÄ±ya sessizce Ã§evirme:
baÄŸÄ±msÄ±z t iÃ§in d=0.5 Ã¶nerisini varsayÄ±m olarak aÃ§Ä±kla ve onay iste, sonra Ã§aÄŸÄ±r.
Kuyruk ve grup oranÄ±nÄ± tahmin etme. AraÃ§ hatasÄ±nÄ± dÃ¼rÃ¼stÃ§e aÃ§Ä±kla. G*Power eÅŸdeÄŸerliÄŸi kanÄ±tlanmÄ±ÅŸ deme.
Hasta kimlikleri veya gerÃ§ek kiÅŸi verileri isteme; yalnÄ±z sentetik/kimliksiz tasarÄ±m bilgisi kullan."""

def complete(messages, tools, endpoint, model, key):
    body = {"model": model, "messages": messages, "tools": tools, "tool_choice": "auto"}
    request = Request(endpoint, data=json.dumps(body).encode(), headers={"Content-Type":"application/json", "Authorization":"Bearer "+key}, method="POST")
    with urlopen(request, timeout=60) as response: return json.load(response)

def log_record(path, **fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"ts":datetime.now(timezone.utc).isoformat(), **fields}, ensure_ascii=False, allow_nan=False)+"\n")

async def chat(args, key):
    child_env = {k:v for k,v in os.environ.items() if k not in {"GPOWER_API_KEY", "OPENAI_API_KEY"}}
    params = StdioServerParameters(command=sys.executable, args=["-m","gpower_clone.mcp_server"], env=child_env)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=30)) as session:
            await session.initialize()
            listed = await session.list_tools()
            tools = [{"type":"function", "function":{"name": t.name, "description":t.description, "parameters":t.inputSchema}} for t in listed.tools]
            messages = [{"role":"system", "content":SYSTEM}]
            if getattr(args,"structured",False):
                messages.append({"role":"system","content":"Son yanÄ±tÄ±n yalnÄ±z JSON olsun: {\"action\":\"call_tool|ask_user|report_unsupported\",\"label\":\"t2-indep veya tanÄ±mladÄ±ÄŸÄ±n test ailesi veya ambiguous\",\"message\":\"TÃ¼rkÃ§e aÃ§Ä±klama/soru\"}. call_tool yalnÄ±z gerÃ§ek araÃ§ Ã§aÄŸrÄ±sÄ± yaptÄ±ÄŸÄ±nda kullanÄ±labilir. Desteklenmeyen aileyi adÄ±yla sÄ±nÄ±flandÄ±r; belirsiz aile ambiguous. Eksik bilgi iÃ§in clarify."})
            question = args.question
            while True:
                if question is None:
                    try: question = input("Soru (Ã§Ä±kÄ±ÅŸ: /quit): ")
                    except EOFError: return
                if question.strip() == "/quit": return
                messages.append({"role":"user", "content":question})
                trace=[]
                for _ in range(8):
                    response = await asyncio.to_thread(complete, messages, tools, args.endpoint, args.model, key)
                    message = response["choices"][0]["message"]
                    messages.append(message)
                    usage = response.get("usage")
                    log_record(str(Path(args.log).with_name("llm_responses.jsonl")), event="llm_response", question=question, output=message, usage=usage, provider_response_id=response.get("id"), synthetic=True)
                    calls = message.get("tool_calls") or []
                    if not calls:
                        content=message.get("content") or ""
                        decision=json.loads(content) if getattr(args,"structured",False) else None
                        if decision is not None:
                            if not isinstance(decision,dict) or decision.get("action") not in {"call_tool","ask_user","report_unsupported"}: raise ValueError("Invalid structured agent decision")
                            if decision["action"]=="call_tool" and not trace: raise ValueError("Model claimed a tool call without actual execution")
                        print(content)
                        break
                    for index, call in enumerate(calls):
                        fn = call["function"]
                        arguments = json.loads(fn["arguments"])
                        if fn["name"] != "power_analysis" or not isinstance(arguments,dict): raise ValueError("Unexpected tool call")
                        result = await session.call_tool(fn["name"], arguments)
                        output = "".join(c.text for c in result.content if c.type == "text")
                        counts = usage if isinstance(usage,dict) and index == 0 else {}
                        trace.append({"tool_input":arguments,"tool_output":json.loads(output),"is_error":bool(result.isError)})
                        log_record(args.log, question=question, tool_input=arguments, tool_output=json.loads(output), tokens_in=counts.get("prompt_tokens"), tokens_out=counts.get("completion_tokens"), provider_response_id=response.get("id"), usage_attribution="triggering model response; attributed only to first tool call", synthetic=True)
                        messages.append({"role":"tool", "tool_call_id":call["id"], "content":output})
                else: raise RuntimeError("Tool loop limit reached")
                if args.question is not None: return {"decision":decision,"tool_calls":trace,"final_text":content}
                question = None

def main(argv=None):
    parser = argparse.ArgumentParser(description="LLM + actual MCP stdio power-analysis agent; synthetic cases only")
    parser.add_argument("--question")
    parser.add_argument("--model", default=os.environ.get("GPOWER_MODEL"))
    parser.add_argument("--endpoint", default=os.environ.get("GPOWER_ENDPOINT", "https://api.openai.com/v1/chat/completions"))
    parser.add_argument("--log", default="logs/agent_calls.jsonl")
    parser.add_argument("--structured",action="store_true",help="Require model final JSON action/label/message; retain actual tool trace")
    parser.add_argument("--synthetic-case", action="store_true", required=True, help="Confirm only synthetic, non-identifying case data will be used")
    args = parser.parse_args(argv)
    key = os.environ.get("GPOWER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key or not args.model:
        parser.error("Set API key in GPOWER_API_KEY/OPENAI_API_KEY and model in --model/GPOWER_MODEL; no provider call was made")
    try: asyncio.run(chat(args,key))
    except Exception as exc:
        print("Agent stopped: "+type(exc).__name__+"; inspect local setup/provider response without sharing secrets", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__": raise SystemExit(main())
