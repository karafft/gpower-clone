# t2-indep uygulama şartnamesi

26 Ekim2026 son denetiminde kullanıcının tamamlama talebiyle güncellendi.
Sude’nin özgün belgesi docs/SPEC_ORIGINAL_SUDE.md altında aynen korunur.
Değişiklik dayanağı SPEC_ONERI.md ve bağlantılı REA kanıtlarıdır.
Arayüz kaynağı CONTRACT1.0.0, matematik kaynağı önceki SPEC;
inceleme ve uygulama oturumları ayrıdır. Yeni aday sürüm1.1.0rc4.

## Kapsam ve dış arayüz

Yalnız iki bağımsız grup t testi, test=t2-indep. Motor analyze(mapping)
çağrısı sonuç sözlüğü döndürür; çıktı yazmaz. CLI ve MCP aynı motoru ve
aynı serialize işlevini kullanır. CLI stdout tek satır JSON; başarılı
çıkış0, girdi hatası2, dahili hata1. Tam sayılar gerçek JSON int;
ondalıklar double hassasiyetinde, elle yuvarlama yok.

| Mod | test/mode dışında zorunlu girdiler | Zorunlu çıktılar |
|---|---|---|
| a-priori | tails,d,alpha,power,ratio | ncp,critical_t,df,n1,n2,n_total,actual_power |
| post-hoc | tails,d,alpha,n1,n2 | ncp,critical_t,df,power |
| compromise | tails,d,beta_alpha_ratio,n1,n2 | ncp,critical_t,df,alpha,beta,power |
| criterion | tails,d,power,n1,n2 | ncp,critical_t,df,alpha |
| sensitivity | tails,alpha,power,n1,n2 | ncp,critical_t,df,d |

Varsayılan yok. Eksik, bilinmeyen ve moda ilgisiz alan hatadır. CONTRACT
hata kodları korunur. Girdi sayıları sonlu; tails1/2; alpha,power açık(0,1);
ratio,d,beta_alpha_ratio pozitif; n1/n2 en az2 tam sayıdır. GUI'nin negatif d
ve kesirli n kabul etmesi bu sözleşmeyi değiştirmez.

## Matematik

df=n1+n2-2. delta=d*sqrt(n1*n2/(n1+n2)).
c=t.isf(alpha/tails,df). Tek yönlü güç SF_nct(c,df,delta);
çift yönlüde buna CDF_nct(-c,df,delta) eklenir.

[Sayısal karar] SF sonlu/geçerli değilse 1-CDF kullanılır; sol kuyruk CDF'si
geçersizse dağılım simetrisi SF(c,df,-delta) kullanılır. Hiçbir geçerli eşdeğer
kalmadıysa NO_SOLUTION. Yalnız1e-12 düzeyinde küçük aralık taşması[0,1]'e
sıkıştırılır; büyük hata gizlenmez. Bu backend kararı G*Power'ın aynı
kütüphaneyi kullandığı iddiası değildir.

## A priori tahsis kuralı

[REA-STATIC-008/009 ile desteklenen sürekli çözüm ve yuvarlama yolu]

Önce sürekli toplam x çözülür: kesirli n1=x/(1+ratio), n2=x-n1,
df=x-2 ile güç hedefe eşitlenir. x=4'te hedef zaten sağlanıyorsa minimum
toplam4 kullanılır. Aksi halde braket ve sürekli kök çözümü uygulanır.
Aranan, yuvarlanmış gruplarda en küçük gücü veren N değildir.

q=x/2; q10=floor(q*1e10+0.5)/1e10; N=2*ceil(q10).
n1=floor(N/(1+ratio)+0.5), n2=ceil(N-n1).
abs(ratio-1)<1e-8 ve abs(n1-n2)>1e-8 ise küçük grup yalnız bir kez1 artırılır.
Son n_total=n1+n2 ve df=n_total-2 üzerinden güç yeniden hesaplanır.
Yuvarlama sonrası actual_power hedeften biraz küçük kalırsa ayrıca N
optimizasyonu eklenmez. Çıktı ondalıkları bu iç yuvarlamadan bağımsızdır;
tam double hassasiyetle yazılır.

Küçük veya sıfır grup üreten uç tahsisler için mühendislik koruması
belgelenir; bu uçta GUI eşdeğerliği ayrıca doğrulanmalıdır. Birkaç örneğe
özel sabitler kullanılmaz. Tamamen aynı geliştirme setine uyum bağımsız
doğrulama değildir. Önceki ceil-ratio ve minimal-even-power varsayımları
bu statik bulguyla değiştirilmiştir.

[ORC-046/048 ve REA-STATIC-001 desteği] A-priori power<alpha reddedilir;
eşitlik kabul edilir ve normal minimum N araması yapılır.

[REA-STATIC-003 desteği] A-priori d>=1e-5 alt sınırı uygulanır; pozitif
fakat daha küçük d OUT_OF_RANGE olur. Bu kural diğer modlara genellenmez.
Statik bulgunun tam kaynak/hash ve sınırlamaları docs/REA_STATIC_FINDINGS.md'dedir.

[REA-STATIC-002/005/007] Verilen alpha ve power alanlarında
1e-7<=değer<=0.9999999; a-priori ratio için0.01<=ratio<=100 uçlar dahil
aralıkları uygulanır. Bu alpha/power sınırları girdiler içindir; ters çözümden
üretilen alpha/power çıktıları aynı aralığa zorlanmaz. Sözleşme içinde olup bu gözlenen aralıkların dışında
kalan girdiler de OUT_OF_RANGE olur. Testler uçların hemen iki yanını kapsar.

