# Son doğrulama raporu

26 Ekim2026;1.1.0rc4 / final denetim. Kaynak ve kanıtlar repoya yüklendi.

| Kontrol | Sonuç | Kayıt |
|---|---|---|
| Yazılım, gerçek MCP dahil |25/25 test geçti |tests/reports/final_audit_unit.txt |
| MCP/CLI |33/33 tam metin eşdeğerliği |logs/mcp_parity.jsonl |
| Açık sayısal vektörler |5/5 t2-indep;20 başka aile dışlandı |tests/reports/final_audit_public.json |
| Sude özgün görsel destekli set |57/57;37/37 N |tests/reports/final_audit_screenshots57.json |
| ORC-011 yeni gerçek koşum |96/48, toplam144; ayrıca karşılaştırıldı |oracle/replays/vectors.jsonl |
| Görsel destekli tamamlanmış set |58/58;38/38 N |tests/reports/final_audit_screenshots58.json |
| Yeni GUI takip seti |14/14;10/10 N |tests/reports/final_audit_prospective14.json |
| Sayısal çapraz kontrol |540/540; güç farkı en fazla5.55e-16 |oracle/scale/statsmodels_final_rc4.summary.json |
| Dosya bütünlüğü |Son denetim çıktısı |logs/final_file_audit.json |

Tam sayılar tam eşitlikle, diğer sayılar1e-6 mutlak/bağıl toleransla sınanır.
Hata kayıtları özgün GUI hata varlığını doğrular; GUI’nin CLI hata kodlarını
kullandığı iddia edilmez. ORC-050 ve059 GUI’de başarılı fakat CONTRACT dışında;
ikisi CLI eşdeğerliği paydasına alınmaz. Eski eksik ORC-011 PNG’si korunur,
yeni JPEG ayrı güncel tarihli tekrar deneyidir; eski görüntü gibi gösterilmez.

Motor core.py son denetimde değişmedi. Ajan yönergelerinin UTF-8 düzeltmesi
tüm kaynak hash’ini değiştirdi; eski/yeni hash SOURCE_FREEZE.json altında.
Önceden yapılmış14 GUI deneyinin dondurma kaydı tarihsel olarak korunur.

Yeni14 girdi önceki60 geliştirme kaydıyla örtüşmez; kör üçüncü taraf/gizli
yarışma testi değildir.540 karşılaştırma ortak SciPy altyapısı kullanabilir.
Mevcut kanıtlar tüm girdilerde doğruluk veya tüm makinelerde2s garantisi vermez.
Eski raporlar tarihsel dosyalardır; güncel koşumlar final_audit öneklidir.

Canlı model çağrısı0; doğal dil anlama başarısı ve gerçek token maliyeti
ölçülmedi. [Kalan gerçek ölçümler](docs/FINAL_AUDIT.md).
