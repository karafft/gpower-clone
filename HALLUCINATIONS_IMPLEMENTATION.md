# Gerçek düzeltmeler ve kapsam sınırları

Bu kayıtlar bu koordinasyon/uygulama çalışmasına aittir; Sude veya Zeliha tarafından ayrı oturumlarda yapılmış gibi sunulmaz. Hayali hata veya kanıt eklenmez.

1. **Arayüz deneyi ile REA etiketi karıştırıldı.** İlk koordinasyon önerisinde ekran görüntülü deneyler [REA] diye adlandırılmıştı. Ekip protokolü okununca [REA] ikili inceleme, [ORC] arayüz gözlemi olarak ayrıldı. Bu hatayı kod testi değil belge karşılaştırması yakaladı. LEDGER şablonu ve doğrulama belgeleri ayrımı koruyor.
2. **Şartnamenin toleransı yeterli sanılabilirdi.** SPEC 1e-4, CONTRACT 1e-6 diyordu. Sözleşme karşılaştırması farkı ortaya çıkardı; testlerde mutlak veya göreli 1e-6 uygulanıyor. Orijinal SPEC onaysız değiştirilmedi.
3. **Dosya düzeni ekip planıyla uyuşmuyordu.** İlk paket kök gpower_clone altında hazırlanmıştı. Ekip planı kontrolünden sonra src/gpower_clone/engine düzenine taşındı; test ve paket kurulum kontrolü tekrarlandı.

N'nin gizli vektörlerde %90 eşleştiği, REA kanıtının tamamlandığı veya gerçek LLM ajan değerlendirmesinin geçtiği iddia edilmez. Bunlar ayrı doğrulama gerektirir.

## Yeni veriyle ortaya çıkan hatalı varsayımlar

4. İlk SPEC'teki n2=ceil(n1*ratio) ve en küçük n1 araması doğru G*Power
   davranışı gibi uygulanmıştı. ORC-033'te 57/73 kaydı ceil(57*1.3)=75 ile
   çelişti. Sude setinde önce N eşleşmesi28/38 idi. Yeni genel çift-toplam
   tahsis adayı bu geliştirme kayıtlarıyla yeniden sınandı. Bu eski hatayı
   düzeltti; fakat aynı veriye uyum bağımsız doğrulama sayılmaz.
5. İlk uygulamada power<=alpha reddediliyordu. ORC-046/048 eşitlikte sonuç
   verdi; ayrıca REA-STATIC-001 metin/kod referansı eşitliği ayırdı. A-priori
   koşulu power<alpha olarak düzeltildi. Tüm modlara kanıtsız genellenmedi.
6. İlk örnek testleri geçtiği için sayısal kuyrukların her durumda sonlu
   olacağı varsayımı yetersizdi. ORC-023, küçük alpha için NO_SOLUTION
   üretti. Sağ/sol kuyruk için matematiksel eşdeğer fallback'ler ve gerçek
   regresyon testleri eklendi.

7. Minimal-even-power kuralı38 örneğe uysa da binary sürekli çözüm sonrası yuvarlama yolunu gösterdi; genel algoritma bu nedenle tekrar düzeltildi. Kayıtları tutturmak tek başına doğru söküm kanıtı değildi.
8. Ajan değerlendirmesinde null oracle değerlerinin başarı sayılma/çökme riski düzeltildi; bilinmeyen metrik artık null ve ayrı payda ile raporlanıyor.
