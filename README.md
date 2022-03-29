# telegram_bot
Create session: `docker-compose run telegram_bot python3 create_session.py`
Create database:
```
$ docker-compose up -d & docker-compose run db psql -h db -U postgres

# CREATE DATABSSE {{YOUR_DB_NAME}};

# \c {{YOUR_DB_NAME}};

And create tables with sql commands from https://github.com/tardigrada-agency/sql-scheme

```
