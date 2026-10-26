> **Son denetim:** ORC-011 yeniden G*Power’da çalıştırıldı;96+48=144 sonucu ve yeni görsel oracle/replays altında. Eski eksik PNG korunur. Yeni tamamlanmış58/58 set ve38/38 N raporu REPORT.md içinde; toplam75 görsel. Aşağıdaki inceleme ilk60 dosyayı anlatır.

# Sude’nin gönderdiği 60 ekran görüntüsünün kontrolü

26 Ekim2026: screenshots.zip içindeki ORC-001–060 adlı60 özgün PNG
yerel pakete alındı. Görseller değiştirilmedi. ZIP ve her görselin SHA-256
değeri oracle/sude_screenshots/manifest.json içinde kayıtlıdır. Dosya adları,
görünen girdiler ve çıktılar Word protokolüyle görsel olarak karşılaştırıldı.
Bu ilişkilendirme dosyaların çekildiği cihazın veya executable hash’inin
adli doğrulaması değildir. Görsellerde G*Power3.1.9.7 görünür.

**59 görüntüde sonuç veya hata penceresi protokolü destekliyor. ORC-011’de
girdiler görünür, ancak tüm çıktı alanları ? durumundadır.** Bu görseldeki
96/48/toplam144 sonucunun doğrulandığı söylenemez. Word’den alınmış eski
beklenen değerler değiştirilmedi; bu kayıt görselle desteklenen koşumdan
çıkarıldı. Sonuçları görünür yeni bir ORC-011 görüntüsü isteğe bağlı olarak
tamamlanabilir; mevcut57 kayıtla30+ görsel hedefi zaten karşılanıyor.

ORC-050 negatif d ve ORC-059 kesirli n1 ile gerçek GUI başarısını gösteriyor;
hocanın CONTRACT’ı bu girdileri reddettiği için CLI eşdeğerlik paydasına
alınmadılar. Hata penceresi olan11 kayıt yalnız hata varlığı bakımından
karşılaştırılır. Görselle desteklenen57 CLI kaydı (46 sayısal+11 hata),
a-priori37 N hesabı içerir. Rapor ayrıca kaydedilir; daha önceki58/58 ve38/38
sonuçları Word protokolüne dayalı regresyon sonucu olarak geçerlidir.

[REA-SUDE-001] ORC-038/039: hedef güç .8014→.8015 değişince toplam N128→130;
ORC-040/041: .9514→.9515 değişince176→178. Çift toplam adımları doğrudan görünür.
[REA-SUDE-002] ORC-046/048: hedef güç alpha=.05 ile eşitken GUI hata vermiyor,
her iki yönde2+2 kişi veriyor; ORC-047 daha küçük güçte hata gösteriyor.
[REA-SUDE-003] ORC-050 ve059 sözleşmenin GUI davranışından ayrıldığı somut
örneklerdir. Klonun sözleşmeyi izlemesi açıkça belgelendi.

Bu60 dosya ile önceki14 yeni deneyin toplamı74 görseldir;74 bağımsız başarılı
test iddiası değildir. Canlı model ve gerçek token karşılaştırması hâlâ
API/model ayarı bekler. GitHub’a yükleme yapılmadı.
