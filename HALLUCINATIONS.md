> Güncel uygulama kayıtları: [HALLUCINATIONS_IMPLEMENTATION.md](HALLUCINATIONS_IMPLEMENTATION.md). Aşağıdaki ekip notları korunmuştur.

# Halüsinasyon günlüğü

AI oturumlarının yanlış çıkardığı ya da kanıtsız ileri sürdüğü şeyler. Her kayıtta iddia, nasıl fark edildiği ve onu yakalayan deney ya da test yer alır.

Herkes kendi oturumundaki kayıtları ekler. Kimlik sırası: H-001, H-002 …

## Kayıt şablonu
```
### H-xxx <kısa başlık>
- Oturum / kişi:
- Tarih:
- İddia:
- Neden inandırıcıydı:
- Nasıl fark edildi:
- Yakalayan deney / test: [ORC-...] / [VAL-...] / tests/...
- Doğrusu:
- Durum: düzeltildi / açık
- Ders:
```

---

### H-001 Eşit olmayan oranda n2 = ⌈n1 · ratio⌉ kuralı
- **Oturum / kişi:** İnceleme tarafı, SPEC.md ilk sürümü (5f508eb). Kuralın AI oturumundan mı geldiğini Sude teyit edecek.
- **Tarih:** 2026-10-25
- **İddia:** a-priori modunda n1 aranır, ikinci grup her adımda n2 = ⌈n1 · ratio⌉ ile bulunur.
- **Neden inandırıcıydı:** Oran 1, 2, 0.5 ve 0.67 olan vektörlerde kural doğru sonuç veriyordu.
- **Nasıl fark edildi:** Aynı dosyadaki ratio = 1.5 vektörü 54 / 80 diyordu; kurala göre n2 = ⌈54 · 1.5⌉ = 81 olmalıydı.
- **Yakalayan deney:** [ORC-010] G*Power ratio 1.5 için gerçekten 54 / 80 veriyor. [ORC-033]–[ORC-037] (oran 1.3, 0.7, 2.5, 1.1, 0.75) de kuralla uyuşmuyor.
- **Doğrusu:** Henüz doğrulanmadı. Gözlenen bütün vektörlere uyan hipotez: n1 = round(N / (1 + ratio)), n2 = N − n1. Bu bir [AJAN] hipotezi; binary kanıtı ([REA]) bekleniyor.
- **Durum:** açık
- **Ders:** Birkaç "kolay" oran (tam sayı çarpım veren) yuvarlama kuralını ayırt etmez. Kural, küsuratlı çarpım veren oranlarla sınanmalı.

### H-002 Doğru vektörün türetilmiş sanılması
- **Oturum / kişi:** Repo ve entegrasyon oturumu (Zeliha, Claude Code)
- **Tarih:** 2026-10-25
- **İddia:** ground_truth.json'daki ratio 1.5 vektörü (54 / 80) G*Power'da çalıştırılmamış, ratio 0.67 vektöründen türetilmiş olabilir; çünkü ikisinin ncp, kritik t, df ve güç değerleri birebir aynı.
- **Neden inandırıcıydı:** Kural ile vektör çelişiyordu ve iki vektörün çıktıları özdeşti.
- **Nasıl fark edildi:** G*Power protokol çıktısı ratio 1.5 için 54 / 80 verdi. Özdeş çıktıların nedeni ncp'nin n1 ve n2'ye göre simetrik olması: (54, 80) ile (80, 54) aynı sonucu verir.
- **Yakalayan deney:** [ORC-010], [ORC-012]
- **Doğrusu:** Vektör doğruydu, yanlış olan SPEC'teki kural (H-001).
- **Durum:** düzeltildi (geri bildirim notunda)
- **Ders:** Kural ile kâhin verisi çeliştiğinde önce kâhin yeniden ölçülür. Veriyi değil, kuralı şüpheli saymak gerekir.

### H-003 Çıktı alanlarının her modda zorunlu sanılması
- **Oturum / kişi:** Repo ve entegrasyon oturumu (Zeliha, Claude Code)
- **Tarih:** 2026-10-25
- **İddia:** CONTRACT.md'ye göre `ncp`, `n_total`, `actual_power`, `power`, `alpha` ve `beta` her modda ortak çıktı alanı; SPEC'te a-priori ve post-hoc modlarında bunların bir kısmı eksik.
- **Neden inandırıcıydı:** Sözleşmenin ilk okuması tam metinden değil, web sayfasının otomatik özetinden yapılmıştı. Özet "ortak alanlar" listesini mod ayrımı olmadan veriyordu.
- **Nasıl fark edildi:** CONTRACT.md'nin tam metni okundu. Bölüm 4.0 bu alanların hangi modda kullanıldığını ayrı ayrı yazıyor. Bölüm 4.1'deki mod tablosu SPEC ile uyuşuyor.
- **Yakalayan kanıt:** CONTRACT.md Bölüm 4.0 ve 4.1 (deney değil, belge karşılaştırması)
- **Doğrusu:** SPEC'teki mod bazında alanlar sözleşmeyle uyumlu.
- **Durum:** düzeltildi (geri bildirim notunun 6. maddesi değiştirildi)
- **Ders:** Özet üzerinden ayrıntılı iddia kurulmaz; birincil kaynak okunur.
