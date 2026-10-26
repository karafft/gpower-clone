> **YAYIN GÜNCELLEMESİ — 26 Ekim2026:** Kullanıcının talebiyle kaynaklar ve kanıtlar repoya eklendi. Aşağıdaki yüklenmedi/onay bekliyor notları yerel hazırlık aşamasının tarihsel kaydıdır.

> **GÜNCEL — 26 Ekim, ekran görüntüleri alındı:** Sude’nin60 PNG’si
> pakete eklendi ve kayıtlarla karşılaştırıldı.59 görüntüde sonuç/hata mevcut;
> ORC-011’in çıktıları ? olduğu için bu görsel sayısal sonucu kanıtlamıyor.
> Görselle desteklenen, sözleşmeye uygun57/57 kayıt ve37/37 N hesabı eşleşti.
> Önceki14 yeni GUI deneyiyle toplam74 görsel var;30+ görsel hedefi karşılandı.
> Aşağıdaki “görseller gelmedi/30 görsel eksik” ifadeleri önceki aşamaya aittir.
> Ayrıntı: docs/SUDE_GORSEL_KONTROLU.md. Canlı ajan/token ölçümü hâlâ bekliyor.

# GPower Clone ekip inceleme paketi

İki bağımsız ortalama t testi için eğitim amaçlı bağımsız uygulama.
Bu proje G*Power değildir; G*Power'ı değiştirmez veya dağıtmaz.
Sürüm1.1.0rc4, sözleşme1.0.0. Henüz GitHub'a gönderilmedi.

**Başlangıç:** [teslim durumu](TESLIM_DURUMU.md), [şartname önerisi](SPEC_ONERI.md),
[kanıt defteri](LEDGER.md), [nihai rapor](REPORT.md).

## Kurulum ve bütün kontroller

Python3.13.14 üzerinde doğrulandı. Python3.10+ ve uygun SciPy/MCP sürümü gerekir.
Proje klasöründe tek kurulum/kontrol komutu:

```powershell
python tools/check_all.py --install
```

Bu komut .venv oluşturur, resmî paket deposundan bağımlılık kurar ve yerel
testleri çalıştırır. API çağırmaz, GitHub'a yazmaz. Mevcut ortamda alternatif:

```powershell
python -m pip install '.[mcp,scale]'
python -m unittest discover -s tests -v
python tests/test_differential.py oracle/sude_contract_compatible_vectors.jsonl --require-evidence --report tests/reports/local_sude58.json
```

## CLI

```powershell
python -m gpower_clone --version
python -m gpower_clone --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.8 --ratio 1.3
```

Normal paket kurulumu gpower-clone konsol adını oluşturur. Bu bilgisayarın
Uygulama Denetimi yeni exe başlatıcısını engelledi. Güvenlik ayarını
değiştirmeden çalışan Python modülü veya proje kökündeki metin başlatıcısı:

```powershell
.\gpower-clone.cmd --version
```

Metin başlatıcısı varsa .venv Python'unu, yoksa mevcut Python'u kullanır;
aynı modülü çağırır ve çıkış kodunu korur. Başarı0, girdi hatası2, dahili hata1.
Stdout tek JSON satırıdır; sayılar elle yuvarlanmaz, N/df gerçek tam sayıdır.
Varsayılan alan yoktur; gereken her parametre açıkça verilir.

| Mod | test/mode dışında gerekenler |
|---|---|
| a-priori | tails,d,alpha,power,ratio |
| post-hoc | tails,d,alpha,n1,n2 |
| compromise | tails,d,beta_alpha_ratio,n1,n2 |
| criterion | tails,d,power,n1,n2 |
| sensitivity | tails,alpha,power,n1,n2 |

## MCP ve ajan

```powershell
python -m gpower_clone.mcp_server
python -m gpower_clone.agent --synthetic-case
```

MCP tek power_analysis aracı sunar. Hesabı ortak motor yapar.
Ajan için yerelde model ve API anahtarı gerekir; anahtar sohbet veya Git'e
yazılmaz. Sistem talimatı belirsiz etki, kuyruk ve oran için soru istemeyi
veya açıklanmış/onaylanmış varsayımı kullanmayı gerektirir. Kod gerçek
MCP çağrısı yapar; canlı model başarısı bu pakette ölçülmedi.
Kurulum ve log şeması [ajan rehberinde](docs/ZELIHA_KURULUM.md).
Canlı test opt-in komutu ve sonuçların sınırları [ajan değerlendirmesinde](eval/README.md).

## Kontrol sonucu

