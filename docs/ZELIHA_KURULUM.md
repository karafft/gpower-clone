# Zeliha — gerçek MCP ve LLM ajanı

Motor değiştirilmedi. `mcp_server.py` resmi Python MCP SDK ile stdio sunucusudur;
`power_analysis` JSON parametrelerini ortak motora verir. Tek metin içerik
bloğu CLI JSON satırıyla (satır sonu hariç) birebir aynıdır; hata sonucu
`isError=true` taşır. Şema test/mode ve sayısal alanları ilan eder; eksik,
ilgisiz ve geçersiz girdilerde motorun aynı hatasını korumak için şema
reddi yerine ortak doğrulama kullanılır.

```powershell
python -m pip install '.[mcp]'
gpower-mcp
```

Sunucu stdout'u protokole ayrılmıştır; elle terminalde okunacak sohbet değildir.
Kaynakla çalıştırmak için src ve kurulu bağımlılıkları PYTHONPATH'a ekleyin.

## Gerçek sağlayıcıyla ajan

`agent.py` anahtar kelime ayrıştırıcısı değildir. Modelin Chat Completions
function çağrılarını alır, gerçek `ClientSession` stdio bağlantısında MCP'ye
iletir ve sonucu model konuşmasına geri verir. Eksik/belirsiz alanları sorması,
orta etki için d=0.5 önerisini açıkça belirtip onay istemesi ve sessiz
varsayılan kullanmaması sistem talimatındadır. Bu dil davranışının canlı
modelde kalitesi henüz ölçülmemiştir.

```powershell
$env:GPOWER_API_KEY='anahtari-yerel-olarak-ayarlayin'
$env:GPOWER_MODEL='hesabinizda-desteklenen-model'
gpower-agent --synthetic-case
```

Anahtarı dosyaya veya Git'e yazmayın. Anahtar sağlanmadan sağlayıcı çağrısı
yapılmaz. `GPOWER_ENDPOINT` veya `--endpoint` tam Chat Completions URL'sini
değiştirir; yalnız güvendiğiniz sağlayıcıya yöneltin, anahtar bu uç noktaya
gönderilir. Etkileşimli kullanım takip sorularını saklar; `--question` tek
tur içindir. Yalnız sentetik, kimliksiz örnekler kullanın; zorunlu
`--synthetic-case` bunu kullanıcı beyanı olarak kayda geçirir.

`agent_calls.jsonl` kaydı `ts,question,tool_input,tool_output,tokens_in,tokens_out`
alanlarını içerir. Sayılar gerçek sağlayıcı usage metadatasından gelir;
usage yoksa null, token tahmini yapılmaz. Aynı model yanıtının birden fazla
araç çağrısında usage yalnız ilk çağrıya atanır. Ayrı `llm_responses.jsonl`
tüm model yanıtlarını tutar; bu iki dosyanın tokenlarını toplayarak maliyet
çıkarmayın. API anahtarı MCP alt sürecinin ortamına aktarılmaz.
Loglarda soru içeriği bulunur. Canlı sağlayıcı erişimi/anahtar bu oturumda
kullanılmadığından gerçek LLM çalışma veya başarı iddiası yoktur.

API yapısı [resmi OpenAI Chat Completions belgesinden](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
ve [function calling akışından](https://developers.openai.com/api/docs/guides/function-calling)
doğrulanmıştır. API anahtarı keşif aracı mevcut değildi. Özel uç noktaların
uyumluluğu sağlayıcıya bağlıdır.

Chat Completions function-calling destekleyen bir model seçilmelidir.
Responses gerektiren modeller bu adaptörle uyumlu değildir; model adı için
sessiz varsayılan yoktur. İstemden gerçek tool-call seçimi ve açıklama üretimi
LLM'ye aittir; eksik bilgi davranışı canlı sağlayıcı değerlendirmesi bekler.

## Test

`python -m unittest discover -s tests -v` gerçek initialize, tools/list ve
tools/call alışverişini yeni stdio süreçte çalıştırır. `public_vectors.jsonl`
bulunduğunda tüm input satırlarını CLI ile tam JSON metin eşitliğinde
karşılaştırır. Ek geçersiz girdi örneklerini de kontrol eder. Bunlar MCP
protokol/taşıma testleridir; G*Power veya canlı LLM doğrulaması değildir.

25 Ekim yerel kontrolünde SDK 1.30.0 ile 25 public girdi ve dört ek hata
girdisi için gerçek stdio initialize/list/call ve CLI metin eşitliği geçti
(1 test, 10.971 saniye). Sonraki test genişletmesi yanlış tür/aralık
örnekleri ekledi; güncel toplam sonuç final test raporunda tutulur.
İki ajan testi de geçti (1.702 saniye): biri eksik anahtarda sağlayıcı çağrısı
yapılmadığını, diğeri açıkça mock sağlayıcı yanıtıyla gerçek MCP çağrı döngüsünü
kontrol eder. Mock test canlı LLM başarısı olarak yorumlanamaz.


Son bütünleşik çalıştırma: **12/12 test metodu geçti, 16.831 saniye**.
Gerçek MCP taşımasında 25 public + 8 geçersiz girdi = 33 satır tam CLI
metin eşitliği sağlandı. logs/mcp_parity.jsonl gerçek scripted sentetik
kontrol sonuçlarıdır; logs/zeliha_test_summary.json özeti tutar.
Canlı LLM çağrısı sıfırdır; agent_calls.jsonl canlı kayıt dosyası üretilmedi.
Windows --target geliştirme kurulumunda pywin32 için .deps/win32,
.deps/win32/lib ve .deps/pywin32_system32 yolları da PYTHONPATH ile verilmiştir.
Normal pip ortam kurulumunda pywin32 yol düzeni kurucu tarafından sağlanır.
