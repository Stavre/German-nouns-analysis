import pandas as pd
"""pd.set_option('display.max_rows', 5)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)"""
from main import parse_dict

#get dictionary
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

############## check male gender #############################

# retrieve words that contain "{m}" in Word class definitions
m = df[df["Word class definitions"].str.contains("{m}", na=False)]

# retrieve words that contain not only {m}
m = m[m["Word class definitions"] != "{m}"]
# there are 1278 entries

# check how many categories are
options_m = set(list(m["Word class definitions"]))

# For a simpler analysis these categories will be deleted
# Another approach would have been to keep nouns with two genders and use the first one as the main gender
# However, this would lead to more complexity in the analysis

df.reset_index()
df.drop(df[df["Word class definitions"].isin(options_m)].index, inplace=True)
# 430849 rows left

########################### check female gender ###############################

# retrieve words that contain "{f}" in Word class definitions
f = df[df["Word class definitions"].str.contains("{f}", na=False)]

# retrieve words that contain not only {f}
f = f[f["Word class definitions"] != "{f}"]
# 167 entries were found. They will be deleted
options_f = set(list(f["Word class definitions"]))

df.reset_index()
df.drop(df[df["Word class definitions"].isin(options_f)].index, inplace=True)
# 430682 rows left


######################## check neutral gender  ###########################################


# retrieve words that contain "{n}" in Word class definitions
n = df[df["Word class definitions"].str.contains("{n}", na=False)]

# retrieve words that contain not only {n}
n = n[n["Word class definitions"] != "{n}"]
# 18 entries were found. They will be deleted

options_n = set(list(n["Word class definitions"]))

df.reset_index()
df.drop(df[df["Word class definitions"].isin(options_n)].index, inplace=True)
# 430664 rows left

################## delete plural entries ####################
df.drop(df[df["Word class definitions"] == "{pl}"].index, inplace=True)
# 388524 rows left

# drop NaN rows
df.dropna(inplace=True)
# 388316 rows left

# Check if there are other values on column Word class definitions besides {m}, {f}, and {n}
# df.drop(df[df["Word class definitions"].isin(options_f)].index, inplace=True)
df = df[df["Word class definitions"].isin(['{m}', "{f}", "{n}"])]
# 388311 rows left
