# Launch SV Debug Agent as a native desktop window
Set-Location $PSScriptRoot

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
if (-not (Test-Path (Join-Path $repoRoot ".env")) -and (Test-Path (Join-Path $repoRoot ".env.example"))) {
  Copy-Item (Join-Path $repoRoot ".env.example") (Join-Path $repoRoot ".env")
}

Set-Location $repoRoot
python -m pip install -r requirements.txt | Out-Null
Set-Location $PSScriptRoot
python desktop_app.py
