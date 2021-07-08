import pandas as pd

df = pd.read_csv(
    "./data/01/emotions_full.csv",
    index_col=0,
    usecols=["text", "lemma", "sentiment"]#, "is_positive"]
)

#df["is_positive"] = np.where(df["is_positive"] == "Yes", 1, 0)
keeped = [
    'happy', 'sadness', 'worry', 'love'
]

df = df[df['sentiment'].isin(keeped)]
#df = df[df['sentiment'].isin(["happy", "sadness"])]

df.dropna(axis=0, inplace=True)

#df["feeling"] = df["sentiment"]

df.to_csv("./data/02/emotions_no_neutral.csv")
