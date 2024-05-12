# ultimate-video-player
The repository for the UoW COMPX241-24A project, Ultimate Video Player.

## Team Members

Project Manager: 
- Michael Peddie

Team Members: 
- Luke Fraser-Brown
- Jayden Litolff
- Shreyaa Senthil Kumar
- Jack Unsworth
- Leo Van Der Merwe

## How to run this weird stack
<code>cd web-app & npm install & npm run dev</code>

<code>cd backend && flask run --port 8000</code>


## Note for Jayden, how to expose the stack
- tailscale funnel -https 10000 127.0.0.1:8000
- tailscale funnel 127.0.0.1:5173

## How to get the pip venv list
pip freeze > requirements.txt

## Whisper not importing?
pip install -U openai-whisper