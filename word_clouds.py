from wordcloud import WordCloud
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("results/filtered_data.csv")
t = df.groupby(by=['field'], as_index=False).count()
print(t)
text = dict(zip(t.field, t.word))
print(text)

# Create and generate a word cloud image:
wordcloud = WordCloud(width=1600, height=800).generate_from_frequencies(text)


# Display the generated image:
plt.figure( figsize=(20,10) )
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
#plt.show()
plt.savefig("results/word_cloud_field_of_work_frequency.png")