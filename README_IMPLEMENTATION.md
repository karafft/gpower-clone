# Kurulum ve kullanım

Python3.10+ gerekir. Proje kökünde:

```sh
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\python -m pip install -e ".[mcp,scale]"
.\.venv\Scripts\python tools/check_all.py
```

Linux/macOS:

```sh
.venv/bin/python -m pip install -e ".[mcp,scale]"
.venv/bin/python tools/check_all.py
```

Tek adımlı seçenek: `python tools/check_all.py --install`.

CLI:

```sh
python -m gpower_clone --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.8 --ratio 1
python -m gpower_clone --version
```

Windows’ta konsol exe’si uygulama denetimine takılırsa güvenlik ayarlarını
değiştirmeden aynı modül veya `.\gpower-clone.cmd` kullanılır.

MCP: `python -m gpower_clone.mcp_server`. Tek araç `power_analysis`;
istemci komutu Python yolu, args `["-m","gpower_clone.mcp_server"]` olur.

CLI ve MCP aynı motoru çağırır. Başarı stdout tek JSON satırı, çıkış0;
girdi hatası2, dahili hata1. Tüm mod alanları açıkça verilmelidir; varsayılan yok.
Girdiler/çıktılar [SPEC.md](SPEC.md) ve değişmeyen [CONTRACT.md](CONTRACT.md) içindedir.

Ajan, tool calling destekleyen Chat Completions uyumlu sağlayıcı ister.
Anahtar yalnız yerel GPOWER_API_KEY veya OPENAI_API_KEY ortam değişkeninde,
model GPOWER_MODEL içinde tutulur; repoya/sohbete eklenmez. Özel sağlayıcı
GPOWER_ENDPOINT kullanabilir. Ayar yapıldıktan sonra sentetik bir soru:

```sh
python -m gpower_clone.agent --synthetic-case --question "İki bağımsız grupta çift yönlü t testi, d=0.5, alpha=0.05, power=0.8, oran=1: kaç kişi?"
python -m gpower_clone.agent.evaluate --run-live --model MODEL
```

Canlı koşum yapılmadığında metrikler null/not_run kalır. Mock testler canlı
model başarısı değildir. [Maliyet kaydı](AGENT_COST_IMPLEMENTATION.md).

[Sonuçlar](REPORT.md), [teslim durumu](TESLIM_DURUMU.md),
[temiz oda kaydı](docs/CLEAN_ROOM_PROVENANCE.md), [demo](demo/CLI_Demo_60s.mp4).
G*Power binary’si, bağımlılıklar, kurulum arşivi ve decompile çıktısı teslim edilmez.

## Windows’ta canlı testi başlatma

Proje kökündeki CANLI_AJAN_TESTI.cmd dosyasını çift tıklayın. Model adını,
Chat Completions servis adresini ve ekranda görünmeyen anahtar girişini
yerelde tamamlayın. Anahtar diske yazılmaz.10 sentetik soru gerçek serviste
çalışır; kullanım ücretine tabi olabilir. Sonuç logs/agent_evaluation.json
ve logs/agent_calls.jsonl dosyalarında oluşur. Bu kayıtlar incelenmeden
canlı başarı veya GUI’ye göre token kazancı ilan edilmez.

Groq için yalnız anahtar isteyen kısa yol:

```powershell
.\.venv\Scripts\python.exe tools\run_live_local.py --groq
```

Model ve servis adresi projede seçilen Groq değerleriyle doldurulur.
