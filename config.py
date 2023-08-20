from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_NAME = getenv('DB_NAME')
TOKEN = getenv('TOKEN')
BOT_USERNAME = getenv('BOT_USERNAME')

WEEKDAY_LIMIT = 500
WEEKEND_LIMIT = 300
WEEK_LIMIT = WEEKDAY_LIMIT * 5 + WEEKEND_LIMIT * 2
FOUR_WEEK_LIMIT = WEEK_LIMIT * 4