# Kurulum ve çalışma rehberi

Görev dağılımı için: [GOREV_DAGILIMI.md](GOREV_DAGILIMI.md). Her oturumun ilk prompt'u: [prompts/](../prompts/).

Herkes yalnızca kendi bölümündekini kurar. Komutlar Windows PowerShell içindir.

---

## Herkes

### 1. Git ve Python
```powershell
winget install --id Git.Git -e
winget install --id Python.Python.3.12 -e
```
Kurulumdan sonra PowerShell'i kapatıp yeniden açın, sonra kontrol edin:
```powershell
git --version
python --version
```

### 2. Repoya katılma
1. E-postanıza gelen GitHub davetini kabul edin.
2. Repoyu klonlayın:
   ```powershell
   cd $HOME
   git clone https://github.com/karafft/gpower-clone.git
   cd gpower-clone
   ```
3. Commit'lerin GitHub profilinize sayılması için adınızı ve GitHub'ın noreply e-postasını bu repoya ayarlayın. Noreply adresi GitHub → Settings → Emails sayfasında yazar (`12345678+kullaniciadi@users.noreply.github.com` biçiminde).
   ```powershell
   git config user.name "github-kullanici-adiniz"
   git config user.email "12345678+kullaniciadi@users.noreply.github.com"
   ```

### 3. Günlük git akışı
```powershell
git pull --rebase            # işe başlamadan önce
git add <yalnızca kendi dosyalarınız>
git commit -m "kısa ve ne yaptığını söyleyen mesaj"
git push
```
Kurallar:
- Herkes yalnızca kendi dosyalarını, kendi hesabıyla commit eder. Commit geçmişi temiz oda ayrımının kanıtıdır.
- `git push --force` kullanılmaz.
- `git add .` yerine dosya adı verin. Böylece GPower.exe, ekran görüntüsü klasörleri veya gizli dosyalar yanlışlıkla eklenmez.
- Küçük ve sık commit atın.

### 4. AI ajanı
Her birimiz kendi oturumunu ayrı açar ve `prompts/` altındaki kendi prompt'uyla başlatır. Oturum sonunda yaklaşık token kullanımını ve iterasyon sayısını AGENT_COST.md için not edin.

---

## Sude: inceleme ve doğrulama

### Kurulacaklar
| Araç | Nereden | Not |
|---|---|---|
| G*Power 3.1.9.7 (Windows) | Yalnızca resmi sayfa: psychologie.hhu.de → G*Power | Başka site, portable paket veya zip yok |
| JDK 21 | `winget install --id EclipseAdoptium.Temurin.21.JDK -e` | Ghidra için |
| Ghidra | ghidra-sre.org (veya NationalSecurityAgency/ghidra GitHub sürümleri) | Zip'i açın, `ghidraRun.bat` ile çalıştırın |
| Node.js LTS | `winget install --id OpenJS.NodeJS.LTS -e` | REA için `npx` gerekiyor |
| REA | `npx rea-agents setup` | Yalnızca github.com/morluto/rea, rea.tools ve npm'deki rea-agents. Benzer isimli paketler sahte. |
| statsmodels | `python -m pip install statsmodels scipy pandas` | 500'den fazla ölçek vektörü için |

### Klasör düzeni
İnceleme dosyaları repo dışında durur:
```
C:\Users\<siz>\YZM301-inceleme\
├── GPower\                  # G*Power kurulumu / GPower.exe
├── ghidra_projects\         # Ghidra proje dosyaları
├── rea_out\                 # REA çıktıları (ham)
└── private\                 # gizli [VAL] seti, değerlendirmeye kadar
```
Repoya yalnızca şunlar girer: `LEDGER.md`, `SPEC.md`, `oracle/vectors.csv`, `oracle/screenshots/`, `oracle/scale/`, `tests/test_differential.py`, `tests/reports/`. Ham döküm ve decompile çıktısı hiçbir zaman girmez.

