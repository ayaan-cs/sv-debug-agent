# Start the local API that wraps sv_debug
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $PSScriptRoot
$env:PYTHONPATH = "$repoRoot;$PSScriptRoot"
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
