docker stop hackathon2024-backend
docker rm hackathon2024-backend
docker image rm hackathon2024-backend
export FLASK_APP=manage.py
export FLASK_ENV=development
export SECRET=very_secret_string
docker build -t hackathon2024-backend .
docker run --env FLASK_APP --env FLASK_ENV --env SECRET -itd --name hackathon2024-backend -v .:/app -p 127.0.0.1:5011:5000 .
