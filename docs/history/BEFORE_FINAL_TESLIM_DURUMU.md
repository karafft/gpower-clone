> **YAYIN GÜNCELLEMESİ — 26 Ekim2026:** Kullanıcının talebiyle kaynaklar ve kanıtlar repoya eklendi. Aşağıdaki yüklenmedi/onay bekliyor notları yerel hazırlık aşamasının tarihsel kaydıdır.

> **GÜNCEL — 26 Ekim, ekran görüntüleri alındı:** Sude’nin60 PNG’si
> pakete eklendi ve kayıtlarla karşılaştırıldı.59 görüntüde sonuç/hata mevcut;
> ORC-011’in çıktıları ? olduğu için bu görsel sayısal sonucu kanıtlamıyor.
> Görselle desteklenen, sözleşmeye uygun57/57 kayıt ve37/37 N hesabı eşleşti.
> Önceki14 yeni GUI deneyiyle toplam74 görsel var;30+ görsel hedefi karşılandı.
> Aşağıdaki “görseller gelmedi/30 görsel eksik” ifadeleri önceki aşamaya aittir.
> Ayrıntı: docs/SUDE_GORSEL_KONTROLU.md. Canlı ajan/token ölçümü hâlâ bekliyor.

# Ekip incelemesine hazır paket

26 Ekim 2026 · sürüm **1.1.0rc4** · CONTRACT **1.0.0**.
**GitHub'a yükleme, commit veya etiket yapılmadı.** Bu paket ekip onayına sunuluyor.

## Tamamlananlar

1. Beş t2-indep modu için tek hesap motoru, girdi doğrulama ve JSON CLI.
2. Önceki grup tahsisi, eşitlik ve sayısal kuyruk hatalarının düzeltilmesi.
   Şartname önerisi SPEC_ONERI.md ve gerçek binary adresleriyle kanıt bağlantısı.
3. Gerçek stdio MCP sunucusu; yalnız power_analysis aracı ve aynı motor.
4. Gerçek API sağlayıcısına bağlanıp MCP üzerinden hesap yapan ajan kodu,
   çağrı kayıt sistemi ve on soruluk canlı değerlendirme aracı. API'siz
   çalıştırmada sahte başarı yerine not_run/null üretir.
5. **25/25 otomatik yazılım testi**; hata veya atlanan test yok.
6. Gerçek MCP bağlantısında **33/33 CLI metin eşdeğerliği**:25 açık ve8 hatalı girdi.
7. Sude'nin60 kaydının tamamının incelenmesi. Sözleşmeyle uyumlu58 kaydın
   **58'i**, N içeren38 kaydın **38'i** eşleşti. Negatif d ve kesirli n1
   içeren iki GUI başarı kaydı ayrıca saklandı; CLI'nin sözleşme gereği
   reddi de gerçek komutlarla doğrulandı. Bunlar60/60 GUI eşleşmesi diye sunulmaz.
8. Son motorla **540/540 statsmodels karşılaştırması**. Aynı tam sayı tahsisinde
   en büyük güç farkı 5.55e-16. Bu kütüphane kontrolü
   yeni G*Power gözlemi değildir ve ortak SciPy altyapısından bağımsız bir kanıt sayılmaz.
9. Resmî3.1.9.7 binary örneğinde yedi gerçek dize/kod referansı; ayrıca
   sürekli çözüm,10 ondalık ön yuvarlama, çift toplam ve grup tahsisi yolları.
   Sürüm, SHA-256, RVA, dosya offset'i ve tekrar üretme aracı pakette.
10. Gerçek CLI çıktılarından60 saniyelik açıklayıcı MP4; terminal veya G*Power
    ekran kaydı değildir. Özgün komut/çıktı kayıtları demo/cli_transcript.json altında.
11. Kabul senaryoları, farklılaştırılmış kaynak veriler, karşılaştırma raporları,
    kaynak hash'leri, gerçek hata/düzeltme defteri, maliyet sınırları ve kurulum.
12. Son paket kuruldu; dört Python modül yolu ve Windows metin başlatıcısı
    doğrulandı. Bu bilgisayar yeni pip exe başlatıcısını WinError4551 ile
    engelledi; güvenlik ayarı değiştirilmedi. Çalışan alternatif belgelendi.

## Ölçülmeden tamamlandı denmeyenler

- **Canlı LLM değerlendirmesi ve GUI/MCP token karşılaştırması:** bu ortamda
  API anahtarı/model ayarı yok. Kod ve ölçüm aracı hazır; gerçek çağrı sayısı0.
  Mock test sonucu modelin Türkçe soruları doğru anladığının kanıtı değildir.
- **Özgün ekran görüntüleri:** Sude ayrı klasörde bulunduğunu bildirdi;
  klasör bu çalışmada paylaşılmadı. Word dosyasında gömülü görsel yok.
  Sıfırdan60 görüntü üretilmiş gibi davranılmadı.
- **Gizli kapı:** Yeni GUI takip seti aşağıda raporlandı; yarışmanın gizli%90
  kapısının sonucu hâlâ bilinmiyor.
- **Tam sayısal çözücü eşdeğerliği:** statik yollar çözüldü; her kök bulma
  ayrıntısında bit düzeyinde eşitlik veya tüm olası girdilerde doğruluk iddiası yok.

## Hoca yönergesiyle ilişki

| Kaynak | Gereklilik | Durum |
|---|---|---|
| Sprint metni | Tek test ailesi, tek motor, CLI | Hazır |
| Sprint metni | İki ayrı inceleme/yazım oturumu | Motor ayrı temiz oturumda; kaydı var |
| Sprint metni | REA etiketli gerçek kanıt, binary/decompile teslim etmeme | Adres ve kısa bulgu var; orijinal binary/decompile yok |
| CONTRACT | JSON alanları, türler, hata ve sürüm | Otomatik test ve gerçek CLI çıktıları var |
| CONTRACT |2 saniyelik çağrı hedefi | Son58 ayrı süreçte en yavaş 1.224s; tüm makinelere garanti değil |
| Sprint/CONTRACT | Gizli vektörlerde%90 N kapısı | Dış değerlendirme; henüz sonucu bilinmiyor |
| Bonus | MCP | Kod ve gerçek protokol eşdeğerliği hazır |
| Bonus | Doğal dil ajanı | Kod hazır; canlı sağlayıcı koşumu eksik |
| Ekip planı |500+ ölçek, belgeler ve demo |540 kayıt, belgeler ve açıklayıcı video hazır |
| Ekip planı |30+ özgün görüntü, yeni saklı VAL, GUI/MCP token kıyası | Kaynak/çalıştırma bekliyor |

## Ekipten istenen onay

Sude: kaynak kayıtların doğruluğu, varsa özgün görsellerin bağlantısı ve
SPEC_ONERI.md değişiklikleri. Zeliha: MCP/ajan kurulumu, canlı model tercihi
ve mevcut repo belgeleriyle birleştirme. Merve: onaylar ve kalan gerçek
ölçümlerden sonra kaynakların repoya alınması. Herkes yalnız gerçekten
üstlendiği katkıyı beyan etmeli; ek kodlar bu AI çalışma oturumunda üretildi.


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
