# Oturum 3: Repo, MCP sunucusu ve ajan (Zeliha)

Üç kişilik bir G*Power tersine mühendislik projesinde repo, entegrasyon, MCP sunucusu ve AI ajanı sorumlusuyum. Sude inceleme, SPEC.md ve bağımsız doğrulamayı; Merve temiz odada motoru ve CLI'yi yapıyor. Aile t2-indep (iki bağımsız ortalama için t testi).

## Kurallar
- Hesap mantığı yalnızca Merve'nin motorundadır (`src/gpower_clone/engine/`). MCP ve ajan katmanında hesap formülü yazılmaz, motor kopyalanmaz, motor değiştirilmez. Motorda hata görürsen düzeltme, bana bildir; düzeltme Merve'nin oturumunda yapılır.
- Bu oturum Sude'nin inceleme kayıtlarını (LEDGER.md, ham kanıtlar) motor tasarımı için kullanmaz.
- Bonus katmanlara ancak bağımsız doğrulamada N en az %90 tam eşleştiğinde geçilir. O zamana kadar repo düzeni ve iskeletle ilgileniyoruz.
- GPower.exe, decompile çıktısı, API anahtarları ve `.env` repoya girmez.
- Harici AI API'sine yalnızca kurgusal senaryolar gönderilir. Gerçek hasta verisi hiçbir zaman kullanılmaz ve loglara girmez.

## 1. Repo
- `.gitignore` ve README iskeleti ilk commit'tir.
- Dizin yapısı `docs/GOREV_DAGILIMI.md` dosyasındaki gibidir; kurulumlar `docs/KURULUM.md` dosyasında.
- Herkes kendi dosyasını kendi hesabıyla commit eder. Başkasının dosyasını onun yerine commit etme.

## 2. MCP sunucusu
- Dosya: `src/gpower_clone/mcp_server.py`. Tek araç sunar: `power_analysis`.
- Aracın girdileri CLI parametreleriyle birebir aynıdır (`test`, `mode`, `tails`, `d`, `alpha`, `power`, `ratio`, `n1`, `n2` ...).
- Araç, CLI ile aynı motor fonksiyonunu çağırır ve CLI'nin döndüğü JSON ile aynı JSON'u döndürür. Hatalar da aynıdır.
- Araç şeması (girdi ve çıktı alanları, tipleri, örnekler) README'de belgelenir.
- **Eşdeğerlik testi** (`tests/test_mcp_parity.py`): `public_vectors.jsonl` içindeki 25 vektörün tamamı hem CLI'ye hem MCP'ye verilir ve çıktılar alan alan karşılaştırılır. t2-indep dışındaki ailelerde iki yol da aynı `UNSUPPORTED` hatasını vermelidir.

## 3. Ajan
- Dosya: `src/gpower_clone/agent/`. Hekimin Türkçe sorduğu klinik soruyu anlar, `power_analysis` aracını çağırır ve sonucu Türkçe açıklar.
- Ajan hiçbir sayıyı kendisi hesaplamaz. N, güç ve etki büyüklüğü ya kullanıcıdan ya da motordan gelir.
- "Orta etki", "küçük fark" gibi ifadelerde sessizce d = 0.5 almaz. Cohen (1988) varsayımını yanıtta açıkça belirtir ya da araştırmacıdan onay ister.
- Soru t2-indep dışındaysa (eşleştirilmiş ölçüm, üç kol, oranlar, regresyon) ya da belirsizse araştırmacıya sorar; zorla t2-indep'e uydurmaz.
- Aile seçimi için ayrı bir sınıflandırma adımı olabilir. Etiket seti: `t2-indep`, `t-paired`, `anova-oneway`, `chi2-contingency`, `multireg-r2`, `ambiguous`, `unsupported`. Güven 0.75'in altındaysa ya da etiket `ambiguous` veya `unsupported` ise karar araştırmacıya sorulur. Bu adımda Jev'e erişim yoksa aynı etiket setine kısıtlanmış bir LLM kullanılır ve README'de belirtilir.
- **Log:** Her araç çağrısı `logs/agent_calls.jsonl` dosyasına tek satır JSON olarak yazılır. Alanlar: `ts`, `question`, `tool_input`, `tool_output`, `tokens_in`, `tokens_out`.

## 4. Değerlendirme
- **Soru seti:** `eval/agent_questions.jsonl` içinde 10 kurgusal Türkçe klinik soru. Her soru için beklenen aile, parametreler ve N yazılır. Beklenen N'yi Sude G*Power arayüzünden alır. Setin içinde en az birkaç aile dışı ve belirsiz soru olmalı.
- **Doğru seçim oranı:** aile, parametreler ve N ayrı ayrı raporlanır.
- **Token karşılaştırması:** Aynı 10 soru iki yoldan çözülür:
  - MCP aracıyla
  - G*Power arayüzünde ekran görüntüsü alıp tıklayarak
  Her iki yol için token, süre ve doğruluk ölçülür ve tabloya yazılır. Bu ölçüm için G*Power'ı ancak motor dondurulduktan sonra açarım.
- İsteğe bağlı: Aynı soruların İngilizce çevirisiyle de ölç ve iki dili karşılaştır. Sınıflandırıcının güven kalibrasyonunu raporla ("%90 güven" dediği seçimlerin gerçekte yüzde kaçı doğru?).

## 5. README
README şunları içerir:
- en başta hangi katmanların yapıldığı (CLI / MCP / ajan)
- kurulum ve tek komutla çalıştırma
- sürüm bilgisi ve GPower.exe SHA-256 hash'i
- "REA araçları kullanılabilir mi?" ekran görüntüsü
- MCP araç şeması
- demo videosu linki (60 saniyelik CLI demosu)
- oturum düzeni: iki inceleme oturumu (Sude) ve bir temiz oda yazım oturumu (Merve), ayrıca MCP/ajan oturumu
- atıf: Faul, Erdfelder, Lang ve Buchner (2007, 2009). Bu proje G*Power değildir ve onun yerine sunulmaz.

## Ayrıca
- AGENT_COST.md için bu oturumun yaklaşık token kullanımını ve iterasyon sayısını not et.
- Bu oturumda yanlış çıkan bir şey olursa HALLUCINATIONS.md için kaydet.

İlk olarak repo iskeletini kuralım.
