# YZM301 · t2-indep · Görev dağılımı ve çalışma protokolü

Aile: **t testi, iki bağımsız ortalama (t2-indep)**. Modlar: a-priori ve post-hoc (zorunlu), compromise / criterion / sensitivity (bonus).
Sözleşme: hocanın CONTRACT.md'si (gpower-clone v1.0.0). Çıktı ve hata biçimi bu belgeye harfiyen uyar.

## Temel ilke
Puan yalnızca **[REA]** kanıtlarına veriliyor. [REA] = GPower.exe içinde REA veya Ghidra ile bulunan **fonksiyon adresi ya da dize referansı**. Arayüzde değer girip sonucu okumak [REA] değil, kâhin (oracle) verisidir. İkisini de topluyoruz ama ayrı etiketle:

| Etiket | Anlamı |
|---|---|
| `[REA-xxx]` | Binary kanıtı (adres, dize referansı, kısa alıntı) |
| `[ORC-xxx]` | G*Power arayüzünde yapılmış deney, ekran görüntüsüyle |
| `[DOK-xxx]` | Kılavuz veya makale (sayfa numarasıyla) |
| `[AJAN-xxx]` | Kanıtı olmayan çıkarım; test edilmesi gereken hipotez |
| `[VAL-xxx]` | Gizli doğrulama vektörü (Merve görmez) |

---

## 1. Sude: İnceleme, SPEC ve doğrulama (kirli oda)

**Görev**
- G*Power 3.1.9.7'yi resmi sayfadan kurar. SHA-256 hash'ini ve sürüm ekranını kaydeder.
- **REA ve Ghidra** ile GPower.exe'yi inceler: N araması, yuvarlama, n1/n2 dağılımı, durma koşulu, df / ncp / kritik değer, geçersiz girdi tepkisi. Bulguları fonksiyon adresi ve dize referansıyla `[REA]` olarak kaydeder.
- Arayüzde **en az 30 deney** yapar, her biri ekran görüntüsüyle (`[ORC]`). Sınır değerler zorunlu: çok küçük/büyük d, güç ≤ α, eşit olmayan oran, N'nin bir arttığı eşikler, geçersiz girdiler.
- statsmodels ile **500'den fazla ölçek vektörü** üretir. Kesirli N ile G*Power'ın tam sayı N'si arasındaki farkı açıklar.
- Kanıtlardan **SPEC.md** yazar. Kabul kriterleri Gherkin formatında olur, her kural `[Doğrulandı]`, `[Varsayım]` veya `[CLI kararı]` olarak işaretlenir.
- Geliştirme setinden ayrı, **gizli bir doğrulama seti** (`[VAL]`) tutar. Merve'ye ve SPEC.md'ye ilk değerlendirmeye kadar aktarmaz.
- Merve sürümü sabitleyince karşılaştırmayı Sude yürütür ve uyum raporunu yazar.
- Ajan değerlendirme seti için 10 klinik sorunun beklenen N değerlerini G*Power'dan alır.

**Teslim**
- `LEDGER.md`, `SPEC.md`
- `oracle/vectors.csv` ve `oracle/screenshots/`
- `oracle/scale/` (statsmodels vektörleri)
- `tests/reports/` (uyum raporu)
- `prompts/01_inceleme_spec_sude.md`

---

## 2. Merve: Motor ve CLI (temiz oda)

