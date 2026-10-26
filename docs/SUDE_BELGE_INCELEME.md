> SONRAKİ DÜZELTME: Bu ilk incelemenin tarihsel raporudur. Son1.1.0rc4 sürümünde58/58 kayıt ve38/38 N eşleşti; güncel REPORT.md esas alınmalıdır.

# Sude protokol belgesinin incelemesi

26 Ekim 2026. Kaynak: kullanıcının sağladığı sude 60 görüntü.docx.
SHA-256: d65d739d7a924e3418d5de752362bee11600b42287e062deb5882982a75002a7.
Özgün Word dosyası değiştirilmedi. Motor da bu incelemede değiştirilmedi.

## Sonuç

Belge önemli davranış farklarını ortaya çıkarıyor. Mevcut motor bu setin N
örneklerinde %90'a ulaşmıyor. Önceki 12 yazılım testinin geçmesi ve MCP–CLI
eşdeğerliği, G*Power davranışının eşleştiği anlamına gelmiyordu; yeni karşılaştırma
bunu somut olarak gösterdi. Mevcut paket teslim için doğrulanmış sayılmamalı.

## Dosyada ne var

- ORC-001–ORC-060 arasında 60 kayıt.
- 49 sayısal sonuç ve 11 hata bilgisi.
- Gömülü resim, drawing/blip veya dış görsel ilişkisi yok. Bunlar ekran
  görüntüleri değil, metin halinde aktarılmış protokol/hata kayıtlarıdır.
- Yeni binary adresi veya dize referansı yok; bu belge ekip tanımında [REA]
  kanıtını tamamlamıyor. G*Power sürüm ekranı ve executable hash'i de yok.
- Boş d girdisi ORC-060'ta eksik parametre olarak normalize edildi; gerçek
  GUI boş alanının CLI'de sayısal sıfırla aynı olduğu varsayılmadı.

## Gerçek karşılaştırma

60 kayıt mevcut CLI ile ayrı süreçlerde çalıştırıldı. Sayısal tolerans mutlak
veya göreli 1e-6, tam sayılarda tür ve değer kesin eşleşme, çağrı sınırı 2 saniye.

- Ham sonuç: 48 geçti, 12 uyuşmadı.
- ORC-050 negatif d ile, ORC-059 kesirli n1 ile sayısal sonuç bildiriyor.
  CONTRACT d>0 ve tam sayı örneklem istediğinden bu ikisi sözleşme ile GUI
  arasındaki farktır; motorun bunları reddetmesi otomatik hata sayılmamalıdır.
- Bu iki çelişkili kayıt ayrılınca: 58 kayıtta 48 eşleşme, 10 uyuşmazlık.
- Aynı ayrımla a-priori N alanları: **28/38 tam eşleşme, %73.68**.
  Bu oran yalnız bu kullanıcı setinindir, yarışmanın gizli test sonucu değildir.
- Kayıtlar artık inceleme/geliştirme setidir; sonraki bağımsız değerlendirme
  için yeni, ayrı tutulan vektörler gerekir.

## Düzeltme gerektiren temel farklar

### Grup tahsisi

ORC-010: d=0.5, alpha=0.05, power=0.8, tails=2, ratio=1.5.
Belgede n1=54, n2=80, toplam=134; mevcut motor 53/80, toplam=133 üretti.

ORC-033: aynı temel değerlerde ratio=1.3.
Belgede 57/73, toplam=130; motor 57/75, toplam=132 üretti.
Üstelik ceil(57*1.3)=75 olduğundan SPEC'in n2=ceil(n1*ratio) kuralı
belgedeki 57/73 kaydıyla doğrudan çelişiyor.

Diğer tahsis uyuşmazlıkları: ORC-011, ORC-026, ORC-034, ORC-035, ORC-036.
Belgedeki sonuçları açıklayan yeni genel kural henüz kanıtlanmadı. Tek tek
vektörlere özel sabit değerlerle düzeltme yapılmamalıdır. Eşit olmayan oranlarda
toplam N ve tahsis adımlarını ayırt eden yeni deneyler gerekir.

### Power ile alpha eşitliği

ORC-046 (çift yönlü) ve ORC-048 (tek yönlü), power=alpha=0.05 için 2/2
ve toplam 4 veriyor. Mevcut motor power<=alpha koşuluyla hata üretiyor.
ORC-047 ise power=0.03<alpha=0.05 için hata bildiriyor. Bu kayıtlar
a-priori için eşitlik ile küçüklüğün ayrılması gerektiğini destekliyor;
diğer modlara otomatik genellenmemelidir.

### Sayısal hesap

ORC-023: tails=2, d=0.6, alpha=0.0001, power=0.8, ratio=1.
Belgede 129/129 ve toplam 258; mevcut motor NO_SOLUTION verdi.
Bu, tahsis kuralından ayrı araştırılması gereken sayısal bir başarısızlık.

## Sude'den gereken ek kanıt

1. Özellikle yukarıdaki kayıtlara ait özgün protokol dosyaları veya ekran
   görüntüleri, sürüm ekranı ve GPower.exe SHA-256 kaydı.
2. Tahsis algoritmasını ayırt eden ek oran/eşik deneyleri; ilgili binary
   kanıtı bulunabiliyorsa adres/dize referansıyla [REA] defterine işleme.
3. SPEC'te eski ceil kuralını doğrulandı olarak sunmama; gözlem, hipotez ve
   CLI kararlarını ayıran güncel şartname.
4. Düzeltilmiş şartnameyi ayrı uygulama oturumuna aktarma; ham kanıtları
   uygulama oturumuna vermeme. Sonraki sürümü yeni bir saklı setle değerlendirme.

## Üretilen dosyalar

- merve-engine-cli/oracle/sude_protocol_text.txt: DOCX'ten çıkarılan tam metin.
- merve-engine-cli/oracle/sude_protocol_vectors.jsonl: 60 normalize kayıt.
- merve-engine-cli/tests/reports/sude_protocol_cli.json: her kayıt için beklenen,
  gerçek çıktı, süre ve uyuşmazlıklar.

Bu inceleme kaynak belgedeki metinlerin aktarımını ve motorla karşılaştırmasını
doğrular; protokollerin gerçek G*Power çalıştırmasına ait olduğunu bağımsız olarak
kanıtlamaz. Ekran görüntüsü veya binary kanıtı uydurulmamıştır.
