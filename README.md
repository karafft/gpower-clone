> **26 Ekim2026 güncellemesi:** Beş t2-indep modu, tek hesap motoru,
> CLI, MCP ve ajan kodu eklendi.25 yazılım testi ve33 MCP/CLI kontrolü geçti.
> Görselle desteklenen57/57 kaynak kaydı (37/37 tam N), ayrıca motor
> dondurulduktan sonra14/14 yeni GUI deneyi (10/10 tam N) eşleşti.
> Toplam74 görsel var. ORC-011’in çıktıları ?; sayısal kanıt olarak sayılmadı.
> Canlı model ve gerçek GUI/MCP token ölçümü henüz yapılmadı.
> Gizli yarışma kapısının sonucu bilinmiyor.
>
> [Kurulum/kullanım](README_IMPLEMENTATION.md) · [Sonuç raporu](REPORT.md) ·
> [Görsel kontrolü](docs/SUDE_GORSEL_KONTROLU.md) · [Şartname önerisi](SPEC_ONERI.md)

# gpower-clone

İki bağımsız grup ortalaması için t testi (`t2-indep`) güç analizi: a-priori örneklem büyüklüğü ve post-hoc güç. G*Power 3.1.9.7'nin bu hesabı temiz oda yöntemiyle yeniden yazılmıştır ve CLI üzerinden kullanılır.

YZM301 Teardown Sprint · Ekip: Sude, Merve, Zeliha

> Bu proje G*Power değildir ve onun yerine sunulmaz. G*Power yalnızca resmi sayfasından indirilmelidir.

## Yapılan katmanlar
- [x] CLI (temel)
- [x] MCP sunucusu
- [x] AI ajanı kodu (canlı model değerlendirmesi bekliyor)

## Kurulum
```sh
python -m pip install -e ".[mcp]"
```

Ayrıntılı kullanım: [README_IMPLEMENTATION.md](README_IMPLEMENTATION.md).

## Kullanım
```
gpower-clone --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1
```

## Sürüm bilgisi
| | |
|---|---|
| İncelenen program | G*Power 3.1.9.7 (Windows) |
| Resmî GPowerNT.exe SHA-256 | `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812` |
| Sözleşme | CONTRACT.md, gpower-clone v1.0.0 |
| Değerlendirilen sürüm | 1.1.0rc4 |

## Ekip planındaki çalışma düzeni

Aşağıdaki tablo başlangıç görev planıdır. Gerçek AI oturum ayrımı ve ek katkılar
[temiz oda kaydında](docs/CLEAN_ROOM_PROVENANCE.md) açıklanır. Bu çalışmadaki statik
inceleme PE/Capstone ile yapıldı; Ghidra kullanıldığı iddia edilmez.

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
_[60 saniyelik açıklayıcı CLI demosu](demo/CLI_Demo_60s.mp4). Bu video gerçek CLI çıktılarından üretilmiştir; ekran kaydı değildir._

## Atıf
Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods, 39*, 175–191.

Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G. (2009). Statistical power analyses using G*Power 3.1: Tests for correlation and regression analyses. *Behavior Research Methods, 41*, 1149–1160.
