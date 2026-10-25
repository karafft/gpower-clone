# Oturum 1: İnceleme, SPEC.md ve doğrulama (Sude)

Üç kişilik bir G*Power tersine mühendislik projesinde inceleme, SPEC.md ve bağımsız doğrulama sorumlusuyum. Merve ayrı bir AI oturumunda yalnızca SPEC.md ve CONTRACT.md ile motoru ve CLI'yi yazacak. Zeliha repo, MCP sunucusu ve ajanla ilgileniyor. Bu oturum uygulama kodu yazmaz.

## Kapsam
- G*Power 3.1.9.7 (Windows), yalnızca resmi sayfadan (psychologie.hhu.de) indirilmiş kopya
- Test ailesi: t testi, iki bağımsız ortalama (Means: Difference between two independent means, two groups). CLI kimliği `t2-indep`.
- Modlar: a-priori ve post-hoc. Compromise, criterion ve sensitivity ancak ben istersem.
- Sözleşme: CONTRACT.md (gpower-clone v1.0.0) ve public_vectors.jsonl. Bunları sana vereceğim.

## Başlamadan önce
1. GPower.exe dosyasının SHA-256 hash'ini almamı sağla.
2. "About" ekranının görüntüsünü kaydettir.
3. "REA araçları ve Ghidra sağlayıcısı bu oturumda kullanılabilir mi?" sorusuna cevap ver; bu cevabın ekran görüntüsü README'ye girecek.
4. REA'yı yalnızca github.com/morluto/rea, rea.tools ve npm'deki rea-agents paketinden kullanıyoruz.

## Kanıt etiketleri
Puan yalnızca binary'den kanıtlanan bulgulara veriliyor. Etiketleri birbirine karıştırma.

- **[REA-xxx]:** GPower.exe içinde REA veya Ghidra ile bulunan fonksiyon adresi, dize referansı, sabit ya da kontrol akışı. Kısa alıntı ve adres yeterli; decompile edilmiş kod bloğu kaydedilmez.
- **[ORC-xxx]:** Arayüzde yapılan deney. Bu bir gözlemdir; binary kanıtı değildir.
- **[DOK-xxx]:** Kılavuz veya makale (sayfa ve bölümle).
- **[AJAN-xxx]:** Senin çıkarımın. Kanıtı yoksa bu etiketi alır ve test edilmesi gereken bir hipotez olarak kalır.
- **[VAL-xxx]:** Gizli doğrulama vektörü.

İdeal akış: arayüzde bir davranış gözlenir (ORC), binary'de onu üreten yer bulunur (REA), ve REA kaydı ilgili ORC kayıtlarına bağlanır.

Kendinden emin bir açıklama yaptığında sana "Bunun kanıtı hangi fonksiyonda?" diye soracağım. Cevap veremiyorsan o iddia [AJAN] olarak kalır.

## 1. Deney planı
Önce deneyleri tasarla. Her deney iki ya da daha fazla rakip hipotezi birbirinden ayırt etmeli. Her deney için şunları yaz: kimlik, ayırt ettiği hipotezler, girdiler, her hipotezin öngördüğü sonuç ve hangi sonucun neyi çürüteceği.

Araştırılacak sorular (kılavuzda olmayan davranışlar):
- **Yuvarlama:** Kesirli N yukarı mı yuvarlanıyor, yoksa tam sayılar üzerinde artırarak mı aranıyor?
- **Grup dağılımı:** N2/N1 oranı 1 değilken n1 ve n2 nasıl bulunuyor? Hangi grup yuvarlanıyor; toplam mı, gruplar ayrı ayrı mı? Oran küsuratlı olduğunda ne oluyor?
- **Eşikler:** d, α veya güç çok az değiştiğinde N'nin bir arttığı noktaların hemen altı ve hemen üstü.
- **Durma koşulu:** Güç hedefi tam tutturulduğunda o N mi seçiliyor, bir fazlası mı (≥ mi, > mi)? Başlangıç N'si, adım, en fazla iterasyon sayısı.
- **Formüller:** df, kritik t, ncp ve "Actual power" hesabı. Tek ve çift yönlü testte farklar.
- **Sınır değerler:** çok küçük ve çok büyük d, güç α'ya eşit veya ondan küçük, α ve güç için uç değerler, çok büyük ve çok küçük oranlar.
- **Geçersiz girdiler:** negatif, sıfır, boş, aralık dışı değerler. G*Power hata mı veriyor, alanı mı düzeltiyor, sessizce mi hesaplıyor? Hata mesajının metni de kayda girer.

Binary'de başlangıç noktası olarak arayüzde görünen dizeleri ("Noncentrality parameter", "Critical t", "Actual power", "Sample size group 1" vb.) ve hata mesajlarını kullan. Bu dizelere referans veren fonksiyonları izle.

## 2. Deneyleri yürütme
- Arayüze erişemiyorsan hangi menüden hangi testi seçeceğimi, hangi alana ne gireceğimi ve hangi düğmeye basacağımı adım adım söyle. Sonra benim gerçek sonuçlarımı bekle. Sonuç tahmin etme ve uydurma.
- Deneyleri tek tek yürüt. Bir deneyin kaydı tamamlanmadan sonrakine geçme.
- Tek örnekten genel kural çıkarma. Bir kural ancak bir REA bulgusuyla ve birden fazla ORC deneyiyle desteklendiğinde "doğrulandı" sayılır.
- Hedef: ekran görüntüsüyle en az 30 ORC vektörü, sınır değerler ve geçersiz girdiler dahil.

