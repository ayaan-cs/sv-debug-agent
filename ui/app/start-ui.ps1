# Start the React app shell (expects API on http://127.0.0.1:8000)
Set-Location (Join-Path $PSScriptRoot "frontend")
if (-not (Test-Path "node_modules")) {
  npm install
}
npm run dev
