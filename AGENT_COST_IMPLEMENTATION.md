> **Gerçek kullanım güncellemesi:** Önceki kısmi canlı koşumda7 model yanıtı,4.299 girdi+5.175 çıktı=9.474 toplam token raporlandı. Başarılı canlı MCP çağrısı0; GUI karşılaştırması ve doğrulanmış ücret yok. Kaynak logs/measured_partial_usage.json. Aşağıdaki ilk aşama tablosu tarihsel kayıttır.

# Ajan kullanım ve maliyet kaydı

Tarih: 25 Ekim 2026. Kaynak: bu sohbet ve ayrı temiz uygulama alt oturumu.

| Alan | Kayıt |
|---|---|
| Koordinasyon | Bu sohbet; repo belgeleri ve görev planı incelendi |
| Uygulama | Ayrı, geçmişi aktarılmamış uygulama ajanına SPEC/CONTRACT aktarımı; sonrasında aynı oturumda paket/MCP/ajan geliştirmesi |
| Kesin model kimliği | Bu rapor için doğrulanmış telemetri yok |
| Girdi/çıktı token toplamı | Bilinmiyor; uydurulmadı |
| Parasal maliyet | Bilinmiyor; hesap faturası alınmadı |
| Kesin iterasyon sayısı | Otomatik ölçülmedi; sayı verilmedi |
| GUI ile token/süre karşılaştırması | Henüz yapılmadı |

Ölçülmüş test ve süreler REPORT.md ile tests/reports altındaki raporlarda yer alır. Testlerin toplam süresi, model token maliyeti değildir. Gerçek ajan çağrılarında varsa sağlayıcının usage alanları kaydedilir; olmayan değerler bilinmiyor olarak tutulur. Scriptli/fixture test çağrıları gerçek LLM değerlendirmesi gibi sunulmaz.

Bir sonraki çalışmada başlangıçtan itibaren sağlayıcı usage kayıtları, sürüm/hash ve her deneyin kaynak kimliği tutulmalı; inceleme ve uygulama girdileri baştan fiziksel olarak ayrılmalıdır. Her üye kendi gerçek oturumunu bu ortak kayda ayrıca eklemelidir; bu dosya üç kişinin bağımsız katkı beyanı değildir.
