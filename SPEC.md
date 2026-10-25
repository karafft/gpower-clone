# YZM301 Clean Room Spesifikasyonu: t2-indep

**Yazar:** Sude Naz Öztoprak (Analist / REA Lead)  
**Tarih:** 25 Ekim 2026  
**Hedef Modül:** `t2-indep` (İki Bağımsız Örneklem t-Testi)  
**Kaynak:** G*Power 3.1.9.7 Davranışsal Analizi (Black-Box REA)  

Bu belge, Temiz Oda (Clean Room) kuralı gereğince G*Power kaynak kodu veya ikili kodlarına bakılmaksızın, yalnızca girdi/çıktı davranışları ve standart istatistiksel literatür temel alınarak hazırlanmıştır. Motor geliştiricisi (Merve) hesaplama mantığını bu şartnameye birebir uygun kurmalıdır.

---

## 1. Genel Matematiksel Temeller ve Dağılımlar

* **Kullanılacak Kütüphane:** `scipy.stats` (`t` ve `nct` fonksiyonları).
* **Serbestlik Derecesi ($df$):**
  $$df = n_1 + n_2 - 2$$
  *(Her zaman tamsayı / integer).*

* **Non-centrality Parametresi ($\delta$ / ncp):**
  $$\delta = d \cdot \sqrt{\frac{n_1 \cdot n_2}{n_1 + n_2}}$$

* **Kritik t Değeri ($t_{crit}$):**
  Standart t-dağılımının ters kümülatif fonksiyonu (`scipy.stats.t.ppf`):
  * Tek yönlü (`tails = 1`): $t_{crit} = t.ppf(1 - \alpha, df)$
  * Çift yönlü (`tails = 2`): $t_{crit} = t.ppf(1 - \alpha / 2, df)$

* **Güç (Power) Hesabı:**
  Non-central t-dağılımının kümülatif dağılım fonksiyonu (`scipy.stats.nct.cdf`):
  * Tek yönlü:
    $$Power = 1 - nct.cdf(t_{crit}, df, \delta)$$
  * Çift yönlü:
    $$Power = 1 - nct.cdf(t_{crit}, df, \delta) + nct.cdf(-t_{crit}, df, \delta)$$
  *(Tipik olarak $\beta = 1 - Power$ olarak tanımlanır).*

---

## 2. Modlara Göre Girdi, Çıktı ve Hesaplama Kuralları

### Mod 1: `a-priori`
* **Girdiler:** `d` (float), `alpha` (float), `power` (float), `ratio` (float, $N_2/N_1$), `tails` (int, 1 veya 2).
* **Çıktılar:** `ncp` (float), `critical_t` (float), `df` (int), `n1` (int), `n2` (int), `n_total` (int), `actual_power` (float).
* **Algoritma Mantığı:**
  1. $Power(n_1, n_2) \ge target\_power$ eşitsizliğini sağlayan en küçük pozitif $n_1$ tamsayısı aranır (İkili arama / Binary search veya ardışık tarama).
  2. Her adımda ikinci grup tamsayıya yuvarlanır: $n_2 = \lceil n_1 \cdot ratio \rceil$ (tavan/ceil).
  3. $n_{total} = n_1 + n_2$ ve $df = n_1 + n_2 - 2$.
  4. Bulunan optimal $n_1, n_2$ ile elde edilen net güç `actual_power` alanına atanır.

### Mod 2: `post-hoc`
* **Girdiler:** `d` (float), `alpha` (float), `n1` (int), `n2` (int), `tails` (int, 1 veya 2).
* **Çıktılar:** `ncp` (float), `critical_t` (float), `df` (int), `power` (float).
* **Algoritma Mantığı:**
  1. $df = n_1 + n_2 - 2$ hesaplanır.
  2. Verilen $n_1, n_2, d$ ile $\delta$ (ncp) hesaplanır.
  3. $\alpha$ ve $df$ üzerinden $t_{crit}$ belirlenir.
  4. $nct.cdf$ ile elde edilen güç doğrudan `power` alanına atanır.

### Mod 3: `compromise`
* **Girdiler:** `d` (float), `beta_alpha_ratio` (float, $q = \beta / \alpha$), `n1` (int), `n2` (int), `tails` (int, 1 veya 2).
* **Çıktılar:** `ncp` (float), `critical_t` (float), `df` (int), `alpha` (float), `beta` (float), `power` (float).
* **Algoritma Mantığı:**
  1. $\beta / \alpha = q$ oranını ve verilen $n_1, n_2$ değerlerini sağlayacak optimal kritik eşik ($t_{crit}$) kök bulma yöntemiyle çözülür.
  2. Bu eşiğe karşılık gelen $\alpha$ ve $\beta$ değerleri hesaplanır ($Power = 1 - \beta$).

### Mod 4: `criterion`
* **Girdiler:** `d` (float), `power` (float), `n1` (int), `n2` (int), `tails` (int, 1 veya 2).
* **Çıktılar:** `ncp` (float), `critical_t` (float), `df` (int), `alpha` (float).
* **Algoritma Mantığı:**
  1. Hedef gücü verecek $t_{crit}$ değeri `scipy.optimize.brentq` veya ters kök bulma ile çözülür.
  2. Bulunan $t_{crit}$ değerinden standart t dağılımı kullanılarak gereken $\alpha$ hesaplanır:
     * Tek yönlü: $\alpha = 1 - t.cdf(t_{crit}, df)$
     * Çift yönlü: $\alpha = 2 \cdot (1 - t.cdf(t_{crit}, df))$

### Mod 5: `sensitivity`
* **Girdiler:** `alpha` (float), `power` (float), `n1` (int), `n2` (int), `tails` (int, 1 veya 2).
* **Çıktılar:** `ncp` (float), `critical_t` (float), `df` (int), `d` (float).
* **Algoritma Mantığı:**
  1. $\alpha$ ve $df$ ile $t_{crit}$ belirlenir.
  2. Hedef gücü sağlayan non-centrality parametresi $\delta$ kök bulma ile bulunur.
  3. Etki büyüklüğü tersine çözülür: $d = \delta / \sqrt{\frac{n_1 \cdot n_2}{n_1 + n_2}}$.

---

## 3. Katı Tip ve Biçimlendirme Kuralları

1. **JSON Tamsayı Zorunluluğu:** `df`, `n1`, `n2`, `n_total` alanları kesinlikle JSON tamsayısı (integer) olmalıdır (`128` geçerli, `128.0` geçersizdir).
2. **Hassasiyet ve Tolerans:** Sayısal float değerleri (ncp, critical_t, actual_power, power, alpha, beta, d) en az 6-7 ondalık basamak hassasiyetle hesaplanmalı ve `ground_truth.json` ile en az $\pm 10^{-4}$ bağıl hata toleransı içinde kalmalıdır.
3. **Standart Çıktı:** Motor veya CLI çağrıldığında `stdout`'a tek satır saf JSON basmalıdır. Debug logları `stderr`'e yönlendirilmelidir.

---

## 4. Akademik Atıf ve Referans

Bu şartnamede yer alan davranışsal analizler ve doğrulama vektörleri, Heinrich Heine Üniversitesi Düsseldorf tarafından geliştirilen **G*Power 3.1.9.7** yazılımı üzerinden kara kutu (black-box) yöntemiyle elde edilmiştir.

* **Yazılım Referansı:**
  Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods*, 39, 175–191.