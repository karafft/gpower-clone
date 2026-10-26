"""Collect provider configuration locally and run the real MCP agent evaluation."""
import getpass
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse


def main():
    root=Path(__file__).resolve().parents[1]
    model=input("Model adi: ").strip() or os.environ.get("GPOWER_MODEL","")
    default=os.environ.get("GPOWER_ENDPOINT","https://api.openai.com/v1/chat/completions")
    endpoint=input(f"Chat Completions URL [{default}]: ").strip() or default
    parsed=urlparse(endpoint)
    if not model or parsed.scheme!="https" or not parsed.netloc or parsed.username or parsed.password:
        print("Model adi ve kullanici/parola icermeyen HTTPS servis URL'si gerekli.")
        return 2
    key=os.environ.get("GPOWER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        key=getpass.getpass("API anahtari (ekranda gorunmez, dosyaya kaydedilmez): ").strip()
    if not key:
        print("Anahtar girilmedi; hicbir API cagrisi yapilmadi.")
        return 2
    child=dict(os.environ,GPOWER_MODEL=model,GPOWER_ENDPOINT=endpoint,GPOWER_API_KEY=key)
    print("10 sentetik soru gercek model ve MCP ile denenecek; servis kullanim ucreti olabilir.")
    print("Ucretsiz kota icin sorular arasinda 30 saniye beklenir. Yaklasik 5-10 dakika surebilir.")
    result=subprocess.run([sys.executable,"-m","gpower_clone.agent.evaluate","--run-live","--delay","30"],cwd=root,env=child)
    child.pop("GPOWER_API_KEY",None)
    print("Rapor: logs/agent_evaluation.json; cagrilar: logs/agent_calls.jsonl")
    print("Gercek GUI ajan kaydi alinmadan GUI/MCP token kazanci hesaplanamaz.")
    return result.returncode


if __name__=="__main__":
    raise SystemExit(main())
