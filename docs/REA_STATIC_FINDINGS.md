# Gerçek statik binary incelemesi

26 Ekim 2026. Kaynak HHU resmî indirmesi:
https://www.psychologie.hhu.de/fileadmin/redaktion/Fakultaeten/Mathematisch-Naturwissenschaftliche_Fakultaet/Psychologie/AAP/gpower/GPowerWin_3.1.9.7.zip

Dosya GPowerNT.exe; dosya ve ürün sürümü 3.1.9.7; boyut 2.287.616 bayt.
SHA-256: c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812.
PE32 x86, tercih edilen image base 0x400000. ASLR çalışma anındaki adresleri
değiştirebilir; RVA ve dosya offset'leri bu hash için yeniden üretilebilirdir.

Yöntem: PE başlığı/section okuması ve Capstone statik instruction referansları.
Program çalıştırılmadı; Ghidra veya özel ders REA uygulaması kullanıldığı
iddia edilmiyor. Buradaki [REA] kayıtları gerçek binary adres/dize bulgularıdır;
özel bir araç kullanma şartı varsa araç uygunluğu ayrıca teyit edilmelidir.
Decompile çıktısı ve orijinal executable teslim paketinde yoktur.

## [REA-STATIC-001] Eşitlik hata metninde açıkça ayrılıyor

Dize VA 0x5c6220, RVA 0x1c6220, dosya offset 0x1c5220.
Kısa alıntı: “greater than or equal to alpha”. Kod referansı 0x4880f9.
0x4880e0 başlangıcındaki kısa karşılaştırıcıda 0x4880ec'de strictly-below
dalı hata yoluna, diğer yol 0x4880ee'de başarıya gidiyor.

Sınırlandırılmış çıkarım: bu karşılaştırıcı eşitliği sırf eşit olduğu için
reddetmiyor. Argümanların anlamsal eşlemesi hata metni ve ORC-046/048 ile
destekleniyor. Bu, tüm analiz modlarının tüm çağrı yolları için tek başına
kontrol akışı kanıtı değildir.

## [REA-STATIC-002] Oran aralığı için ayrı doğrulama yolu

Dize VA 0x5c679c, dosya offset 0x1c579c; kod referansı 0x487394.
Kısa alıntı: “allocation ratio falls outside”. Bu kayıt oran doğrulama
mesajının binary'de bulunduğunu ve koddan referanslandığını doğrular.
Aralığın uçlarının kapsanıp kapsanmadığı bu kayıttan çıkarılmaz.

## [REA-STATIC-003] A-priori etki alt sınırı

Hata dizesi VA 0x5cb24c; bağımsız iki grup nesnesinin doğrulama yolundaki
referans 0x4d9292. İlgili kısa doğrulayıcı başlangıcı 0x4d9260.
0x5c7ed8 adresindeki little-endian double değeri **0.00001**.
0x4d927a mutlak değer maskesinden sonra 0x4d9281 karşılaştırma yapılıyor;
0x4d9285'te threshold<=abs(effect) koşulu kabul yoluna gidiyor.

Aynı nesne tablosu VA 0x5ca40c, +0x104 slotunda 0x4d9260'a, +0x78 slotunda
0x4d9a00'a işaret ediyor. İkincisi t2-indep etiketini kuran yol: etiket
dizesi VA 0x5cb418 ve yükleme referansı 0x4d9a3a.

Sınırlandırılmış çıkarım: bu test nesnesindeki a-priori etki doğrulama
yolunda **abs(d)>=1e-5** kabul karşılaştırması var. Hata metnindeki “greater
than” ifadesinden farklı olarak equality kabul dalı görülüyor. Mod/alan
eşlemesinin dinamik GUI sınır deneyiyle de teyit edilmesi değerlidir.

## Diğer dize referansları

- [REA-STATIC-004]: t2-indep etiket yolu 0x4d9a3a -> dize 0x5cb418.
- [REA-STATIC-005]: alpha aralık hata yolu 0x4874ec ve 0x4875b4 -> 0x5c6100.
- [REA-STATIC-006]: toplam N aralık hata yolu 0x488a3c -> 0x5c6524.
- [REA-STATIC-007]: power aralık hata yolu 0x48809c -> 0x5c60d8.

## [REA-STATIC-005/007] Sayısal alan sınırları ve uçların kabulü

