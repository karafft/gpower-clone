# Son dosya ve teslim denetimi

26 Ekim2026. Kapsam: takip edilen dosyalar, hesap testleri, MCP protokolü,
kanıt bağlantıları ve güncel ana belgeler. Sonradan kaynaklara bakıldığı için
temiz oda geçmişi yeniden icat edilmedi; özgün oturum kaydı korunur.

Düzeltmeler:

1. agent.py içindeki Türkçe yönergeler bozuk kodlamadan UTF-8’e dönüştürüldü.
   Yapılandırılmış yanıtta action alanı artık tutarlı ask_user ister.
2. SPEC.md’deki eski ceil oranı/minimum n1 algoritması kanıtlı sürekli
   çözüm+tahsis kuralıyla değiştirildi. Orijinal Sude belgesi arşivlendi.
3. ORC-011 G*Power3.1.9.7’de tekrarlandı; çıktı ve özgün JPEG ayrı kaydedildi.
   Önceki60 PNG ve14 yeni deney değişmeden korundu. Toplam75 görüntü.
4. Eski/çelişkili ana durum sayfaları güncellendi; önceki sürümleri
   docs/history altında saklandı. Tarihsel raporlar yeni koşum sanılmamalı.
5. check_all.py görselle desteklenen seti, yeni GUI setini ve dosya denetimini
   de çalıştırır. audit_files.py tüm takip edilen dosyaları denetler.

Canlı model koşumu engeli: GPOWER_API_KEY/OPENAI_API_KEY ve GPOWER_MODEL
tanımlı değil. Gizli anahtar aramak için kişisel dosyalar taranmadı.
logs/final_live_status.json gerçek not_run kaydını içerir. Yerelde ayarlar
tanımlandıktan sonra README_IMPLEMENTATION.md içindeki değerlendirme komutu
çalıştırılır. Aynı soruların GUI ajanı üzerinden gerçek kayıtları da alınmadan
GUI/MCP token kazancı veya ücret hesaplanamaz. Otomatik test başarısı canlı
model sonucu değildir. Bu bölümün eksikliği gizlenmedi.

Kalan insan adımı: ekip katkılarını ve güncellenmiş şartnameyi inceleyip son
teslimi yapmak. Gizli%90 N kapısı yalnız hocanın değerlendirmesiyle bilinir.

6. ground_truth.json aslında JSONL içeriyordu; aynı kayıtlar geçerli JSON dizisine
   dönüştürüldü. İlk dosya docs/history/ground_truth_original.jsonl içinde korunur.

## Canlı deneme bağlantı düzeltmesi

Kullanıcı ilk gerçek denemeyi çalıştırdı;10/10 kayıt ExceptionGroup ile
sonuçlandı, tamamlanan model yanıtı yok. Bu sonuç model doğruluğu%0 diye
yorumlanamaz. Anahtarsız tanı denemesinde Python varsayılan istemcisiyle
HTTP403/1010, uygulama User-Agent başlığıyla beklenen HTTP401 alındı.
Standart uygulama başlığı eklendi; iç HTTP durumları sırları açmadan
raporlanır. Tamamlanmış yanıt yoksa doğruluk metrikleri artık null olur.
Gerçek anahtarla tekrar koşum hâlâ gereklidir. Sayısal motor değişmedi.
