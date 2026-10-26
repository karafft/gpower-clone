# Ajan maliyet ve süreç günlüğü

Her oturum için kullanılan ajan, yaklaşık token ve maliyet, iterasyon sayısı ve "neyi farklı yapardık" notu. Herkes kendi oturumunun satırını doldurur.

**İterasyon:** Oturumdaki kullanıcı mesajı (istek) sayısı.
**Token:** Bağlam penceresinin anlık doluluğu ile toplam faturalanan token farklı şeylerdir. Mümkünse ikisi de yazılır; toplam token, kullanılan aracın kullanım ekranından alınır.

## Özet

| Oturum | Kişi | Ajan / model | Toplam token (yaklaşık) | Maliyet | İterasyon | Durum |
|---|---|---|---|---|---|---|
| İnceleme ve SPEC | Sude | | | | | sürüyor |
| Motor ve CLI (temiz oda) | Merve | | | | | başlamadı |
| Repo, MCP ve ajan | Zeliha | Claude Code (masaüstü), Claude Opus 5.5 | bağlam ≈ 260 bin (2026-10-26); toplam: kullanım ekranından eklenecek | abonelik planı; eklenecek | ≈ 27 | sürüyor |
| Ajan değerlendirmesi (MCP) | Zeliha | | | | | başlamadı |
| Ajan değerlendirmesi (GUI) | Zeliha | | | | | başlamadı |

---

## Oturum notları

### Repo, MCP ve ajan (Zeliha)
- **Ajan:** Claude Code, masaüstü uygulaması, model Claude Opus 5.5
- **Başlangıç:** 2026-10-25
- **Yapılanlar:**
  - ödev ve sözleşme analizi
  - görev dağılımı, kurulum rehberi ve üç oturum prompt'u
  - repo iskeleti ve .gitignore
  - CONTRACT.md ve 25 referans vektörü
  - 10 soruluk ajan değerlendirme seti
  - Sude'nin SPEC'i ve deney sonuçları için geri bildirim ve 60 deneylik plan
- **Zaman alan adımlar:**
  - ekip içi görev dağılımının iki kez yeniden yazılması
  - sözleşmenin önce özetten, sonra tam metinden okunması (bkz. HALLUCINATIONS.md H-003)
- **Neyi farklı yapardık:**
  - Sözleşmeyi en başta tam metniyle repoya koyup herkesin aynı kaynaktan çalışmasını sağlamak.
  - Kâhin deneylerini SPEC yazılmadan önce yapmak; SPEC'in ilk sürümü deneylerden önce yazıldığı için yuvarlama kuralı yanlış çıktı (H-001).

### İnceleme ve SPEC (Sude)
_Doldurulacak._

### Motor ve CLI (Merve)
_Doldurulacak._
