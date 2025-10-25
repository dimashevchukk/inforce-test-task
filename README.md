

## Installation

```
git clone https://github.com/dimashevchukk/inforce-test-task.git
cd inforce-test-task
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
python manage.py migrate
python manage.py runserver
```

## Docker setup

```
docker-compose up --build
```

## Testing

To run all tests
```
python manage.py test
```

To test manually use registration and modheader
