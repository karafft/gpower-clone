# Ekip onayı için devir

Motor/CLI, gerçek MCP, API ajan kodu, değerlendirme aracı, kanıt defteri,
source hash'leri,25 test,58 kaynak doğrulaması ve açıklayıcı demo hazır.

Sude: SPEC_ONERI.md, LEDGER.md ve dokuz statik bulgu başlığını kontrol et.
Özgün görseller elindeyse ORC kimlikleriyle bağla. Yeni saklı VAL setini
uygulama oturumundan ayrı tut; mevcut60 kayıt artık geliştirmede kullanıldı.

Zeliha: dört Python modülünü, MCP tek aracını ve API konfigürasyonunu kontrol
et. Gerçek model koşumu/logları ve GUI/MCP token karşılaştırması henüz yok.
Model/anahtar yerelde ayarlanır; sırlar repoya veya sohbet metnine yazılmaz.

Merve: onaylanan kaynakları mevcut repo belgeleriyle birleştir. ZIP'i veya
binary/decompile dosyalarını yükleme. CONTRACT.md değişmez; önerilen SPEC
ve README ekip kararıyla güncellenir. Git etiketi kaynak onayından sonra.

Python API: from gpower_clone import analyze,serialize,AnalysisError.
analyze(mapping) çıktı yazmaz, serialize canonical JSON verir. MCP aynı
API'yi kullanır. Kaynak yazar/oturum sınırları docs/CLEAN_ROOM_PROVENANCE.md'de.
