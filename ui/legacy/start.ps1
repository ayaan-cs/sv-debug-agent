# Legacy Streamlit UI
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $repoRoot
streamlit run ui/legacy/app.py
