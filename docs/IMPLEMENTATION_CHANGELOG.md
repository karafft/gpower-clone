# Uygulama değişiklik kaydı — 1.1.0rc1 aday

26 Ekim 2026. Uygulama girdileri: önceki transkribe SPEC/CONTRACT ve
`work/CORRECTED_SPEC.md` bağımsız davranış eki. Uygulama ajanı oracle klasörü,
ham belgeler, görüntüler veya koordinatörün gözlem raporlarını incelemedi.
Bu sürüm genellenmiş bir adaydır; G*Power eşdeğerliği kanıtı değildir.

## Motor

- A-priori artık çift toplam `N=2*k`, `k>=2` arar. Tahsis
  `n1=floor(N/(1+ratio)+0.5)`, `n2=N-n1` formülüdür. Her grup en az 2
  olmalıdır; hedefi karşılayan en küçük uygun çift toplam döner.
- Yarıma yuvarlama aritmetik half-up'tır. Tie davranışı SPEC'te hâlâ
  gözlenmemiş olarak belirtilmiştir; bu uygulama kararının bağımsız
  doğrulaması bekler. Önceki ceil oran/en küçük n1 kuralı kaldırılmıştır.
- A-priori `power==alpha` kabul edilir; `power<alpha` INCONSISTENT döner.
  Sensitivity için `power<=alpha` reddi ayrı, geçici politika olarak korunur.
- Sağ kuyruk için geçerli sonlu SF tercih edilir; geçersizse `1-CDF`
  denenir. Sol kuyruk CDF geçersizse simetri
  `F(-c;df,delta)=SF(c;df,-delta)` kullanılır. Bu son ek, verilen küçük-alfa
  regresyonunun arama adayındaki gerçek SciPy NaN sonucunu düzeltmiştir;
  koordinatör genel matematiksel kimliği onaylamıştır.
- Her kuyruk ve toplam kontrol edilir. Yalnız 1e-12 büyüklüğündeki küçük
  kayan nokta aralık sapmaları kabul edilip nihai değer [0,1]'e alınır;
  daha büyük geçersiz sonuçlar gizlenmez. Hiç geçerli olasılık yoksa
  NO_SOLUTION döner. Ters modlar da aynı olasılık yardımcısını kullanır.
- Geçici mühendislik sınırı `MAX_TOTAL=20,000,000`; ters delta/eşik sınırı
  1,000,000. Bunlar ürün gözlem limiti değildir. Üstel/ikili arama verilen
  SPEC'teki monotonluk varsayımına dayanır. Sayısal doğruluk SciPy sürümüne
  bağlıdır; CDF tamamlayıcısı çok küçük sağ kuyruklarda hassasiyet kaybedebilir.
- CONTRACT sürümü 1.0.0 korunur; paket/motor/MCP sunucu sürümü 1.1.0rc1.

## Gerçek doğrulama

Python 3.13.14 / SciPy 1.18.1 / MCP SDK 1.30.0 ortamında son test keşfi:
**17/17 test metodu geçti; 14.255 saniye**. Önceki ara çalıştırmada yalnız
mock değerlendirme fixture'ının null tool girdisini yanlış ele alması
başarısız olmuş, fixture düzeltilmiştir; bu canlı model sonucu değildir.

Kapsam: özgün beş public vektör, verilen yeni tahsis regresyonları, her iki
kuyrukta eşitlik, önceki çift toplamların minimalite taraması, küçük alfa,
SF/CDF fallback testleri, ters modlar, CLI sözleşmesi, gerçek MCP initialize/
tools-list/tools-call, **25 public + 8 hata girdisinde 33 tam metin eşitliği**,
mock sağlayıcıyla gerçek MCP ajan döngüsü ve değerlendirme puanlayıcı testleri.

Yeni aday wheel'i oluşturulup `work/merve-install-spec11` içine kuruldu.
Gerçek `gpower-clone`, `gpower-mcp`, `gpower-agent`, `gpower-agent-eval`
yürütücüleri toplam beş senaryoda kontrol edildi. MCP gerçek stdio çağrısı
yaptı; ajan `--help`, değerlendirme anahtarsız not_run yolu kontrol edildi.
Bağımlılıklar önceki .deps ortamından sağlandığı için sıfırdan bağımlılık
kurulumu iddiası yoktur. Ayrı yeni performans kıyaslaması yapılmadı.

