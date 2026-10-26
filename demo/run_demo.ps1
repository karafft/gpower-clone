# 60 saniyelik CLI demosu: her adimda baslik, komut, cikti ve cikis kodu gosterilir.
# Calistirma (repo kokunden): powershell -ExecutionPolicy Bypass -File demo\run_demo.ps1

$root = Split-Path -Parent $PSScriptRoot
$py = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) { $py = "python" }

$steps = @(
    @{ title = "Surum bilgisi"; args = "--version" },
    @{ title = "A priori: orta etki (d=0.5), %80 guc, esit gruplar"; args = "--test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.8 --ratio 1" },
    @{ title = "A priori: esit olmayan gruplar (N2/N1 = 1.5)"; args = "--test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.8 --ratio 1.5" },
    @{ title = "Post hoc: her grupta 10 kisiyle ulasilan guc"; args = "--test t2-indep --mode post-hoc --tails 2 --d 0.8 --alpha 0.05 --n1 10 --n2 10" },
    @{ title = "Sensitivity: 100+100 kisiyle saptanabilen en kucuk etki"; args = "--test t2-indep --mode sensitivity --tails 2 --alpha 0.01 --power 0.95 --n1 100 --n2 100" },
    @{ title = "Gecersiz girdi: guc alfadan kucuk"; args = "--test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.03 --ratio 1" },
    @{ title = "Eksik parametre: ratio verilmedi"; args = "--test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.8" }
)

Clear-Host
Write-Host "gpower-clone: t2-indep guc analizi (CONTRACT 1.0.0)" -ForegroundColor Cyan
Write-Host ""

$i = 1
foreach ($s in $steps) {
    Write-Host "== $i) $($s.title)" -ForegroundColor Cyan
    Write-Host "> gpower-clone $($s.args)" -ForegroundColor Yellow
    & $py -m gpower_clone $s.args.Split(" ")
    Write-Host "(cikis kodu: $LASTEXITCODE)" -ForegroundColor DarkGray
    if ($i -lt $steps.Count) { Read-Host "Devam icin Enter" | Out-Null }
    Write-Host ""
    $i++
}
Write-Host "Demo bitti." -ForegroundColor Cyan
