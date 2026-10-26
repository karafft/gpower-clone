> **Son denetim:** ORC-011 yeni gerçek koşumla tamamlandı;96/48/toplam144. Ayrı kanıt oracle/replays/vectors.jsonl. Güncel75 görsel,58/58 kayıt ve38/38 N sonucu REPORT.md içinde. Aşağıdaki önceki aşama kayıtları tarihsel olarak korunur.

> **YAYIN GÜNCELLEMESİ — 26 Ekim2026:** Kullanıcının talebiyle kaynaklar ve kanıtlar repoya eklendi. Aşağıdaki yüklenmedi/onay bekliyor notları yerel hazırlık aşamasının tarihsel kaydıdır.

> **GÜNCEL — 26 Ekim, ekran görüntüleri alındı:** Sude’nin60 PNG’si
> pakete eklendi ve kayıtlarla karşılaştırıldı.59 görüntüde sonuç/hata mevcut;
> ORC-011’in çıktıları ? olduğu için bu görsel sayısal sonucu kanıtlamıyor.
> Görselle desteklenen, sözleşmeye uygun57/57 kayıt ve37/37 N hesabı eşleşti.
> Önceki14 yeni GUI deneyiyle toplam74 görsel var;30+ görsel hedefi karşılandı.
> Aşağıdaki “görseller gelmedi/30 görsel eksik” ifadeleri önceki aşamaya aittir.
> Ayrıntı: docs/SUDE_GORSEL_KONTROLU.md. Canlı ajan/token ölçümü hâlâ bekliyor.

# Kanıt defteri

Bu defter gerçek binary okumalarını, kullanıcı protokolünü ve varsayımları
ayırır. Binary3.1.9.7, tercih edilen image base0x400000; hash
c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812. Yöntem PE okuması ve Capstone.

| Kimlik | Kanıt ve adres | Sınırlı çıkarım |
|---|---|---|
|[REA-STATIC-001]|0x4880f9 ->0x5c6220; karşılaştırıcı0x4880e0|Eşitlik hata dalına zorunlu olarak gitmiyor; ORC046/048 destekliyor |
|[REA-STATIC-002]|0x4d9c3c ->0x487300; sabit0x5c3b50|Tahsis oranı0.01–100 uçlar dahil |
|[REA-STATIC-003]|0x4d9260,0x4d9285; sabit0x5c7ed8|A-priori abs(d)>=1e-5 karşılaştırması |
|[REA-STATIC-004]|0x4d9a3a ->0x5cb418|İki bağımsız ortalama test etiketiyle nesne bağlantısı |
|[REA-STATIC-005]|0x487460; sabitler0x5c4398/0x5c6860|Alpha1e-7–0.9999999 uçlar dahil |
|[REA-STATIC-006]|0x488a3c ->0x5c6524|Toplam N için ayrı doğrulama mesaj/yolu |
|[REA-STATIC-007]|0x488010,0x48809c ->0x5c60d8|Power aralık yolu ve aynı uç sabitleri |
|[REA-STATIC-008]|0x496aa0 ->0x4d64c0 ->0x496a20|Sürekli çözüm sonrası10 ondalık ön yuvarlama ve çift toplam |
|[REA-STATIC-009]|0x4d9d55,0x4d9d88,0x4d9dd2–0x4d9e03|Half-up ilk grup, ceil ikinci grup ve yakın-eşit tek düzeltme |

RVA, dosya offset'i, kısa dize ve referanslar oracle/binary_evidence.json;
aritmetik yorum ve sınırlar docs/REA_STATIC_FINDINGS.md. Özgün binary,
kurulum ZIP'i ve raw assembly/decompile dökümü teslimde bulunmaz.

## ORC ve doğrulama

ORC001–060 kullanıcının Sude belgesinden metin olarak aktarıldı. Kaynak
DOCX hash'i ve her kaydın kimliği oracle/sude_protocol_vectors.jsonl altında.
Belgede gömülü görsel yok; ayrı klasördeki özgün görüntüler paylaşılmadı.
Kaynak protokolü gerçek G*Power koşumuna bağlayan görsel/özgün dosya kontrolü
henüz yapılmadı. Bu metinler binary kanıtı diye etiketlenmez.

Sonuç:58 sözleşme-uyumlu kayıt eşleşti,38 N örneği tam eşleşti; iki GUI
başarı kaydı sözleşme dışında ve ayrı tutuldu. Yeni GUI takip seti aşağıda ayrıca raporlandı; gizli yarışma verisi yok.

## Varsayım ve mühendislik kararları

- Sürekli kökü bağımsız Brent yöntemiyle çözüyoruz; orijinal çözücünün bütün
  nümerik adımları kopyalanmadı. Alt toplam4 kelepçesi ve aşırı tahsiste
  küçük grubu reddeden koruma uçta GUI doğrulaması bekler.
- Sensitivity power==alpha için d=0 sınırı matematiksel SPEC açıklamasıdır;
  yeni GUI gözlemi değildir.
- Ters çözüm korumaları, metin hata kodları ve JSON biçimi CLI kararlarıdır.
- Kamu vektörleri ve statsmodels verileri yeni[REA] veya[VAL] olarak sunulmaz.


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
