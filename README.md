## Medical test task

###to run locally
```
cp deploy/docker-compose.override.sample.yml docker-compose.override.yml
cp deploy/local_settings.sample.py medical/local_settings.py
docker-compose up
pip install -r requirements.txt
python manage.py runserver
```

### for development environment
```
pip install -r requirements-dev.txt
```


###to load data from levels csv file
```
python manage.py load_levels -f 'file_name'
```

### docs are located on 
```
http://localhost:8000/swagger
```
and
```
http://localhost:8000/redoc/
```