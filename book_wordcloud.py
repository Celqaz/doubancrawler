from wordcloud import WordCloud
import matplotlib.pyplot as plt
# import jieba

f = open(u'authors.txt','r',encoding='UTF-8').read()

# cut_text = '\n'.join(jieba.cut(f))

wordcloud = WordCloud(
    font_path="Users/libin/Library/Fonts/SourceHanSerif-Regular.ttc",
    background_color="white",width=1600,height=900).generate(f)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()