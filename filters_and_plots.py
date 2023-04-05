import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, cycler
from matplotlib.pyplot import pie
import seaborn as sns
from parser import parse
from utilities import process_field, eval_word, get_ending, predicted_gender, process_tags, assign_to_dict

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

if __name__ == '__main__':
    ######################################### DATA FILTERING ####################################################
    path = "results"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
    dictionary = {
        "schaft": "{f}",
        "ismus": "{m}",
        "heit": "{f}",
        "keit": "{f}",
        "ling": "{m}",
        "chen": "{n}",
        "lein": "{n}",
        "ich": "{m}",
        "tum": "{n}",
        "ent": "{m}",
        "and": "{m}",
        "ant": "{m}",
        "ung": "{f}",
        "ion": "{f}",
        "ig": "{m}",
        "in": "{f}",
        "um": "{n}",
        "at": "{n}",
        "er": "{m}",
        "e": "{f}",
        "o": "{n}"
    }

    df = pd.read_csv("results/cleaned_data.csv")

    # np.nan is treated like a float
    df["field"] = df["field"].map(lambda x: process_field(x))
    print(df.head(15))
    df['field'] = df['field'].map(process_tags("resources/tags.txt"))

    prediction_type = list(df.apply(lambda row: eval_word(row["word"], row["gender"], dictionary), axis=1))
    # prediction_type = df.apply(lambda row: print(row), axis=1)
    df["good_predictions"] = list(map(lambda row: 1 if row == 0 else 0, prediction_type))
    df["bad_predictions"] = list(map(lambda row: 1 if row == 1 else 0, prediction_type))
    df["no_predictions"] = list(map(lambda row: 1 if row == 2 else 0, prediction_type))



    df["ending"] = df.apply(lambda row: get_ending(row["word"], dictionary), axis=1)
    df["predicted_gender"] = df.apply(lambda row: predicted_gender(row["word"], dictionary), axis=1)

    # save filtered data
    df.to_csv("results/filtered_data.csv", index=False)

    df = pd.read_csv("results/filtered_data.csv")

    #group by field
    h = df[["field", "word"]].groupby('field', as_index=False).count()

    h.to_csv("results/field_of_work.csv")

    # get top 10 fields by the number of words
    top_ten_fields = h.sort_values(by="word", ascending=False).head(17)

    rest_of_the_fields = df[~df['field'].isin(top_ten_fields.field)]
    rest_of_the_fields = rest_of_the_fields[["field", "word"]].groupby('field', as_index=False).count().sort_values(
        by="word", ascending=False)
    # print(rest_of_the_fields)
    #
    #
    # print(top_ten_fields)
    #
    # print(top_ten_fields.word.sum(), rest_of_the_fields.word.sum(), df.word.count())

    h = dict()




    top_ten_fields.apply(lambda x: assign_to_dict(x, h), axis=1)
    h['other groups'] = rest_of_the_fields.word.sum()

    # plt.pie(top_ten_fields.word, labels=top_ten_fields.field)
    data = list(top_ten_fields.word)
    data.append(rest_of_the_fields.word.sum())
    labels = list(top_ten_fields.field)
    labels.append('rest of the fields')

    theme = plt.get_cmap('bwr')
    plt.gca().set_prop_cycle("color", [theme(1. * i / 18) for i in range(18)])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Percentage of words grouped by field of work")
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.gcf().set_size_inches((12, 8), forward=False)
    plt.gcf().savefig("results/Percentage_of_words_grouped_by_field_of_work.png", dpi=500)

    plt.clf()

    t = df[['gender', 'good_predictions', 'bad_predictions', 'no_predictions']]

    t = t.groupby("gender").sum()



    plt.clf()
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Percentage_of_words_grouped_by_gender.png")
    plt.pie(t.sum(axis=1), labels=t.index, autopct='%1.1f%%', startangle=90)
    plt.gcf().set_size_inches((12, 8), forward=False)
    plt.gcf().savefig("results/Percentage_of_words_grouped_by_gender.png", dpi=500)

    plt.clf()
    t.T.plot(kind="pie", subplots=True, legend=False, autopct='%1.1f%%')
    plt.gcf().set_size_inches((12, 8), forward=False)
    plt.gcf().savefig("results/Percentage_of_predictions_grouped_by_gender.png", dpi=500)
    t.T.to_csv("results/Predictions_grouped_by_gender.csv")
    #plt.show()

    t = df[['field', 'gender', "ending", 'good_predictions', 'bad_predictions', 'no_predictions']]
    print(t.columns)
    t = t.groupby(by=['ending']).sum()


    total_number_of_words = df['field'].count()
    t['good_predictions % all_words'] = t["good_predictions"].apply(lambda x: (x / total_number_of_words) * 100)
    t['bad_predictions % all_words'] = t["bad_predictions"].apply(lambda x: (x / total_number_of_words) * 100)

    t[['good_predictions % all_words', 'bad_predictions % all_words']].plot(kind="bar", ylabel="%", title="Precentage of predictions out of the total number of words grouped by ending")
    plt.gcf().set_size_inches((17, 8), forward=False)
    plt.savefig("results/Precentage of predictions out of the total number of words grouped by ending.png".replace(" ", '_'), dpi=500)
    t.to_csv("results/Precentage of predictions out of the total number of words grouped by ending.csv".replace(" ", '_'))
    plt.clf()
    t = df[['field', 'good_predictions', 'bad_predictions', 'no_predictions']]

    t = t.groupby(by=['field'], as_index=False).sum()


    mask = t.field.apply(lambda x: any(item for item in list(top_ten_fields.field) if item in x))
    t = t[mask]
    t.set_index("field", inplace=True)
    t.plot(kind="bar", use_index=True, title="Number of predictions grouped by field of work")
    t.to_csv("results/Number of predictions grouped by field of work.csv".replace(" ", '_'))
    plt.gcf().set_size_inches((17, 8), forward=False)
    plt.savefig("results/Number of predictions grouped by field of work.png".replace(" ", '_'), dpi=500)
    plt.clf()







