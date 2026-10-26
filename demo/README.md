# CLI demosu

## Ekran kaydı (asıl demo)
- **YouTube:** https://youtu.be/vt77iAK14kM
- **Dosya:** [CLI_Demo_ekran_kaydi.mp4](CLI_Demo_ekran_kaydi.mp4)

Windows PowerShell'de gerçek terminal kaydı. Kayıtta `run_demo.ps1` betiği çalıştırılıyor. Betik yedi adımı sırayla gösteriyor ve her adımda komutu, JSON çıktısını ve çıkış kodunu ekrana basıyor:

1. Sürüm bilgisi (`--version`)
2. A priori, eşit gruplar: 64 + 64 (G*Power ORC-006 ile aynı)
3. A priori, N2/N1 = 1.5: 54 + 80 (ORC-010)
4. Post hoc, 10 + 10 kişi: güç 0.3950692 (ORC-028)
5. Sensitivity, 100 + 100 kişi: d 0.6019547 (ORC-031)
6. Güç α'dan küçük: `INCONSISTENT`, çıkış kodu 2
7. Eksik `ratio`: `MISSING_PARAM`, çıkış kodu 2

Yeniden çalıştırmak için repo kökünden:

```powershell
powershell -ExecutionPolicy Bypass -File demo\run_demo.ps1
```

## Açıklayıcı video
[CLI_Demo_60s.mp4](CLI_Demo_60s.mp4), gerçekten çalıştırılan beş komutun stdout kayıtlarından (`cli_transcript.json`) üretilmiş bir videodur; ekran kaydı değildir.

Yeniden üretim: Pillow ve imageio-ffmpeg kurulu bir ortamda
`python tools/build_demo.py --frames work/demo_frames --output demo/CLI_Demo_60s.mp4`
