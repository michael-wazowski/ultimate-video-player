cd ..
py -m venv --copies BackendEnv
./BackendEnv/scripts/activate
pip install -r ./BackendEnv/requirements.txt
$relativePath = Join-Path -Path $PWD -ChildPath "/BackendEnv/ffmpeg/bin"
$env:Path += ";$relativePath"
$env:Path