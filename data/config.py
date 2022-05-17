import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN=str(os.getenv('BOT_TOKEN'))


admins=[
    644812536
]

ip=os.getenv('ip')
PGUSER=str(os.getenv('PGUSER'))
PGPASSWD=str(os.getenv('PGPASSWD'))
DATABASE=str(os.getenv('DATABASE'))


POSTGRES_URI=f'postgresql://{PGUSER}:{PGPASSWD}@{ip}/{DATABASE}'