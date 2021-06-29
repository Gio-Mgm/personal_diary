from numpy.random import randint, uniform as u
import pandas as pd

df = pd.read_csv("./data/02/emotions.csv")

# ----------------------------- #
# ---- Dataframe for users ---- #
# ----------------------------- #

cols = [
    "name",
    "register_date",
    "city",
    "monitoring",
]

user_df = pd.DataFrame(columns=cols)

names_list = "Lily-Rose Cotton Tracey Mcdonald Tiah Hampton Burhan Marks Alasdair Cyrus".split(
    " ")
user_df.name = names_list
user_df.register_date = "2019-06-25"
user_df.city = "Lille"
user_df.monitoring = ""

# -------------------------------- #
# ---- Dataframe for messages ---- #
# -------------------------------- #

cols = [
    "user_id",
    "date",
    "text",
    "major",
    "anger",
    "fear",
    "fun",
    "happy",
    "hate",
    "love",
    "neutral",
    "sadness",
    "worry"
]
post_df = pd.DataFrame(columns=cols)

date = "2019-06-25"
i = 0
for j in range(20):
    if i / 10 == 1:
        i = 0
    s = df.sample(1)
    post_df.loc[j] = [
        randint(0, 10), date, 
        s.iloc[0]["text"], 
        s.iloc[0]["sentiment"], 
        u(), u(), u(), u(), u(), u(), u(), u(), u()
    ] 

post_df.to_csv('./data/03/posts.csv')
user_df.to_csv('./data/03/users.csv', index_label="id")
