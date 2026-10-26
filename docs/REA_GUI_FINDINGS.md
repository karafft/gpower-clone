> **GÜNCEL — 26 Ekim, ekran görüntüleri alındı:** Sude’nin60 PNG’si
> pakete eklendi ve kayıtlarla karşılaştırıldı.59 görüntüde sonuç/hata mevcut;
> ORC-011’in çıktıları ? olduğu için bu görsel sayısal sonucu kanıtlamıyor.
> Görselle desteklenen, sözleşmeye uygun57/57 kayıt ve37/37 N hesabı eşleşti.
> Önceki14 yeni GUI deneyiyle toplam74 görsel var;30+ görsel hedefi karşılandı.
> Aşağıdaki “görseller gelmedi/30 görsel eksik” ifadeleri önceki aşamaya aittir.
> Ayrıntı: docs/SUDE_GORSEL_KONTROLU.md. Canlı ajan/token ölçümü hâlâ bekliyor.

# [REA] Gerçek G*Power GUI kanıtları

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
