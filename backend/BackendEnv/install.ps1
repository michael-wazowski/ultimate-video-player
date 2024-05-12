cd ..
python -m venv --copies BackendEnv
cd BackendEnv
./scripts/activate
pip install -r requirements.txt
$relativePath = Join-Path -Path $PWD -ChildPath "/ffmpeg/bin"
$env:Path += ";$relativePath"
$env:Path