### Kâhin deneyi formatı
```
### [ORC-001] <kısa başlık>
- Tarih:
- Araştırılan soru:
- Menü yolu: t tests → Means: Difference between two independent means (two groups)
- Mod:
- Seçili seçenekler: tails, allocation ratio N2/N1
- Girdiler: (bütün alanlar, görüldüğü gibi)
- Görünen çıktılar: (bütün alanlar, ekrandaki basamak sayısıyla)
- Ekran görüntüsü: oracle/screenshots/ORC-001.png
- Gözlem: (yalnızca görülen)
- Yorum: (olası açıklama; doğrulanmadıysa öyle işaretle)
- İlgili kayıtlar:
```

### Binary bulgusu formatı
```
### [REA-001] <kısa başlık>
- Araştırılan soru:
- Araç ve sürüm: REA / Ghidra
- Konum: fonksiyon adresi, dize referansı
- Kısa alıntı: (birkaç satır; decompile bloğu değil)
- Gözlem:
- Yorum:
- Destekleyen deneyler: [ORC-...]
- Durum: doğrulandı / kısmen / hipotez
```

## 3. Ölçek vektörleri
Python statsmodels ile 500'den fazla vektör üretilecek (`oracle/scale/`). Bu kütüphane N'yi kesirli verir, G*Power tam sayı gösterir. Bu farkı SPEC'te ayrı bir bulgu olarak açıkla. Kütüphane sonuçları G*Power'ın yerine geçmez; asıl kâhin G*Power'dır.

## 4. SPEC.md
Merve yalnızca SPEC.md ve CONTRACT.md'yi görecek. SPEC, başka bir kaynağa ihtiyaç duymadan uygulanabilir olmalı. İçermesi gerekenler:

1. **Kapsam:** aile, modlar, kapsam dışı olanlar (diğer aileler `UNSUPPORTED`)
2. **CLI sözleşmesi:** CONTRACT.md'deki t2-indep kuralları
   - her mod için zorunlu ve yasak alanlar
   - varsayılan değer olmaması, `.` ondalık ayırıcı
   - çıktı alanları ve tipleri
   - hata formatı, hata kodları, çıkış kodları
3. **Hesaplama kuralları:** df, kritik t, ncp, actual power
4. **Örneklem araması:** başlangıç, adım, durma koşulu, iterasyon sınırı, çözüm bulunamazsa ne olacağı
5. **Yuvarlama ve n1/n2 dağılımı**
6. **Hata davranışları:** hangi girdinin hangi hata koduna gittiği
7. **Kabul kriterleri:** Gherkin formatında (Given / When / Then), geliştirme setinden somut sayılarla
8. **Geliştirme örnekleri:** girdiler ve G*Power'dan gözlenen çıktılar
9. **Toleranslar:** N, n1 ve n2 tam eşleşir; diğer değerler 1e-6 mutlak veya göreli
10. **Kütüphane kuralı:** scipy yalnızca dağılım fonksiyonları için kullanılır; N araması, yuvarlama ve df hesabı ekibin kendi kodudur

Her kuralı şu üç türden biri olarak işaretle:
- **[Doğrulandı]:** G*Power davranışı; [REA-...] ve [ORC-...] kayıtlarına bağlı
- **[Varsayım]:** Kanıtı yetersiz; neden kabul edildiği yazılı
- **[CLI kararı]:** G*Power'da karşılığı yok; sözleşmeden ya da bizim tasarımımızdan geliyor

SPEC.md'ye decompile edilmiş kod, ham Ghidra çıktısı veya fonksiyon gövdesi konmaz. Yalnızca algoritma ve davranış anlatılır; kanıt kimlikleri referans olarak kalır.

## 5. Doğrulama seti
- Geliştirme örneklerinden ayrı bir doğrulama seti oluştur. Her kayıt [VAL-001] gibi bir kimlik ve ekran görüntüsü taşır.
- Set; tipik değerleri, sınır değerleri, eşik noktalarını, eşit olmayan oranları ve geçersiz girdileri kapsar.
- Bu setin girdileri ve sonuçları ilk değerlendirmeye kadar SPEC.md'ye, repoya veya Merve'ye aktarılmaz.

## 6. Değerlendirme
Merve sürümü git etiketiyle sabitlediğinde karşılaştırmayı yürüt:
- N, n1 ve n2 için tolerans sıfır. Diğer alanlar için 1e-6.
- Raporda şunlar olur: sürüm etiketi ve commit hash, toplam vektör sayısı, N tam eşleşme oranı, alan bazında eşleşme oranı. Her uyuşmazlık için girdi, beklenen, bulunan ve olası açıklama (bizim hatamız mı, kaçırılmış bir kural mı).
- Rapor `tests/reports/` altına konur.
- %90 tam eşleşmenin altındaysa MCP ve ajan aşamasına geçilmez.
- Bir hatayı düzeltmek için Merve'ye açılan her doğrulama vektörü artık geliştirme setine geçer. Sonraki değerlendirme için yeni vektörler ayrılır.
- Yerel doğrulama sonucunu hocanın gizli test sonucu gibi sunma.

## 7. Ajan değerlendirme seti için
Zeliha 10 kurgusal Türkçe klinik soru hazırlayacak. Bu soruların G*Power'daki beklenen N değerlerini arayüzden alıp ekran görüntüsüyle kaydet.

## Ayrıca tutulacak kayıtlar
- **HALLUCINATIONS.md:** Yanlış çıkardığın her şey: ne iddia edildi, nasıl fark edildi, hangi deney ya da bulgu onu çürüttü. En az 2 kayıt gerekiyor.
- **AGENT_COST.md:** Yaklaşık token kullanımı, iterasyon sayısı, zaman alan adımlar, neyi farklı yapardık.

## Kurallar
- GPower.exe ve decompile çıktısı repoya girmez.
- Hesap motoru yazma.

İlk olarak kurulum kanıtlarını alalım, sonra deney planını hazırlayalım.
