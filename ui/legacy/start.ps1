# Legacy one-file Streamlit app (agent + UI)
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $repoRoot
streamlit run legacy.py
