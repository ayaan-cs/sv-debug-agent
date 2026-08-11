# Run the upstream-master Streamlit snapshot
Set-Location $PSScriptRoot
python -m pip install -r requirements.txt | Out-Null
streamlit run app.py
