# Ajan değerlendirmesi ve mevcut soruların incelemesi

Orijinal 10 soru repoda eval/agent_questions.jsonl altındadır. Bu pakette o
dosya değiştirilmez; yeni bir G*Power sonucu üretilmiş gibi doldurulmaz.

## Orijinal sorularda çözülmesi gereken belirsizlikler

- Q01, Q02 ve Q06 için expected_tool_input ratio=1 kabul ediyor; soru metninde eşit tahsis açıkça belirtilmiyor. Oran sorulmalı veya eşit tahsis varsayımı kullanıcıya açıkça sunulmalıdır. Otomatik puanlamadan önce soru metni/ölçüt uyumu ekipçe düzeltilmelidir.
- Q04 hem sayısal etki hem test yönü bakımından eksik. Güvenli kabul davranışı açıklama/teyittir; araç çağrısı zorunlu değildir. "Orta" sessizce 0.5'e çevrilmez.
- Q07 ve Q08 kapsam dışı tasarımlardır; iki bağımsız gruba çevrilmez.
- Q09 için hesaplama yerine bilgi istenir.
- Sonuç beklenen diğer kayıtlarda expected_n/expected_power/evidence gerçek G*Power gözleminden gelmelidir. Motor çıktısı expected olarak kopyalanmaz.

## Koşum ve raporlama

Gerçek LLM koşumu için docs/ZELIHA_KURULUM.md içindeki model ve anahtar
kurulumu gerekir. Anahtarlar repoya veya konuşmaya yapıştırılmaz. İlk
değerlendirmede her sorunun cevabı, doğru aile/eylem/girdi ve kaynak kanıtına
göre N/güç eşleşmesi ayrı sütunlarda değerlendirilmelidir. Eksik oracle
nedeniyle N karşılaştırılamıyorsa null/ölçülmedi olarak tutulmalıdır.

Scriptli MCP testleri protokol ve aktarım testidir; Türkçe soruları modelin
doğru anladığının kanıtı değildir. GUI/MCP token karşılaştırması aynı
sorular, aynı model, aynı token sayma yöntemi ve ölçülmüş sürelerle yapılır;
henüz böyle bir karşılaştırma yapılmadı.
