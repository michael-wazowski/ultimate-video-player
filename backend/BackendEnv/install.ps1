cd ..
py -m venv --copies BackendEnv
./BackendEnv/scripts/activate
pip install -r requirements.txt
$relativePath = Join-Path -Path $PWD -ChildPath "/BackendEnv/ffmpeg/bin"
$env:Path += ";$relativePath"
$env:Path