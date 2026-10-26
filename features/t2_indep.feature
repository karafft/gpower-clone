# Kabul kriterleri: t2-indep
# Beklenen değerler G*Power 3.1.9.7 protokol çıktılarından (ORC kayıtları) ve CONTRACT.md'den gelir.
# Otomatik karşılıkları tests/ altındaki unittest dosyalarındadır.

Feature: t2-indep güç analizi CLI sözleşmesi

  Scenario: Açık referans vektörü, tek yönlü a-priori (ORC-001)
    Given test "t2-indep", mode "a-priori", tails 1
    And d 0.5, alpha 0.05, power 0.95, ratio 1
    When gpower-clone çalıştırılır
    Then stdout tek satır JSON olur ve çıkış kodu 0 olur
    And n1 88, n2 88, n_total 176, df 174 JSON tam sayısı olarak döner
    And ncp 3.3166248, critical_t 1.6536580, actual_power 0.9514254 değerleriyle 1e-6 içinde eşleşir

  Scenario: Eşit olmayan oran, n1*ratio tam sayı olsa bile ceil kuralı uygulanmaz (ORC-010)
    Given test "t2-indep", mode "a-priori", tails 2
    And d 0.5, alpha 0.05, power 0.80, ratio 1.5
    When gpower-clone çalıştırılır
    Then n1 54, n2 80, n_total 134 döner

  Scenario: Küsuratlı oranda tahsis (ORC-033)
    Given test "t2-indep", mode "a-priori", tails 2
    And d 0.5, alpha 0.05, power 0.80, ratio 1.3
    When gpower-clone çalıştırılır
    Then n1 57, n2 73, n_total 130 döner

  Scenario: Durma koşulu, hedef gücü sağlayan en küçük N (ORC-038, ORC-039)
    Given test "t2-indep", mode "a-priori", tails 2, d 0.5, alpha 0.05, ratio 1
    When power 0.8014 ile çalıştırılır
    Then n1 64, n2 64 döner
    When power 0.8015 ile çalıştırılır
    Then n1 65, n2 65 döner

  Scenario: Güç alfaya eşitse hata verilmez (ORC-046)
    Given test "t2-indep", mode "a-priori", tails 2
    And d 0.5, alpha 0.05, power 0.05, ratio 1
    When gpower-clone çalıştırılır
    Then çıkış kodu 0 olur ve n1 2, n2 2, n_total 4 döner

  Scenario: Güç alfadan küçükse tutarsız girdi (ORC-047)
    Given test "t2-indep", mode "a-priori", tails 2
    And d 0.5, alpha 0.05, power 0.03, ratio 1
    When gpower-clone çalıştırılır
    Then code "INCONSISTENT", field "power" döner ve çıkış kodu 2 olur

  Scenario: Post-hoc gücü (ORC-028)
    Given test "t2-indep", mode "post-hoc", tails 2
    And d 0.8, alpha 0.05, n1 10, n2 10
    When gpower-clone çalıştırılır
    Then df 18 ve power 0.3950692 değeri 1e-6 içinde döner

  Scenario: Eksik zorunlu alan
    Given test "t2-indep", mode "a-priori" ve ratio verilmemiş
    When gpower-clone çalıştırılır
    Then code "MISSING_PARAM", field "ratio" döner ve çıkış kodu 2 olur

  Scenario: Modla ilgisiz alan
    Given test "t2-indep", mode "post-hoc" ve ek olarak power 0.8 verilmiş
    When gpower-clone çalıştırılır
    Then code "UNKNOWN_PARAM", field "power" döner ve çıkış kodu 2 olur

  Scenario: Tam sayı olması gereken alanda ondalık (ORC-059)
    Given test "t2-indep", mode "post-hoc", n1 2.5, n2 10
    When gpower-clone çalıştırılır
    Then code "INVALID_VALUE", field "n1" döner ve çıkış kodu 2 olur
    # G*Power bu girdiyi sessizce 3'e yuvarlayıp hesaplıyor; sözleşme tam sayı istediği için CLI reddeder.

  Scenario: Negatif etki büyüklüğü (ORC-050)
    Given test "t2-indep", mode "a-priori", d -0.5
    When gpower-clone çalıştırılır
    Then code "OUT_OF_RANGE", field "d" döner ve çıkış kodu 2 olur
    # G*Power negatif d ile hesap yapıyor; sözleşme d > 0 istediği için CLI reddeder.

  Scenario Outline: G*Power'ın kabul aralıkları (ORC-049, ORC-051 – ORC-057)
    Given test "t2-indep", mode "a-priori" ve <alan> = <değer>
    When gpower-clone çalıştırılır
    Then code "OUT_OF_RANGE", field "<alan>" döner ve çıkış kodu 2 olur

    Examples:
      | alan  | değer      | G*Power sınırı           |
      | alpha | 0.00000001 | [1e-7, 0.9999999]        |
      | ratio | 0.005      | [0.01, 100]              |
      | d     | 0.000005   | a-priori'de \|d\| ≥ 1e-5 |

  Scenario: Kapsam dışı test ailesi
    Given test "t-paired"
    When gpower-clone çalıştırılır
    Then code "UNSUPPORTED", field "test" döner ve çıkış kodu 2 olur