`logs/mcp_parity.jsonl` son 33 satırlık aday çalıştırmayla değiştirilmiştir;
bu dosya scripted/public sentetik taşıma kaydıdır, LLM veya oracle gözlemi
değildir. Eski tarihli zeliha_test_summary.json tarihsel sonucu korur.
Güncel özet `logs/software_summary_spec11.json`, kurulum kontrolü
`logs/installed_console_spec11.json` dosyasındadır.

## İsteğe bağlı gerçek LLM değerlendirmesi

`gpower-agent-eval --run-live --model MODEL` yalnız yapılandırılmış
GPOWER_API_KEY/OPENAI_API_KEY ile çalışır. Model Chat Completions function
calling desteklemelidir; Responses gerektiren modeller için adaptör yoktur.
Varsayılan vakalar `eval/agent_questions_review.jsonl` içindeki on public/
sentetik sorudur. Her soru ayrı gerçek MCP oturumuyla işlenir; model son
JSON kararı (`action`, `label`, `message`) ve gerçek araç izleri tutulur.
Etiket, eylem, parametre ve public sayısal sonuç doğruluğu ölçülür;
başarısız vakalar paydaya dahildir. Uygun anahtar/model veya --run-live yoksa
0 vaka, null metrik ve not_run döner. Bu oturumda **0 canlı LLM çağrısı**
yapılmıştır; mock puanlayıcı kontrolleri ajan doğruluk yüzdesi değildir.

Depoya yazılmadı, yayımlanmadı ve ZIP yeniden oluşturulmadı. Koordinatör
harici doğrulama, son ekip belgeleri ve paketlemeden sorumludur.


# 1.1.0rc2 — temiz sınır eki

26 Ekim 2026. Yalnız work/SPEC_BOUNDARY_ADDENDUM.md davranış eki okundu;
ham yürütücü/oracle/görüntü veya koordinatörün kanıt raporları okunmadı.

A-priori d alt sınırı 1e-5 olarak uygulandı. Pozitif fakat altındaki değerler
OUT_OF_RANGE/d döner; tam uç nokta alan kontrolünden geçer. Diğer modların
pozitif d kuralı korunur; bu eşik diğer modlara yayılmaz. Ek içindeki
REA-STATIC-003 etiketi koordinatörün ayrı analizine atıftır; uygulama ajanının
yaptığı gözlem veya yeni oracle fixture'ı değildir.

Çift toplam arama tavanı 2,147,483,646 oldu. Bu aday arama/aritmetik sınırıdır;
genel post-hoc grup boyutlarına yeni bir üst sınır getirilmedi. Alan kontrolünü
geçen fakat tavanda hedefe ulaşamayan problem NO_SOLUTION döner. Paket, motor
ve MCP sürümü 1.1.0rc2; CONTRACT yine 1.0.0.

Anlamlı yeni testler: math.nextafter ile sınırın hemen altı/üstü ve uç noktası;
uç noktanın alan kabulü ile arama başarısızlığının ayrımı; post-hoc için
eşiğin uygulanmaması; d=.0005, alpha=.05, power=.8, ratio=1, tails=2 ile
20 milyonun üzerindeki ulaşılabilir tasarım ve bir önceki çift toplamın
yetersizliği. Beklenen N harici gözlemden sabitlenmedi. Hesaplanan sonuç:
n1=n2=62,790,886, toplam125,581,772, güç0.8000000060271003.

Son bütünleşik test: **19/19 metot geçti, 18.579 saniye**. Bu süre bütün
süite aittir, tek çağrı performans garantisi değildir. Gerçek MCP33 satır
CLI metin eşitliği ve açıkça mock sağlayıcı ajan/değerlendirme testleri
korundu. Kurulan dört gerçek konsol giriş noktası beş senaryoda yeniden
kontrol edildi; MCP gerçek initialize/list/call, ajan --help, değerlendirme
anahtarsız not_run yolu çalıştı. Canlı LLM çağrısı0.

