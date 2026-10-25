# gpower-clone

İki bağımsız grup ortalaması için t testi (`t2-indep`) güç analizi: a-priori örneklem büyüklüğü ve post-hoc güç. G*Power 3.1.9.7'nin bu hesabı temiz oda yöntemiyle yeniden yazılmıştır ve CLI üzerinden kullanılır.

YZM301 Teardown Sprint · Ekip: Sude, Merve, Zeliha

> Bu proje G*Power değildir ve onun yerine sunulmaz. G*Power yalnızca resmi sayfasından indirilmelidir.

## Yapılan katmanlar
- [ ] CLI (temel)
- [ ] MCP sunucusu
- [ ] AI ajanı

## Kurulum
_Eklenecek._

## Kullanım
```
gpower-clone --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1
```

## Sürüm bilgisi
| | |
|---|---|
| İncelenen program | G*Power 3.1.9.7 (Windows) |
| GPower.exe SHA-256 | _eklenecek_ |
| Sözleşme | CONTRACT.md, gpower-clone v1.0.0 |
| Değerlendirilen sürüm | _eklenecek_ |

## Çalışma düzeni
| Oturum | Kim | Gördüğü kaynaklar | Ürettiği |
|---|---|---|---|
| İnceleme | Sude | GPower.exe, REA, Ghidra, G*Power arayüzü | LEDGER.md, SPEC.md, oracle/ |
| Yazım (temiz oda) | Merve | yalnızca SPEC.md ve CONTRACT.md | src/gpower_clone/engine, cli.py |
| MCP ve ajan | Zeliha | motorun dış arayüzü | mcp_server.py, agent/ |

Her oturumun ilk prompt'u `prompts/` klasöründedir.

## Belgeler
- [CONTRACT.md](CONTRACT.md): eğitmenin arayüz sözleşmesi (v1.0.0, değiştirilmeden)
- [public_vectors.jsonl](public_vectors.jsonl): sözleşmenin 9. bölümündeki 25 referans vektörü
- [eval/](eval/): ajan değerlendirme seti
- [docs/GOREV_DAGILIMI.md](docs/GOREV_DAGILIMI.md): görev dağılımı ve çalışma protokolü
- [docs/KURULUM.md](docs/KURULUM.md): kişi bazında kurulum ve git akışı
- [SPEC.md](SPEC.md): kabul kriterleri (Gherkin)
- [LEDGER.md](LEDGER.md): kanıt defteri
- [HALLUCINATIONS.md](HALLUCINATIONS.md)
- [AGENT_COST.md](AGENT_COST.md)
- `oracle/`: G*Power vektörleri ve ekran görüntüleri
- `tests/`: diferansiyel test ve uyum raporu

## Demo
_Video linki eklenecek._

## Atıf
Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods, 39*, 175–191.

Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G. (2009). Statistical power analyses using G*Power 3.1: Tests for correlation and regression analyses. *Behavior Research Methods, 41*, 1149–1160.