**Görev**
- **Yalnızca SPEC.md ve CONTRACT.md** ile çalışır. G*Power'ı kurmaz, açmaz.
- AI oturumunu repo içinde değil, yalnızca bu iki dosyanın bulunduğu ayrı bir klasörde başlatır. Böylece LEDGER.md, ekran görüntüleri ve ham kanıtlar oturuma hiç girmez.
- Bütün hesap mantığını `src/gpower_clone/engine/` altında tek motorda yazar.
- `scipy.stats` yalnızca dağılım fonksiyonları için kullanılır (t, merkezi olmayan t). **N araması, yuvarlama ve df hesabı ekibin kendi kodudur;** `scipy.optimize` ile N aranmaz.
- İnce bir CLI yazar (`gpower-clone`):
  - stdout'a yalnızca tek satır JSON yazılır; loglar stderr'e gider.
  - Tam sayı alanlar (`n1`, `n2`, `n_total`, `df`) JSON tam sayısı olur; `88.0` olmaz.
  - Ondalık değerler yuvarlanmaz, tam double hassasiyetinde kalır.
  - Çıktı alanları: `n1`, `n2`, `n_total`, `actual_power`, `power`, `alpha`, `beta`, `critical_t`, `df`, `ncp`.
  - Hata çıktısı: `{"error": "...", "code": "...", "field": "..."}`.
  - Hata kodları: `MISSING_PARAM`, `UNKNOWN_PARAM`, `INVALID_VALUE`, `OUT_OF_RANGE`, `INCONSISTENT`, `UNSUPPORTED`, `NO_SOLUTION`.
  - Çıkış kodları: 0 başarı, 2 geçersiz girdi, 1 dahili hata.
  - `gpower-clone --version` sözleşmedeki JSON'u döndürür.
- SPEC'teki Gherkin senaryolarını ve geliştirme örneklerini teste çevirir.
- Testler geçince sürümü git etiketiyle sabitler (örn. `v0.1.0`) ve Sude'ye bildirir. Değerlendirme bitene kadar kodu değiştirmez.

**Teslim**
- `src/gpower_clone/engine/` ve `src/gpower_clone/cli.py`
- `tests/test_engine.py` ve `tests/test_cli_contract.py`
- `prompts/02_uygulama_merve.md`

---

## 3. Zeliha: Repo, entegrasyon, MCP ve ajan

**Görev**
- Repoyu açar. İlk commit `.gitignore` ve README iskeletidir. Sude ile Merve'yi collaborator olarak ekler.
- **MCP sunucusu** (`src/gpower_clone/mcp_server.py`): tek araç, `power_analysis`. Motoru doğrudan çağırır; MCP katmanında hesap formülü olmaz. Araç şeması README'de belgelenir.
- **CLI–MCP eşdeğerlik testi** (`tests/test_mcp_parity.py`): `public_vectors.jsonl` içindeki 25 vektörün tamamında CLI ve MCP aynı JSON'u verir. t2-indep dışındaki ailelerde bu, aynı `UNSUPPORTED` hatası demektir.
- **Ajan** (`src/gpower_clone/agent/`): Türkçe klinik soruyu MCP aracına çevirir; hesabı asla kendisi yapmaz.
  - "Orta etki" gibi ifadelerde sessizce d = 0.5 almaz. Cohen (1988) varsayımını açıkça yazar ya da araştırmacıya sorar.
  - Aile dışı veya belirsiz sorularda araştırmacıya sorar.
- Her araç çağrısı `logs/agent_calls.jsonl` dosyasına tek satır JSON olarak yazılır: `ts`, `question`, `tool_input`, `tool_output`, `tokens_in`, `tokens_out`.
- **10 soruluk değerlendirme seti:** Her soru için beklenen aile, parametreler ve N yazılır; beklenen N'yi Sude G*Power'dan verir. Doğru seçim oranı raporlanır.
- **Token karşılaştırması:** Aynı 10 soru hem MCP hem GUI (ekran görüntüsüyle) yoluyla çözülür; token, süre ve doğruluk raporlanır. Bunun için Zeliha, **motor dondurulduktan sonra** G*Power'ı açabilir. Temiz oda kuralı motoru yazan Merve için geçerli; bu ölçüm temizliği bozmaz.
- README'yi tamamlar: yapılan katmanlar (en başta), kurulum, çalıştırma, sürüm bilgisi, SHA-256, demo videosu, REA kullanılabilirlik ekran görüntüsü ve atıf (Faul, Erdfelder, Lang ve Buchner, 2007, 2009).
- 60 saniyelik CLI demo videosunu çeker.

