export FLASK_APP=manage.py
export FLASK_ENV=development
export SECRET=very_secret_string
docker run -itd --name hackathon2024-backend -v .:/app .