rc1 raporları tarihsel olarak korundu. mcp_parity.jsonl son rc2 çalıştırma
ile değiştirildi. Güncel kayıtlar logs/software_summary_spec11rc2.json ve
logs/installed_console_spec11rc2.json. Harici oracle değerlendirmesini
koordinatör yapar; burada böyle bir başarı iddiası yoktur. Depo/ZIP değişmedi.


## rc2 son matematiksel açıklama — sensitivity eşitliği

work/SPEC_SENSITIVITY_EQUALITY.md okundu. Özgün SPEC'in negatif olmayan delta
ve sıfır dahil etki çıktısı tanımına göre sensitivity power==alpha sınırında
ncp=0.0,d=0.0 döner; normal critical_t ve tam sayı df korunur. power<alpha
reddedilir. Önceki geçici power<=alpha reddi bu sürümde kaldırıldı. Bu yeni
GUI gözlemi değildir; matematiksel açıklamadır ve endpoint harici doğrulaması
bekler. Yalnız kesin eşitlik özel duruma girer; yakın değerler yuvarlanmaz.

Her iki kuyruk eşitliği ve hemen üst komşu değerin kök çözümüne girmesi test
edildi. Olağan pozitif ters hesaplar korundu. Nihai bütünleşik çalışma:
**20/20 test metodu geçti, 17.426 saniye**. Önceki19 test sonucu tarihsel ara
sonuçtur. Paket son koddan tekrar oluşturulup work/merve-install-spec11rc2-final
konumuna kuruldu. Dört gerçek konsol giriş noktası beş senaryoda tekrar
kontrol edildi; gerçek MCP sensitivity eşitliği doğrulandı. Nihai kurulum
kaydı logs/installed_console_spec11rc2_final.json; güncel yazılım özeti
logs/software_summary_spec11rc2.json. Önceki19 test özeti
logs/software_summary_spec11rc2_pre_equality.json ile korunur. Canlı LLM0;
depo/ZIP değişmedi. Sürüm halen yayımlanmamış1.1.0rc2.


# 1.1.0rc3 — son temiz alan sınırları

26 Ekim 2026. Yalnız work/SPEC_OBSERVED_RANGES.md semantik eki okundu.
Koordinatörün ayrı statik analizinden bildirilen kurallar: verilen her alpha
ve power için kapalı [1e-7,0.9999999], a-priori ratio için kapalı [0.01,100].
Dışında OUT_OF_RANGE ve ilgili field döner. Diğer modlarda ratio ilgisiz
parametre olarak reddedilir. d a-priori alt sınırı ve sensitivity sıfır
sonucu korunmuştur. Kaynak etiketleri REA-STATIC-002/005 koordinatör analizine
aittir; uygulama ajanının ham ikili/oracle incelemesi yoktur. Bu sınırlar
arama mühendislik korumalarından ayrıdır.

Her sınır için kesin uç noktalar, içerideki hemen komşular ve dışarıdaki
math.nextafter komşuları test edildi; yuvarlak karşılaştırma kullanılmadı.
Eski aşırı küçük oran NO_SOLUTION testi yeni gözlenmiş oran alanını ihlal
ettiğinden, alan içinde fakat tavanda çözümsüz d=1e-5/ratio=.01 tasarımına
uyarlandı. Yeni özellik eklenmedi. Motor/paket/MCP1.1.0rc3; CONTRACT1.0.0.

Nihai suite: **21/21 test metodu geçti,18.366 saniye**. Özgün public/ters/
minimal çift toplam, sınır/büyük N, gerçek MCP33 ve mock ajan testleri korundu.
Son wheel work/merve-install-spec11rc3 içine kuruldu. Dört gerçek konsol girişi
altı senaryoda kontrol edildi: sürüm, sensitivity eşitliği, alan-dışı alpha
reddi, ajan yardım, anahtarsız eval ve gerçek MCP initialize/list/call.
Güncel özet logs/software_summary_spec11rc3.json; kurulum kaydı
logs/installed_console_spec11rc3.json. mcp_parity.jsonl son rc3 scripted
sonuçlarıyla değiştirilmiştir. Önceki sürüm raporları tarihsel olarak korunur.
Canlı LLM0, uygulama ajanı oracle çalıştırması0; depo/ZIP değişmedi.