**Teslim**
- `src/gpower_clone/mcp_server.py` ve `src/gpower_clone/agent/`
- `tests/test_mcp_parity.py`
- `logs/agent_calls.jsonl` ve `eval/agent_questions.jsonl`
- README.md
- `prompts/03_mcp_ajan_zeliha.md`

---

## Herkesin ortak sorumluluğu
- **HALLUCINATIONS.md:** Kendi AI oturumunda yanlış çıkan her şeyi kaydeder: ne iddia edildi, nasıl fark edildi, hangi test yakaladı. En az 2 kayıt gerekiyor; çoğu Sude'nin oturumundan gelir.
- **AGENT_COST.md:** Kendi oturumunun ajanını, yaklaşık token ve maliyetini, iterasyon sayısını ve "neyi farklı yapardım" notunu yazar.
- **Commit'ler:** Herkes kendi dosyasını kendi hesabıyla commit eder. Commit geçmişi temiz oda ayrımının kanıtıdır.

## Akış ve kapılar
1. **Hazırlık (Zeliha):** Repo, `.gitignore`, README iskeleti, collaborator davetleri.
2. **İnceleme (Sude):** LEDGER.md, oracle vektörleri, SPEC.md v1. Gizli [VAL] seti repoya henüz girmez.
3. **Yazım (Merve):** SPEC.md ve CONTRACT.md ile motor ve CLI. Sürüm etiketi.
4. **Değerlendirme (Sude):** Etiketli sürüm [VAL] setiyle karşılaştırılır.
   - N, n1 ve n2 için tolerans sıfır; diğer alanlar 1e-6.
   - Rapor: toplam vektör, tam eşleşme oranı, her uyuşmazlık ve açıklaması.
   - **%90 altındaysa MCP ve ajana geçilmez.** SPEC düzeltilir; düzeltme için açılan vektörler geliştirme setine geçer, sonraki tur için yeni [VAL] vektörleri ayrılır.
5. **Bonus (Zeliha):** MCP, eşdeğerlik testi, ajan, değerlendirme seti, token karşılaştırması.
6. **Kapanış (herkes):** HALLUCINATIONS.md, AGENT_COST.md, README, demo videosu.

Yerel doğrulamada %90'ı geçmek, hocanın gizli vektörlerinde geçmek anlamına gelmez. Raporlarda böyle sunulmayacak.

## Repoda olmayacaklar
- GPower.exe, kurulum dosyası, .zip
- Decompile çıktısı ve ham Ghidra / REA dökümleri (LEDGER'da yalnızca adres ve kısa alıntı)
- `venv/`, `.env`, `__pycache__/`, API anahtarları
- Gerçek hasta verisi
- "G*Power" adını taşıyan bir ürün sunumu; klon G*Power gibi gösterilmez.

## Repo yapısı
```
gpower-clone/
├── README.md
├── CONTRACT.md                # hocanın sözleşmesi, aynen
├── SPEC.md                    # Sude
├── LEDGER.md                  # Sude
├── HALLUCINATIONS.md          # herkes
├── AGENT_COST.md              # herkes
├── public_vectors.jsonl       # hocanın 25 referans vektörü
├── pyproject.toml             # gpower-clone komutu
├── docs/                      # görev dağılımı ve kurulum rehberi
├── prompts/                   # üç oturumun ilk prompt'ları
├── oracle/
│   ├── vectors.csv            # [ORC] vektörleri
│   ├── screenshots/
│   ├── scale/                 # statsmodels vektörleri
│   └── validation/            # [VAL], ilk değerlendirmeden sonra eklenir
├── src/gpower_clone/
│   ├── engine/                # Merve: tek hesap motoru
│   ├── cli.py                 # Merve
│   ├── mcp_server.py          # Zeliha
│   └── agent/                 # Zeliha
├── eval/agent_questions.jsonl # Zeliha + Sude
├── tests/
│   ├── test_engine.py
│   ├── test_cli_contract.py
│   ├── test_differential.py   # Sude
│   ├── test_mcp_parity.py     # Zeliha
│   └── reports/
└── logs/agent_calls.jsonl
```