Alpha doğrulayıcısı0x487460, power doğrulayıcısı0x488010. Alt sabit VA
0x5c4398'de double1e-7, üst sabit0x5c6860'da0.9999999. Strict-below/above
dalları dışarıdaki değerleri reddediyor, uçlar kabul yolunda. Böylece
aralık mesajındaki parantezleri açık aralık diye yorumlamak yanlış olur.

## [REA-STATIC-002] Oran sınırları

t2-indep yolunda0x4d9c1a,0x5c3b50'deki double0.01'i yükleyip0x4d9c3c'de
0x487300 doğrulayıcısına iletiyor. Bu işlev üst sınırı alt sınırın tersiyle
hesaplıyor ve strict-below/above ile reddediyor: **0.01<=ratio<=100**.

## [REA-STATIC-008] Sürekli çözümden sonra çift toplam yuvarlama

t2-indep nesne tablosu0x5ca40c +0x48 ->0x496aa0 çözüm yolunu, +0x74
->0x4d64c0 yuvarlama yolunu bağlıyor.0x496b03'te sayısal çözücü0x4f9bb0
çağrısı var; aynı çağrı hazırlığında0x496aed'de300 ve0x5c3f48'den1e-10
aktarılıyor. Burada300'ün tam durma koşuluna etkisi ayrıca izlenmedi.
0x496b30'da çözüm sonucuna yuvarlama sanal işlevi uygulanıyor.

0x4d64c0 yolunda x önce0.5 ile çarpılıyor,0x496a20'ye veriliyor ve sonuç
ikiyle çarpılıyor. Yardımcı0x496a20,0x5c4328'deki1e10 ölçeğini kullanıyor:
floor(q*1e10+0.5)/1e10 ve ardından ceil. floor ve ceil adları PE import
tablosundan doğrulandı:0x5ac023 ->floor,0x5ac047 ->ceil. Sonuç:
**N=2*ceil(floor((x/2)*1e10+0.5)/1e10)**.

Bu, önceki "yuvarlanmış gruplarda en küçük gücü sağlayan çift N" hipotezinden
farklıdır. Sürekli çözüm alınır ve sonra yuvarlanır; ORC setindeki uyum tek
başına iki yöntemi ayırt etmemişti.540 bağımsız matematik karşılaştırmasında
bu iki semantik45 tahsiste farklı aday üretti; bunlar yeni GUI gözlemi değildir.

## [REA-STATIC-009] Grup tahsisi ve yakın eşit oran düzeltmesi

0x4d9d49, N/(1+ratio) oranını kuruyor.0x4d9d55'te0x5727d0'a digits0
parametresiyle gidiliyor. Bu yardımcı0x5727fa'da0.5 ekleyip floor çağırıyor:
**n1=floor(N/(1+ratio)+0.5)**.0x4d9d6f'de N-n1 kurulur,0x4d9d88'de ceil
uygulanır ve0x4d9dca'da ikinci grup alanına yazılır.

0x4d9dd2–0x4d9e03 aralığında1e-8 toleransıyla ratio'nun1'e yakınlığı ve
grupların farklılığı kontrol edilir; koşulda küçük grup yalnız bir kez1
artırılır.0x4d9e3c'de nihai gruplarla güç hesaplanır,0x4d9e4c'de dönüş
görülür. Bu yol ayrıca "actual_power hedefin altında kalırsa yeniden N ara"
optimizasyonu eklemiyor. Yakın eşit oran düzeltmesi ve tie uçları için
dinamik GUI gözlemi ayrıca değerlidir.

Makinece okunabilir yedi dize/xref kaydı ve hash'e bağlı yapısal anchor'lar
oracle/binary_evidence.json altında. Bunlar tüm sayısal çözücünün her durma
ayrıntısının veya çalışma zamanındaki bütün çağrıların çözülmesi değildir.
Adreslerin anlamı yukarıdaki sınırlı statik yollarla ve kaynak ORC kayıtlarıyla
ilişkilidir. Raw assembly dump veya decompile edilmiş C/C++ teslim edilmez.

## Yeniden üretim

```powershell
python -m pip install 'capstone>=5,<6'
python tools/collect_pe_evidence.py 'yerel\GPowerNT.exe' --output oracle/binary_evidence.json
```

Executable yalnız kullanıcıdaki inceleme klasöründe tutulur. Dağıtım ZIP'i,
GPowerNT.exe ve üçüncü taraf executable'lar teslim veya repoya eklenmez.
Kaynak koşulları: https://www.psychologie.hhu.de/en/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower
