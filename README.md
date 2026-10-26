# gpower-clone

İki bağımsız grup ortalaması için t testi (`t2-indep`) güç analizi. G*Power 3.1.9.7'nin bu hesabı temiz oda yöntemiyle yeniden yazıldı. Hesap tek bir motorda; CLI, MCP sunucusu ve ajan bu motoru çağıran ince katmanlar.

YZM301 Teardown Sprint · Aile: t2-indep (K1) · Ekip: Sude Naz Öztoprak, Merve Beyazal, Zeliha

> Bu proje G*Power değildir ve onun yerine sunulmaz. G*Power yalnızca resmi sayfasından indirilmelidir.

## Yapılan katmanlar

| Katman | Durum |
|---|---|
| CLI (temel) | ✅ Beş mod: a-priori, post-hoc, compromise, criterion, sensitivity |
| MCP sunucusu | ✅ `power_analysis` aracı; CLI ile eşdeğerlik testi geçiyor |
| AI ajanı | ⚠️ Kod ve testler hazır. Canlı model değerlendirmesi ve GUI ile token karşılaştırması **yapılmadı** (bkz. Bilinen sınırlar) |

## Sonuçlar

| Kontrol | Sonuç | Kayıt |
|---|---|---|
| Yazılım testleri (gerçek MCP dahil) | 28/28 geçti | `tests/reports/final_audit_unit.txt` |
| Açık referans vektörleri (t2-indep, 5 mod) | 5/5 | `tests/reports/final_audit_public.json` |
| Ekran görüntülü G*Power kayıtları (ORC) | 58/58 kayıt, 38/38 N tam eşleşme | `tests/reports/final_audit_screenshots58.json` |
| Motor dondurulduktan sonra yapılan 14 yeni G*Power deneyi | 14/14 kayıt, 10/10 N tam eşleşme | `tests/reports/final_audit_prospective14.json` |
| MCP ile CLI çıktısı eşitliği | 33/33 (25 açık vektör ve 8 geçersiz girdi) | `logs/mcp_parity.jsonl` |
| statsmodels ile sayısal çapraz kontrol | 540/540, en büyük güç farkı 5.55e-16 | `oracle/scale/` |

N, n1 ve n2 tam eşitlikle, diğer değerler 1e-6 mutlak ya da göreli toleransla karşılaştırıldı (CONTRACT.md Bölüm 6).

Bağımsız kontrol: Sude'nin özgün G*Power protokol belgesindeki bütün a-priori deneyleri (repodaki türetilmiş dosyalar kullanılmadan) CLI'ye ayrıca verildi. Sözleşmeye uygun 38 deneyin 38'inde n1 ve n2 tam eşleşti. Uymayan tek deney negatif d içeren ORC-050; sözleşme d > 0 istediği için CLI onu bilerek reddediyor.

Bu sonuçlar geliştirme ve takip setlerine aittir. Hocanın gizli vektörlerindeki sonucu bilmiyoruz.

## Kurulum ve çalıştırma

Python 3.10 veya üstü gerekir. Proje kökünde:

```sh
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[mcp]"      # Windows
.venv/bin/python -m pip install -e ".[mcp]"          # Linux / macOS
```

CLI:

```sh
gpower-clone --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.8 --ratio 1
gpower-clone --version
```

```json
{"ncp":2.8284271247461903,"critical_t":1.9789706019906288,"df":126,"n1":64,"n2":64,"n_total":128,"actual_power":0.8014595579222543}
```

Windows'ta konsol komutu engellenirse aynı çağrı `python -m gpower_clone ...` ya da `gpower-clone.cmd` ile yapılabilir.

Testler:

```sh
python -m unittest discover -s tests
```

MCP sunucusu (stdio): `python -m gpower_clone.mcp_server`. Araç şeması ve ajan kurulumu: [README_IMPLEMENTATION.md](README_IMPLEMENTATION.md), [docs/ZELIHA_KURULUM.md](docs/ZELIHA_KURULUM.md).

## Demo

▶️ **[60 saniyelik CLI demosu (YouTube)](https://youtu.be/vt77iAK14kM)**: sürüm bilgisi, a-priori, eşit olmayan grup oranı, post-hoc, sensitivity ve iki geçersiz girdi. Aynı adımlar `powershell -ExecutionPolicy Bypass -File demo\run_demo.ps1` ile yeniden çalıştırılabilir.

## MCP aracı: `power_analysis`

| | |
|---|---|
| Girdi | CLI ile aynı alan adları: `test`, `mode` zorunlu; moda göre `tails`, `d`, `alpha`, `power`, `ratio`, `n1`, `n2`, `beta_alpha_ratio` |
| Çıktı | CLI'nin stdout'a yazdığı JSON satırıyla birebir aynı metin |
| Hata | Aynı `{"error", "code", "field"}` JSON'u, `isError=true` ile |

## Sürüm bilgisi

| | |
|---|---|
| İncelenen program | G*Power 3.1.9.7 (Windows), resmi HHU indirmesi |
| GPowerNT.exe SHA-256 | `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812` |
| Sözleşme | CONTRACT.md v1.0.0 (değiştirilmedi) |
| Değerlendirilen sürüm | 1.1.0rc4 |

GPower.exe ve decompile çıktısı repoda yoktur.

## Teslim dosyaları

| Yönergedeki madde | Dosya |
|---|---|
| SPEC.md, Gherkin kabul kriterleri | [SPEC.md](SPEC.md), [features/t2_indep.feature](features/t2_indep.feature) |
| Kanıt defteri ([DOK], [REA], [AJAN]) | [LEDGER.md](LEDGER.md), [docs/REA_STATIC_FINDINGS.md](docs/REA_STATIC_FINDINGS.md) |
| Halüsinasyon günlüğü | [HALLUCINATIONS.md](HALLUCINATIONS.md), [HALLUCINATIONS_IMPLEMENTATION.md](HALLUCINATIONS_IMPLEMENTATION.md) |
| Ajan maliyet günlüğü | [AGENT_COST.md](AGENT_COST.md), [AGENT_COST_IMPLEMENTATION.md](AGENT_COST_IMPLEMENTATION.md) |
| Oturumların ilk prompt'ları | [prompts/](prompts/) |
| G*Power vektörleri (CSV) ve ekran görüntüleri | [oracle/vectors.csv](oracle/vectors.csv), `oracle/sude_screenshots/`, `oracle/new_validation/` |
| Yeniden yazım | `src/gpower_clone/` (motor `engine/`, `cli.py`, `mcp_server.py`, `agent/`) |
| Diferansiyel test ve uyum raporu | `tests/`, [REPORT.md](REPORT.md) |
| Demo (60 saniyelik CLI videosu) | [YouTube](https://youtu.be/vt77iAK14kM), [demo/CLI_Demo_ekran_kaydi.mp4](demo/CLI_Demo_ekran_kaydi.mp4) (gerçek terminal kaydı); ayrıntı [demo/README.md](demo/README.md) |
| Ajan değerlendirme seti | [eval/agent_questions.jsonl](eval/agent_questions.jsonl) |

## Temiz oda

İnceleme tarafı GPowerNT.exe'yi, G*Power arayüz deneylerini ve kanıtları gördü. Motoru yazan AI oturumu ayrı başlatıldı ve yalnızca SPEC/CONTRACT ile şartname eklerini aldı; ekran görüntüleri, ham protokol ve binary o oturuma verilmedi. Aktarılan şartname ekleri `prompts/spec_handoffs/` altındadır. Ayrıntı ve sınırlar: [docs/CLEAN_ROOM_PROVENANCE.md](docs/CLEAN_ROOM_PROVENANCE.md).

Ayrım AI oturumları arasındadır. Koordinasyon ve yazım oturumlarının ikisi de aynı ekip üyesinin hesabından yürütüldü; bu nedenle insan düzeyinde bir bağımsızlık iddia etmiyoruz.

## Ekip katkıları

| Kişi | Katkı |
|---|---|
| Sude Naz Öztoprak | G*Power arayüz deneyleri (60 kayıt ve ekran görüntüsü), ilk SPEC ve ilk vektör seti |
| Merve Beyazal | İnceleme koordinasyonu ve ayrı temiz oda uygulama oturumu (AI destekli): motor, CLI, MCP, ajan kodu, statik binary incelemesi, takip deneyleri, raporlar |
| Zeliha | Repo ve görev planı, oturum prompt'ları, CONTRACT ve açık vektörlerin eklenmesi, ajan değerlendirme soruları, geri bildirim ve deney planı, halüsinasyon ve maliyet günlükleri, bağımsız doğrulama ve teslim paketi |

Kod AI oturumlarıyla üretildi; bu, temiz oda kaydında ve maliyet günlüğünde açıkça belirtilmiştir.

## Bilinen sınırlar

- **Canlı ajan değerlendirmesi yapılmadı.** Ajan kodu ve sahte sağlayıcıyla MCP döngüsü testleri geçiyor. Gerçek bir LLM ile 10 soruluk değerlendirme ve GUI ile token karşılaştırması bir API anahtarı gerektiriyor. Ölçülmemiş sonuç yazılmadı.
- **REA ve Ghidra araçları kullanılmadı.** Statik binary incelemesi Python PE okuması ve Capstone ile yapıldı. [REA] kayıtları gerçek adres ve dize referanslarına dayanıyor, ama ders aracının kullanılabilirlik ekran görüntüsü yok.
- Eski ara raporlar `tests/reports/`, `logs/` ve `docs/history/` altında tarihsel kayıt olarak duruyor. Güncel sonuçlar `final_audit` önekli dosyalardadır.

## Atıf

Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods, 39*, 175–191.

Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G. (2009). Statistical power analyses using G*Power 3.1: Tests for correlation and regression analyses. *Behavior Research Methods, 41*, 1149–1160.
