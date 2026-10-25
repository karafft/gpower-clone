# Ajan değerlendirme seti

`agent_questions.jsonl`: 10 kurgusal Türkçe klinik soru. Hiçbiri gerçek bir hastaya ya da çalışmaya ait değil.

| Alan | Anlamı |
|---|---|
| `id` | Soru kimliği |
| `question` | Ajana verilen soru |
| `expected_label` | Beklenen test ailesi: `t2-indep`, `t-paired`, `anova-oneway`, `chi2-contingency`, `multireg-r2`, `ambiguous`, `unsupported` |
| `expected_action` | `call_tool` (aracı çağır), `state_assumption_or_ask` (varsayımı açıkça söyle ya da onay iste), `ask_user` (önce sor), `report_unsupported` (kapsam dışı olduğunu söyle) |
| `expected_tool_input` | Ajanın `power_analysis` aracına vermesi beklenen girdiler |
| `expected_n` / `expected_power` | G*Power'dan gözlenen sonuç |
| `evidence` | Beklenen sonucun alındığı G*Power ekran görüntüsünün kimliği (ORC / VAL) |
| `note` | Sorunun neyi sınadığı |

`expected_n`, `expected_power` ve `evidence` alanları henüz boş. Bunları G*Power arayüzünden Sude dolduracak. Beklenen değerler bizim motorumuzdan alınmaz; yoksa değerlendirme kendi kendini doğrulamış olur.

Raporlanacaklar:
- aile seçiminde doğruluk (`expected_label`)
- davranışta doğruluk (`expected_action`)
- araç girdilerinde doğruluk (`expected_tool_input`)
- N veya güçte tam eşleşme
