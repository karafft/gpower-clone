# Sude için hazır doğrulama iş akışı

Bu belge bir gözlem raporu değildir. G*Power veya ikili dosya üzerinde yeni deney yapılmamıştır. Gerçek dosyalar kullanıcıdan bekleniyor. Ekip protokolündeki [REA] ile [ORC] ayrımı korunur.

## Hazır olan araç

Paket kurulduktan sonra:

```powershell
python tests/test_differential.py public_vectors.jsonl --report tests/reports/public_cli.json
python tests/test_differential.py oracle/validation/vectors.jsonl --require-evidence --report tests/reports/heldout_cli.json
```

Araç CLI'yi her vektör için ayrı süreçte çağırır; varsayılan zaman sınırı 2 saniyedir. Tam sayı türünü ve değerini kesin, ondalıkları mutlak veya göreli 1e-6 ile karşılaştırır. Girdi, beklenen/gerçek sonuç, her fark, süre, çıkış kodu, kaynak kod ve vektör SHA-256 değerlerini rapora yazar. Sayısal karşılaştırma yalnızca t2-indep ailesi içindir; diğer aileler atlanır. Diğer ailelerde UNSUPPORTED eşdeğerliği MCP parity testinin konusudur.

Vektör biçimi her satırda `id`, `input`, `expected` ve gerçek kaynağa bağlı `evidence` alanlarını taşıyan JSON nesnesidir. `expected` motor tarafından üretilmez. Hata beklenen kayıtta `expected.error` bulunur; isteğe bağlı `code` ve `field` de karşılaştırılır. Hata açıklamasının kelimesi kelimesine eşleşmesi aranmaz.

Raporun N oranı yalnızca N alanı bulunan a-priori kayıtları üzerinden hesaplanır. Bu oran yalnızca sağlanan set içindir; yarışma gizli setinin sonucu değildir. Evidence kimliği varlığını kontrol etmek, kanıtın gerçekliğini doğrulamaz; görsel ve kaynak incelemesi ayrıca yapılır.

## İnceleme için deney matrisi

1. Eşit oran: tek/çift kuyruk, birkaç d/alpha/power birleşimi.
2. Eşit olmayan oran: 0.5, 0.3, 1.3, 1.7, 2; özellikle n1*ratio tam sayı sınırının iki yanı. Ceil ile sürekli çözümü sonradan yuvarlama olasılıklarını ayırt et.
3. N artış eşiği: hedef gücü komşu N değerlerinin ulaştığı güçlerin çevresinde değiştir.
4. Örneklem alt sınırı: n1/n2=2, çok büyük d; küçük oranla n2<2 adayları.
5. Aralık içinde uyuşmazlık: power<=alpha ve uç fakat sonlu değerler.
6. Ters modlar: aynı N ile post-hoc, criterion, sensitivity; tek/çift kuyruk.
7. Ayrı saklı set: geliştirme kurallarını yazmak için kullanılan örneklerden farklı girdiler.

Her deneyde sürüm, girişler, tüm çıkışlar, ekran görüntüsü ve sorgulanan hipotez kaydedilir. Bu liste yapılmış 30 deney değildir. Statsmodels ölçek çalışması da G*Power doğrulaması yerine geçmez. Binary incelemede yalnızca izin verilen kısa adres/dize kanıtları tutulur; decompile çıktısı teslim edilmez.

## Henüz kesinleşmeyen davranış

ceil tahsisi; n1/n2>=2; monoton N araması; MAX_N1=10.000.000 ve ters çözüm sınırı 1.000.000; power<=alpha reddi. Bunlar mevcut uygulamanın SPEC veya geçici CLI kararlarıdır. G*Power davranışı olarak etiketlenmeleri için kanıt gerekir.
