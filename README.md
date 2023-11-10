# Splitwise-Project

git clone https://github.com/shahilkk/Splitwise-Project

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

Use the following credentials:
Username: admin
Password: admin
Email: your.email@example.com


python manage.py runserver 8000

For celery run the code in celery_start.sh file
