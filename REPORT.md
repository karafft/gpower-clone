> **GÜNCEL — 26 Ekim, ekran görüntüleri alındı:** Sude’nin60 PNG’si
> pakete eklendi ve kayıtlarla karşılaştırıldı.59 görüntüde sonuç/hata mevcut;
> ORC-011’in çıktıları ? olduğu için bu görsel sayısal sonucu kanıtlamıyor.
> Görselle desteklenen, sözleşmeye uygun57/57 kayıt ve37/37 N hesabı eşleşti.
> Önceki14 yeni GUI deneyiyle toplam74 görsel var;30+ görsel hedefi karşılandı.
> Aşağıdaki “görseller gelmedi/30 görsel eksik” ifadeleri önceki aşamaya aittir.
> Ayrıntı: docs/SUDE_GORSEL_KONTROLU.md. Canlı ajan/token ölçümü hâlâ bekliyor.

# Nihai yerel doğrulama raporu

26 Ekim2026 · sürüm1.1.0rc4. Güncel sonuçlar aşağıdadır; daha eski sürümlerin
raporları tarihsel kanıt olarak saklanmıştır. Yayın veya Git commit yapılmadı.

| Kontrol | Gerçek sonuç | Kayıt |
|---|---|---|
| Yazılım testleri |25 test,0 hata/başarısız/atlanan; 20.992s toplam |tests/reports/unit_final_rc4.txt |
| MCP protokolü |initialize/list/call,33/33 tam CLI eşdeğerliği |logs/mcp_parity.jsonl |
| Sude kaynak seti |58/58 uyumlu kayıt,38/38 N |tests/reports/sude_final_rc4_58.json |
| İki sözleşme çelişkisi |Negatif d ve kesirli n1 reddi doğru |tests/reports/final60_audit.json |
| CLI süreleri |Ayrı58 süreçte en yavaş 1.224387s;2s timeout |tests/reports/sude_final_rc4_58.json |
| Sayısal ölçek |540/540, en büyük güç farkı 5.55e-16 |oracle/scale/statsmodels_final_rc4.summary.json |
| Kurulum |Wheel kuruldu; dört modül ve metin başlatıcı kontrol edildi |logs/installed_final_rc4.json |
| Windows exe başlatıcı |Uygulama Denetimi4551 ile engelledi; güvenlik değişmedi |logs/windows_launcher_policy.json |
| Binary analizi |7 dize/xref + yapısal/aritmetik adresler |oracle/binary_evidence.json |
| Canlı model |0 çağrı; başarı/token maliyeti ölçülmedi |AGENT_COST.md |

Önceki motor Sude setinde N28/38(%73.68) üretiyordu. Genel tahsis kuralı,
eşitlik ve sonlu kuyruk hesapları düzeltildi. İlk tam veri koşumunda ayrıca
tek zaman aşımı kaydedildi; tekrar ve nihai58 koşumunda hata kalmadı.
Eski rapor silinmedi. Tüm çağrılarda/tüm makinelerde2s garantisi verilmez.

Sözleşmeyle uyumlu58 veri47 sayısal ve11 hata kaydından oluşur; hata
kayıtlarında kaynakta hata kodları bulunmadığı için hata varlığı ve çıkış
durumu sınanır.60/60 GUI eşleşmesi denmez: iki GUI başarı girdisi CONTRACT'ın
izin vermediği tür/aralıktadır. Onların gerçek CLI sonuçları ayrı raporlanır.

Bu set artık geliştirme/regresyon setidir;38/38 sonucu bağımsız saklı set
veya hocanın gizli%90 kapısının sonucu değildir. Statsmodels aynı SciPy
altyapısından yararlanabilir; çapraz kontrol tam bağımsız doğruluk ispatı değildir.
Mock sağlayıcı testi gerçek MCP taşır fakat canlı model doğruluğu sayılmaz.

Binary sürümü3.1.9.7, SHA256 c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812.
Resmî kaynak örneği incelendi; Sude'nin executable hash'iyle eşleştirme yapılmadı.
İnceleme Capstone/PE okumasıdır; Ghidra veya özel REA uygulaması çalıştırılmış
gibi gösterilmez. Tüm çözücünün bit düzeyinde söküldüğü iddia edilmez.

Kaynak dondurma hash'i SOURCE_FREEZE.json ve tüm paket dosyalarının hash'leri
SHA256SUMS.json altında. Git etiketi ekip onayından sonra oluşturulmalıdır.


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
