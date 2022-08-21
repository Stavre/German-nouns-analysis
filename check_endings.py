import pandas as pd

"""pd.set_option('display.max_rows', 5)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)"""
from main import parse_dict

# get dictionary
# df = parse_dict("de_en_dictionary.txt")
df = pd.read_csv("dictionary.csv")

##############################################        DATA CLEANING       ##############################################


# removing unnecessary columns
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
# 867090 rows left

# we do not need Word class column anymore
df.drop(columns=["Word class"], inplace=True)


# removing entries with multiple words (eg. humanitäre Notlage )
df = df[~df["Word"].str.contains(" ", na=False)]
# 692929 rows left


# removing duplicate entries ( duplicate entries are those that have the same word and the same word class definition )
df.drop_duplicates(inplace=True)
# 432127 rows left

############## check genders #############################

# retrieve words that contain "{m}" in Word class definitions
m = df[df["Word class definitions"].str.contains("{m}", na=False)]


# retrieve words that contain not only {m}
m = m[m["Word class definitions"] != "{m}"]
# there are 1278 entries


# check how many categories are
options_m = set(list(m["Word class definitions"]))
# print(options_m)
# we notice following categories {'{m} {f} {n}', '{f} {m}', '{m} {f}', '{f} / Kleiner {m} / Kleines {n}', '{n} {m} {f}',
# '{n}  {m}', '{m} {f} {pl}', '{f} {n} {m}', '{f} / Bischofshut {m}', '{m} bei Nichtmelden {n}', '{m} {n}', '{m}  {f}',
# '{m} auf weltliche Güter {pl}', '{n} {m}', '{m} und Gestalt {f}', '{m} {pl}', '{f} {m} {n}', '{m} {n} {f}',
# '{f}; Gegenwall {m}', '{f}  {m}', '{m} Phoebe {f}', '{m} und Tigris {m}'}

# For a simpler analysis these categories will be deleted
# Another approach would have been to keep nouns with two genders and use the first one as the main gender
# However, this would lead to more complexity in the analysis


df.reset_index()
df.drop(df[df["Word class definitions"].isin(options_m)].index, inplace=True)
# 430849 rows left




# retrieve words that contain "{f}" in Word class definitions
f = df[df["Word class definitions"].str.contains("{f}", na=False)]


# retrieve words that contain not only {f}
f = f[f["Word class definitions"] != "{f}"]


# 167 entries were found. They will be deleted
options_f = set(list(f["Word class definitions"]))


df.reset_index()
df.drop(df[df["Word class definitions"].isin(options_f)].index, inplace=True)
# 430682 rows left




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

# change column name for easier usage
df.rename(columns = {"Word class definitions": "gender"}, inplace=True)


###########################################################  DATA ANALYSIS  #############################################################
# nouns ending in -ling, -ismus, -er, -ent, -and, -ant are masculine
# nouns ending in -heit, -keit, -ung, -ion, -in, -e, -schaft are feminine
# nouns ending in -chen, -lein, -tum, -um, -at, -o are neutral, according to
# Langenscheidt Go Smart Grammatik Deutsch, ISBN: 978-3-12-563297-4

# how many nouns are masculine, feminine, and neutral?
masculine_nouns = sum(df["gender"] == '{m}')
feminine_nouns = sum(df["gender"] == '{f}')
neutral_nouns = sum(df["gender"] == '{n}')

number_of_nouns = len(df.index)
print(masculine_nouns / number_of_nouns, feminine_nouns / number_of_nouns, neutral_nouns / number_of_nouns)
print(masculine_nouns / number_of_nouns + feminine_nouns / number_of_nouns + neutral_nouns / number_of_nouns)

# create dataframe for the analysis !!!!!!!!!! scrie mei explicit !!!!!!!!!!!!!!!
# ending,  gender it represents, number of nouns with that ending, number of nouns with that ending and with the gender
# it represents, number of nouns with that ending but with another gender

analysis = pd.DataFrame(columns=['ending', 'gender', 'good predictions', 'bad predictions'])

# fill the dataframe with noun endings and genders
dict = {
    "ending" : ["schaft", "ismus", "heit", "keit", "ling","chen", "lein", "tum" , "ent", "and", "ant", "ung", "ion", "in",  "um",   "at",  "er", "e",  "o"],
    "gender" : ["{f}",     "{m}",  "{f}" , "{f}",  "{m}" , "{n}" ,"{n}",  "{n}" , "{m}", "{m}", "{m}" ,"{f}", "{f}" ,"{f}" ,"{n}", "{n}" ,"{m}","{f}","{n}"]
}

analysis["ending"] = pd.Series(dict["ending"])
analysis["gender"] = pd.Series(dict["gender"])
analysis["good predictions"] = pd.Series([0] * len(dict["gender"]))
analysis["bad predictions"] = pd.Series([0] * len(dict["gender"]))

nouns_with_ending = []

for index_noun, noun in analysis.iterrows():
    words = df[df["Word"].str.endswith(noun["ending"])]
    nouns_with_ending.append(len(words.index))
    good_matches = sum(words["gender"] == noun["gender"])
    bad_matches = sum(words["gender"] != noun["gender"])
    analysis["good predictions"][index_noun] = good_matches
    analysis["bad predictions"][index_noun] = bad_matches

analysis["good predictions (%)"] = (analysis["good predictions"] / (analysis["good predictions"] + analysis["bad predictions"])) * 100
analysis["bad predictions (%)"] = (analysis["bad predictions"] / (analysis["good predictions"] + analysis["bad predictions"])) * 100
analysis["number of nouns"] = nouns_with_ending
analysis.sort_values(by=["good predictions (%)"], inplace=True, ascending=False)
print(analysis)



                
