import pandas as pd
pd.set_option('display.max_rows', 50000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from main import parse_dict

# get dictionary
#df = parse_dict("de_en_dictionary.txt")
df = pd.read_csv("dictionary.csv")

# in this analysis we look at the nouns, their endings, and their gender
# removing all unnecessary columns
df = df[["Word", "Word class", "Word class definitions"]]
# 1240783 rows

# retrieve words that contain "noun" in Word class
df = df[df["Word class"].str.contains("noun", na=False)]
# 867121 rows left


# check how many categories there are
options = set(list(df["Word class"]))
# we notice six classes {'noun', 'adv noun', 'noun adj', 'adj noun', 'adj adv noun', 'noun adv'}
# we are interested only in nouns so we filter the dataset even more
df = df[df["Word class"] == "noun"]
# we get 867090 rows

# we do not need Word class column anymore
df.drop(columns=["Word class"], inplace=True)

# removing entries with multiple words (eg. humanitäre Notlage )
df = df[~df["Word"].str.contains(" ", na=False)]
# 692929 rows left

# removing duplicate entries ( duplicate entries are those that have the same word and the same word class definition )
df.drop_duplicates(inplace=True)
# 432127 rows left


############## check gender

# retrieve words that contain "{m}" in Word class definitions
m = df[df["Word class definitions"].str.contains("{m}", na=False)]

# check how many categories are
options_m = set(list(m["Word class definitions"]))
#print(options_m)

# we notice  '{n} {m} {f}', '{m} {f} {n}', '{f} {m} {n}', '{m} {n} {f}',  and '{f} {n} {m}'. These are not useful.
# 24 nouns were found with these genders
# All nouns with three genders will be removed
delete = ['{n} {m} {f}', '{m} {f} {n}', '{f} {m} {n}', '{m} {n} {f}', '{f} {n} {m}']
df = df[~df["Word class definitions"].isin(delete)]
# 432105 rows left
print(df)

#df.to_csv("dict", sep="_")


# retrieve words that contain "{m}" in Word class definitions
m = df[df["Word class definitions"].str.contains("{m}", na=False)]

# check how many categories are
options_m = set(list(m["Word class definitions"]))
#print(options_m)

# these groups were found
# '{m} bei Nichtmelden {n}', '{n} {m}', '{n}  {m}', '{m} {n}', '{f}  {m}', '{f} / Bischofshut {m}',
# '{f} / Kleiner {m} / Kleines {n}', '{f}; Gegenwall {m}', '{m} und Gestalt {f}', '{m} auf weltliche Güter {pl}',
# '{m} {f} {pl}', '{m}', '{f} {m}', '{m} und Tigris {m}', '{m} {pl}', '{m} Phoebe {f}', '{m} {f}', '{m}  {f}'

# Some of them are virtually identical ('{n} {m}' and '{n}  {m}', or '{m} {f}' and '{m}  {f}')
# Some have their order changed ('{n}  {m}' and '{m} {n}')

# Some special labels also appeared
# label                       no. of appearances
# '{m} Phoebe {f}'                   1
# {m} und Tigris {m}                 1
# {m} auf weltliche Güter {pl}       1
# {m} und Gestalt {f}                1
# {f}; Gegenwall {m}                 1
# {f} / Kleiner {m} / Kleines {n}    1
# {f} / Bischofshut {m}              1
# {m} bei Nichtmelden {n}            1






# check if nouns have gender
df = df[df["Word class definitions"].str.match("{f}|{m}|{n}", na=False)]
# we get 789421 rows




