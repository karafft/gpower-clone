# Son sürümün540 ölçek karşılaştırması

Esas güncel dosya statsmodels_final_rc4.jsonl ve özeti
statsmodels_final_rc4.summary.json. Sürüm1.1.0rc4 ile540/540 kayıt üretildi,
hata0. Aynı tam sayı tahsisinde en büyük güç farkı
5.551115123125783e-16. Naif sürekli-n1 ceil yöntemiyle
231 tahsis farklı çıktı; bu G*Power uyumsuzluğu demek değildir.

Statsmodels da SciPy dağılımlarından yararlanabilir. Çalışma bağımsız bir
yüksek düzey kütüphane çapraz kontrolüdür, bağımsız sayısal altyapı ispatı
veya yeni GUI oracle'ı değildir. Ölçülen 4.124s importlardan
sonraki hesap döngüsüdür, CLI soğuk başlangıç süresi değildir.

Daha eski dosyalar önceki motor sürümlerinin tarihsel kontrolleridir.
Tekrar: python tools/generate_scale.py --output oracle/scale/local_statsmodels.jsonl
İsteğe bağlı bağımlılık: python -m pip install '.[scale]'.
