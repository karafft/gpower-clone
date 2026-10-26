# Kaynak bağı: SPEC_ONERI.md ve docs/REA_STATIC_FINDINGS.md.
Feature: t2-indep kabul ölçütleri
  Scenario: Açık a-priori referansı
    Given tails1 d0.5 alpha0.05 power0.95 ratio1
    When CLI çalıştırılır
    Then tek JSON satırında n1 integer88 n2 integer88 n_total integer176 döner

  Scenario: Sürekli çözüm sonrası eşit olmayan tahsis
    Given tails2 d0.5 alpha0.05 power0.8 ratio1.3
    When sürekli çözüm ve REA yuvarlama hattı uygulanır
    Then n1 integer57 n2 integer73 n_total integer130 döner

  Scenario: Eşitlik
    Given a-priori power alpha ile tam eşit
    When girdiler diğer koşullara uygundur
    Then sırf eşitlik nedeniyle INCONSISTENT üretilmez

  Scenario: Eksik zorunlu oran
    Given a-priori ratio verilmemiş
    When CLI çalıştırılır
    Then tek JSON hata satırı MISSING_PARAM ve exit2 döner

  Scenario: Sözleşme türü
    Given post-hoc n1 değeri2.5
    When CLI çalıştırılır
    Then INVALID_VALUE n1 ve exit2 döner

  Scenario: İlgisiz alan
    Given post-hoc moduna power alanı eklenmiş
    When CLI çalıştırılır
    Then UNKNOWN_PARAM ve exit2 döner

  Scenario: Aralık uçları
    Given alpha veya power alt/üst uçta veya komşu float değerde
    When gözlenen kapsayıcı sınırlar doğrulanır
    Then1e-7 ve0.9999999 dahil, dış komşular OUT_OF_RANGE olur

# Bunlar okunabilir kabul senaryolarıdır; gerçek otomatik karşılıklar unittest dosyalarındadır.