[Arama sınırı] En büyük çift toplam2.147.483.646. Bu büyüklük statik
doğrulama sabitiyle uyumludur; tüm girdilerde sonuç üretme garantisi değildir.
Bu sınırda hedefe ulaşılamazsa NO_SOLUTION.

## Diğer modlar

Post-hoc verilen N ile yukarıdaki gücü hesaplar.
Criterion verilen delta ve hedef güce karşı c eşiğini çözer; alpha=t.sf(c,df)*tails.
Compromise beta/alpha=q kökünü çözer; beta=1-power, alpha=t.sf(c,df)*tails.
Sensitivity sabit alpha ve N ile hedef gücü veren delta>=0 kökünü çözer;
d=delta/sqrt(n1*n2/(n1+n2)).

[Matematiksel açıklama; uçta yeni GUI gözlemi yok] Sensitivity power<alpha
ise doğrulama INCONSISTENT, field=power üretir; eşitlikte delta=d=0 ve normal c,df döner.
Yakın değerler eşitliğe yuvarlanmaz.

[Mühendislik kararı] Ters çözüm aramalarında delta/eşik büyüklük korumaları
1.000.000; bunlar gözlenmiş G*Power iterasyon sınırı olarak etiketlenmez.

## Kabul ve kanıt

Tam sayılar tür ve değer olarak kesin. Ondalıklar mutlak VEYA göreli1e-6.
Sözleşme dışı GUI başarı kayıtları ayrı tutulur, sessizce silinmez.
Motor testleri, public sayısal örnekleri, gerçek MCP parity ve Sude gelişim
seti ayrı raporlanır. Ajanın gerçek sağlayıcı değerlendirmesi, mock protokol
testinden ayrıdır. Gizli kapının geçildiği bu belgeyle iddia edilmez.

Temiz uygulama oturumuna yalnız davranış şartnamesi ve sınır ekleri verildi;
ham DOCX, binary, ekran görüntüsü veya oracle sonuç raporları açılmadı.

## Türler, hata alanları ve sayısal korumalar

`tails`, `n1`, `n2` gerçek tam sayı olmalıdır; bool kabul edilmez.
CLI metninde `2` geçerli, `2.0` ve `2e0` bu alanlarda INVALID_VALUE’dur.
API/MCP JSON girdisinde de `2.0` float olduğu için reddedilir. Diğer sayılar
sonlu int/float veya noktalı ondalık/bilimsel sayı metni olabilir; virgüllü
ondalık, NaN ve Infinity reddedilir. Zorunlu çıktı alanlarından df/n1/n2/n_total
JSON int’tir; diğer sayısal çıktılar tam double hassasiyetle serileştirilir.

| Durum | code | field |
|---|---|---|
| Zorunlu alan yok | MISSING_PARAM | Eksik alanın adı |
| Bilinmeyen veya moda ilgisiz alan | UNKNOWN_PARAM | Alanın adı |
| Sayısal tür/biçim hatası veya CLI’de yinelenen alan | INVALID_VALUE | Alanın adı |
| Geçerli biçim, izin verilen aralığın dışında | OUT_OF_RANGE | Alanın adı |
| A-priori/sensitivity power<alpha | INCONSISTENT | power |
| Desteklenmeyen test/mod | UNSUPPORTED | test veya mode |
| A-priori tahsis sonunda bir grup<2 | NO_SOLUTION | ratio |
| Arama koruması içinde hedefe ulaşılamadı | NO_SOLUTION | power veya beta_alpha_ratio |
| Beklenmeyen çalışma zamanı hatası | INTERNAL_ERROR | null |

Hata JSON’u error açıklaması, code ve field içerir. Açıklamanın birebir
G*Power hata metni olduğu iddia edilmez. Birden fazla hatalı alan varsa bütün
hataların birlikte listelenmesi veya belirli bir öncelik sırası garanti edilmez.
NO_SOLUTION sayısal backend/arama korumasından da doğabilir; G*Power’ın aynı
noktada mutlaka hata verdiğinin kanıtı değildir.

Sürekli a-priori çözüm uygulamada [4, üst braket] aralığında Brent yöntemiyle,
xtol=1e-10 ve en çok300 iterasyonla aranır. Sensitivity ve eşik kökleri
xtol=1e-12 kullanır. Çift yönlü criterion/compromise için c>=0, tek yönlüde
negatif c mümkündür. Bu çözücü seçimleri mühendislik kararlarıdır; özgün
programın aynı iterasyonları yaptığı iddiası değildir.

## Tekrarlanabilir kabul örnekleri

| Kaynak | Girdi özeti | Beklenen gözlem |
|---|---|---|
| ORC-011-REPLAY | tails=2,d=.5,alpha=.05,power=.8,ratio=.5 | n1=96,n2=48,N=144 |
| NEW-VAL-002 | tails=2,d=.95,alpha=.02,power=.93,ratio=.4 | n1=59,n2=23,N=82,actual_power=.9295480 |
| ORC-046/048 | power=alpha=.05; diğer kaynak girdileri sabit | Eşitlik kabulü,2+2 kişi |
| ORC-050/059 | Negatif d / kesirli n1 | GUI başarısı; CLI sözleşme gereği reddeder |

[REA] kaynakları: [statik bulgular](docs/REA_STATIC_FINDINGS.md),
[GUI bulguları](docs/REA_GUI_FINDINGS.md), [Sude görsel kontrolü](docs/SUDE_GORSEL_KONTROLU.md).
İlgili girdilerin tamamı ve gözlenen çıktılar oracle kayıtlarında bulunur.
[Okunabilir kabul senaryoları](features/t2_indep.feature) ile tests/ altındaki
otomatik kontroller aynı motoru sınar; feature dosyası otomatik Gherkin
çalıştırıcısı kullanıldığı iddiası değildir. [Güncel rapor](REPORT.md).
