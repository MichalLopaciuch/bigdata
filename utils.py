from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd


def company_freq(comp_names):
    comp_freq = Counter(comp_names).most_common()
    print(len(comp_freq), comp_freq[:10])

    dict_page_word_freq = {}
    for i in comp_freq:
        dict_page_word_freq[i[0]]=i[1]
    wordcloud = WordCloud(max_words=100).fit_words(dict_page_word_freq)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

def price_stats(filename):
    df = pd.read_csv(filename, delimiter=';', header=None)
    df.columns=['brand','price']

    print(f'mean price: {df["price"].mean().round(2)}')
