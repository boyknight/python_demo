# -*- coding: utf-8 -*-

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba


if __name__ == '__main__':
    with open("sample.txt", encoding='utf-8') as f:
        sample_text = f.read()

    cut_text = " ".join(jieba.cut(sample_text))

    wordcloud = WordCloud(font_path='MicrosoftYaHeiMono.ttf').generate(cut_text)

    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


