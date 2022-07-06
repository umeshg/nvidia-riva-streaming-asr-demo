python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

Download RIVA whl from NVIDIA RIVA developer portal and install
pip install ~/Downloads/riva_api-2.2.1-py3-none-any.whl


python manage.py migrate

Create .env under transcript folder and add 
TRANSCRIBE_API_BASE=api.xyz.com:port

python manage.py runserver

Go to localhost:8000 in browser and allow/give permission to mic. Mic audio data will stream to server via websocket and live speech to text / transcribe will happen.