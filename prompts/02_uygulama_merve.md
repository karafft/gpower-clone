# Oturum 2: Temiz oda uygulaması (Merve)

İki bağımsız grup ortalaması için istatistiksel güç analizi yapan bir komut satırı aracı yazıyorum. Ekipteki diğer kişiler davranış şartnamesini ve bağımsız doğrulamayı hazırlıyor.

## Temiz oda kuralı
- Uygulanacak davranışın tek kaynakları bu klasördeki SPEC.md ve CONTRACT.md'dir. SPEC.md henüz yoksa onu bekle; hesaplama koduna başlama.
- İnceleme sohbetlerini, ham kanıtları, ekran görüntülerini, binary'yi veya decompile çıktısını isteme ve kullanma. SPEC.md'deki kanıt kimlikleri yalnızca referanstır; arkalarındaki kayıtlara ihtiyacın yok.
- SPEC.md eksik, belirsiz veya çelişkiliyse ilgili madde numarasıyla açıklama iste. Davranışı tahmin etme.
- "[Varsayım]" olarak işaretli kuralları uygula, ama kodda ve README'de varsayım olduklarını belirt.

## SPEC.md geldiğinde
1. **Kontrol:** Kapsamı ve uygulanabilirliği kontrol et. Eksik veya çelişkili maddeleri listele ve koda başlamadan önce bana sor.
2. **Motor:** Bütün hesaplama mantığını `src/gpower_clone/engine/` altında tek, bağımsız bir motorda yaz. Örneklem araması, yuvarlama, n1/n2 dağılımı, df, kritik değer, ncp ve güç burada hesaplanır. Motor dışarıya sade bir Python fonksiyonu sunar; CLI ve ileride MCP bu fonksiyonu çağırır.
3. **Kütüphane kuralı:** scipy.stats yalnızca dağılım fonksiyonları (t, merkezi olmayan t) için kullanılır. N araması, yuvarlama ve df hesabı kendi kodumuzdur; `scipy.optimize` ile N aranmaz.
4. **CLI:** `src/gpower_clone/cli.py` motoru çağıran ince bir katmandır. Görevi argüman okumak, doğrulamak ve çıktıyı biçimlendirmek; hesap yapmaz. Kurallar:
   - Komut adı `gpower-clone`. pyproject.toml'da console script olarak tanımlanır.
   - Başarıda stdout'a yalnızca tek satır JSON yazılır, çıkış kodu 0. Loglar stderr'e gider; `print` ile karşılama ya da hata ayıklama metni yazılmaz.
   - Tam sayı alanlar (`n1`, `n2`, `n_total`, `df`) JSON tam sayısıdır, `88.0` değil.
   - Ondalık alanlar yuvarlanmaz, tam double hassasiyetinde kalır.
   - Hata çıktısı tek satır `{"error": "...", "code": "...", "field": "..."}` olur.
   - Hata kodları SPEC'teki eşlemeye uyar: `MISSING_PARAM`, `UNKNOWN_PARAM`, `INVALID_VALUE`, `OUT_OF_RANGE`, `INCONSISTENT`, `UNSUPPORTED`, `NO_SOLUTION`.
   - Çıkış kodları: geçersiz girdide 2, beklenmeyen dahili hatada 1.
   - Varsayılan değer yoktur. Eksik alan da ilgisiz alan da hatadır.
   - `gpower-clone --version` sözleşmedeki JSON'u döndürür.
   - Her çağrı ağ erişimi olmadan 2 saniyenin altında biter ve deterministiktir.
5. **Testler:**
   - SPEC'teki Gherkin senaryolarını ve geliştirme örneklerini otomatik teste çevir: `tests/test_engine.py`, `tests/test_cli_contract.py`.
   - Matematiksel tutarlılık kontrolleri ekle. Örneğin güç N ile artmalı; d büyüdükçe N azalmalı; a-priori'de bulunan N post-hoc'a verildiğinde hedef güç ya da daha yüksek bir güç çıkmalı; N bir eksiltildiğinde güç hedefin altına düşmeli.
   - Sözleşme testleri: JSON tek satır mı, tam sayılar int mi, hata kodları ve çıkış kodları doğru mu?
6. **README:** Kurulum, kullanım, örnek çağrılar ve testlerin nasıl çalıştırılacağı.
7. **Sürüm sabitleme:** Testler geçince sürümü git etiketiyle sabitle (örn. `v0.1.0`) ve commit hash'ini bildir. Bağımsız değerlendirme bu sürümle yapılacak; o sırada kodu değiştirme.

## Kurallar
- Teslimde GPower.exe veya decompile çıktısı bulunmaz.
- Uygulamaya "G*Power" adını verme ve onu G*Power gibi sunma.
- Yerel testlerin geçmesini gizli test sonucu gibi sunma.
- AGENT_COST.md için not tut: yaklaşık token kullanımı, iterasyon sayısı, SPEC'te takıldığın yerler.
- SPEC'i yanlış anladığın ya da yanlış uyguladığın bir şey çıkarsa HALLUCINATIONS.md için kaydet.

## Sonraki aşama
Öncelik çalışan motor ve CLI. Bağımsız doğrulamadan sonra aynı motoru kullanan bir MCP sunucusu ve doğal dil ajanı eklenecek. O katmanlar motoru değiştirmeden, yalnızca çağırarak çalışacak. Bu yüzden motorun dış arayüzünü sade ve belgeli tut.

Şimdi SPEC.md'yi bekle.
