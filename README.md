# ClasseVivaBot  [![Build Status](https://travis-ci.org/MarcoBuster/ClasseVivaBot.svg?branch=rewrite)](https://travis-ci.org/MarcoBuster/ClasseVivaBot)
_Telegram bot for the most popular electronic register in Italy_

### Installation
1. Install [Redis](https://redis.io/topics/quickstart) and [PostgreSQL](https://www.postgresql.org/download/).
2. Create a database and credentials on PostgreSQL.
3. Install **Python >3.6** and **pip** on your machine.
4. Create your own Telegram bot from [@BotFather](https://t.me/BotFather) and take note of the bot token
5. `$ <python executable> -m pip install -r requirements.txt`
6. Edit `config.sample.py` and rename it to `config.py`: 
    * `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `REDIS_PASSWORD` from **Redis** configuration.
    * `POSTGRESQL_DBNAME`, `POSTGRESQL_HOST`, `POSTGRESQL_PORT`, `POSTGRESQL_USER`, `POSTGRESQL_PASSWORD` from **PostgreSQL** configuration.
    * In `BOT_TOKEN` insert the Telegram Bot API token from **BotFather**.
    * In `SCHOOL_YEAR_BEGINNING` insert the school year's beginning date by editing the `dt(...)` object. _Note: the "day" param must be "1"._
    * In `SCHOOL_YEAR_END` insert the school year's ending date by editing the `dt(...)` object. _Note: the "day" param must be the last day of the month._
