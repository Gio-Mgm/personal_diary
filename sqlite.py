''' Creation and filling of database'''

from pathlib import Path
import sqlite3
import pandas as pd

DB = './database/diary.db'

Path(DB).touch()

conn = sqlite3.connect(DB)
c = conn.cursor()

# CR_T_POST  = '''
#     CREATE TABLE IF NOT EXISTS post (
#         post_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
#         date DATETIME NOT NULL ,
#         text TEXT NOT NULL,
#         major VARCHAR(20),
#         anger DECIMAL(1,5),
#         fear DECIMAL(1,5),
#         fun DECIMAL(1,5),
#         happy DECIMAL(1,5),
#         hate DECIMAL(1,5),
#         love DECIMAL(1,5),
#         neutral DECIMAL(1,5),
#         sadness DECIMAL(1,5),
#         worry DECIMAL(1,5),
#         user_id INT NOT NULL ,
#         CONSTRAINT fk_user_user_id FOREIGN KEY (user_id) REFERENCES user(user_id)
#     );
# '''

# CR_T_USER = '''
#     CREATE TABLE IF NOT EXISTS user (
#         user_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
#         name VARCHAR(50) NOT NULL,
#         email VARCHAR(50),
#         register_date DATETIME NOT NULL ,
#         city VARCHAR(50) NOT NULL,
#         monitoring TEXT
#     );
# '''

#c.execute(CR_T_POST)
#c.execute(CR_T_USER)


post_df = pd.read_csv('data/03/posts.csv')
post_df.to_sql('post', conn, if_exists='append')

user_df = pd.read_csv('data/03/users.csv')
user_df.to_sql('user', conn, if_exists='append')