- 25/25 yazılım testi;33/33 gerçek MCP–CLI eşdeğerliği.
- 58/58 sözleşmeye uygun kaynak kayıt;38/38 a-priori N eşleşmesi.
- 2 GUI başarı kaydı sözleşme dışında; ayrı tutuldu ve CLI reddi doğrulandı.
- 540/540 statsmodels kontrolü; yeni G*Power verisi değildir.
- 7 gerçek binary dize/kod referansı ve ilave yuvarlama aritmetiği.

Kaynak seti geliştirmede kullanıldı; gizli kapının geçildiği iddia
edilmez. Sude’nin özgün görselleri yok; yeni14 gerçek GUI görseli pakettedir. Tarihsel başarısız ilk
koşumlar raporlarda saklandı; nihai kaynak raporu REPORT.md'de gösterilir.

## Tekrar üretim ve demo

- [Binary bulguları](docs/REA_STATIC_FINDINGS.md), [yeniden üretme aracı](tools/collect_pe_evidence.py).
- [Sude karşılaştırması](docs/SUDE_DOGRULAMA.md), [ölçek sonuçları](oracle/scale/README.md).
- [60 saniyelik CLI anlatımı](demo/CLI_Demo_60s.mp4): gerçek çıktılardan
  üretildi; ekran kaydı değildir. Kaynak komutlar demo/cli_transcript.json.
- [Temiz oda kaydı](docs/CLEAN_ROOM_PROVENANCE.md), [hata düzeltmeleri](HALLUCINATIONS.md), [maliyet kaydı](AGENT_COST.md).

## Atıf ve repo birleştirme

Faul, Erdfelder, Lang ve Buchner(2007), Behavior Research Methods39,175–191;
Faul, Erdfelder, Buchner ve Lang(2009), Behavior Research Methods41,1149–1160.
G*Power yalnız resmî HHU kaynağından indirilir. Binary, kurulum ZIP'i,
decompile çıktısı, bağımlılık klasörleri ve gerçek hasta verisi repoya girmez.
Mevcut CONTRACT.md ve Sude SPEC.md korunur; SPEC_ONERI.md ve README değişiklikleri
ekipçe onaylanarak birleştirilir. Paylaşım ZIP'inin kendisi repoya yüklenmez.


## 26 Ekim: yeni gerçek GUI doğrulaması

Motor kodu dondurulduktan sonra seçilen 14 yeni girdi G*Power 3.1.9.7
arayüzünde çalıştırıldı. Beş analiz modu kapsandı. **14/14 sonuç eşleşti;
a-priori 10/10 deneyde n1, n2 ve toplam N tam eşleşti.** Sayısal alanlar
1e-6 mutlak/bağıl toleransla, tam sayılar tam eşitlikle karşılaştırıldı.
Her deneyin özgün JPEG ekran görüntüsü, erişilebilirlik metni, girdi/çıktısı,
tarihi ve dosya hash'i oracle/new_validation altında bulunur.

[REA-GUI-001] NEW-VAL-002: d=.95, alpha=.02, hedef güç=.93, oran=.4,
çift yönlü hesapta G*Power 59/23 kişi, toplam82 ve actual_power=.9295480
verdi. Hedef gücün altında kalan bu sonuç, yuvarlama sonrasında yeniden
minimum güç optimizasyonu yapılmadığını doğrudan gösterir. Kaynak:
oracle/new_validation/screenshots/NEW-VAL-002.jpg ve NEW-VAL-002.txt.

Girdiler sonuçlar alınmadan önce kaydedildi; önceki 60 kayıtla örtüşmüyor.
Kaynak kod hash'i öncesinde ve sonrasında değişmedi. Seçimi algoritmayı bilen
koordinatör yaptı; bu kör üçüncü taraf deneyi veya hocanın gizli testi değildir.
Rapor: tests/reports/prospective_gui_validation.json. Normal kısıtlı ortamda
ilk çalıştırma zaman aşımına uğradı; yerel testin izinli tekrarında 14/14 geçti.
Bu, bütün makinelerde süre veya bütün girdilerde eşdeğerlik garantisi değildir.

Sude'nin önceki 60 kaydına ait özgün görseller hâlâ paylaşılmadı. Bu yeni
14 ekran görüntüsü onların yerine geçmiş gibi gösterilmez. Ekip planındaki
30+ özgün görüntü hedefi henüz karşılanmadı. Canlı model değerlendirmesi ve
gerçek GUI/MCP token kıyası API/model ayarı bekliyor; canlı çağrı sayısı0.
