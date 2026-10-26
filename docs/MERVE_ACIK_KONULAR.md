> TARİHSEL NOT: Bu ilk paket kaydıdır; güncel durum TESLIM_DURUMU.md ve SPEC_ONERI.md içindedir.

# Merve açık konular

- SPEC arama limitlerini belirtmiyor. Geçici `MAX_N1=10,000,000` ve
  ters problem/pozitif eşik araması `MAX_DELTA=1,000,000` korumaları
  G*Power'dan gözlenmiş değildir; uygun limitler bekliyor.
- A-priori adaylarında `n1>=2`, `n2>=2` uygulanır; küçük `n2` adayları
  atlanır. CONTRACT örneklem alt sınırı ile SPEC'in pozitif tam sayı ifadesi
  arasındaki yorum Sude tarafından REA ile doğrulanmalıdır.
- `n2=ceil(n1*ratio)` ve en küçük uygun `n1` sağlanan SPEC'ten alınmıştır.
  Bunu destekleyen REA kimliği uygulama ajanına verilmemiştir.
- A-priori ve sensitivity için `power<=alpha` INCONSISTENT reddi CONTRACT
  örneğinden yorumlanmıştır; SPEC bu politikayı açıkça tanımlamaz.
- Aralık içinde fakat uç sayısal girdilerin reddedilme politikası kesinleşmedi.
  Sayısal korumalar ve NO_SOLUTION davranışı ürün gözlemi sayılmaz.
- Sayısal tolerans çatışmasında CONTRACT 1.0.0 önceliklidir: mutlak veya
  göreli 1e-6; tam sayılar kesin. Held-out oracle haricen çalıştırılmalıdır.

Sude'nin doğrulama sonuçları ve Zeliha'nın MCP entegrasyonu beklemektedir.