### İlk işler
1. GPower.exe hash'i (README'ye girecek):
   ```powershell
   Get-FileHash "C:\Users\<siz>\YZM301-inceleme\GPower\GPower.exe" -Algorithm SHA256
   ```
2. G*Power "About" ekranının görüntüsü.
3. Ajana "REA araçları ve Ghidra sağlayıcısı bu oturumda kullanılabilir mi?" diye sorun; cevabın ekran görüntüsünü alın.
4. Oturumu `prompts/01_inceleme_spec_sude.md` ile başlatın.

Ekran görüntüleri `ORC-001.png`, `VAL-001.png` gibi kayıt kimliğiyle adlandırılır.

---

## Merve: motor ve CLI (temiz oda)

### Kurulacaklar
```powershell
python -m pip install scipy pytest
```
G*Power, Ghidra ve REA **kurulmaz**. LEDGER.md, `oracle/` ve ekran görüntüleri açılmaz.

### Temiz oda klasörü
AI oturumu repo klasöründe değil, ayrı bir klasörde açılır. Bu klasörde `.git` yoktur; böylece oturum, geçmiş commit'lerdeki kanıt dosyalarına da ulaşamaz.
```
C:\Users\<siz>\YZM301-temizoda\
├── SPEC.md          # repodan kopya
├── CONTRACT.md      # repodan kopya
├── pyproject.toml
├── src\gpower_clone\
│   ├── engine\
│   └── cli.py
└── tests\
    ├── test_engine.py
    └── test_cli_contract.py
```

SPEC.md güncellendiğinde repodan çekip kopyalayın:
```powershell
cd $HOME\gpower-clone
git pull --rebase
Copy-Item SPEC.md, CONTRACT.md $HOME\YZM301-temizoda\
```

Kodu repoya aktarıp commit edin:
```powershell
robocopy $HOME\YZM301-temizoda\src $HOME\gpower-clone\src /E
robocopy $HOME\YZM301-temizoda\tests $HOME\gpower-clone\tests test_engine.py test_cli_contract.py
Copy-Item $HOME\YZM301-temizoda\pyproject.toml $HOME\gpower-clone\
cd $HOME\gpower-clone
git add src tests\test_engine.py tests\test_cli_contract.py pyproject.toml
git commit -m "..."
git push
```

### Sürüm sabitleme
Testler geçince, değerlendirme için:
```powershell
git tag v0.1.0
git push origin v0.1.0
```
Etiketi ve commit hash'ini Sude'ye iletin. Değerlendirme bitene kadar kodu değiştirmeyin.

Oturumu `prompts/02_uygulama_merve.md` ile başlatın.

---

## Zeliha: repo, MCP ve ajan

### Kurulacaklar
| Araç | Komut | Not |
|---|---|---|
| GitHub CLI | `winget install --id GitHub.cli -e` | kurulu |
| MCP Python SDK | `python -m pip install mcp` | `power_analysis` aracı için |
| Ajan için LLM SDK | seçilen sağlayıcının Python paketi | API anahtarı `.env` içinde durur, repoya girmez |
| Ekran kaydı | Windows Game Bar (Win+G) veya OBS | 60 saniyelik CLI demosu |
| G*Power 3.1.9.7 | resmi sayfa | **Yalnızca motor dondurulduktan sonra**, GUI token karşılaştırması için |

### İlk işler
1. Sude ve Merve'yi Settings → Collaborators bölümünden davet edin.
2. Hocanın CONTRACT.md ve public_vectors.jsonl dosyalarını gist'ten indirip repoya ekleyin.
3. Oturumu `prompts/03_mcp_ajan_zeliha.md` ile başlatın.
4. MCP ve ajan kodu, bağımsız doğrulamada N için %90 eşleşme sağlandıktan sonra yazılır.

---

## Hiçbir zaman repoya girmeyenler
- GPower.exe, kurulum dosyaları, zip
- Decompile çıktısı, ham Ghidra/REA dökümleri
- `venv/`, `.env`, API anahtarları
- Gerçek hasta verisi
- Değerlendirmeden önce gizli [VAL] seti
