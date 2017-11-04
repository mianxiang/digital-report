#encoding=utf-8

import jieba.analyse
import lxml.html
import urllib2
import os
import jieba
from collections import Counter
from scipy.misc import imread
from wordcloud import wordcloud, ImageColorGenerator
import matplotlib.pyplot as plt

def download19report(url = "http://news.xinhuanet.com/politics/19cpcnc/2017-10/27/c_1121867529.htm"):
    reportfile = "19dareport.txt"

    if os.path.exists(reportfile) and os.stat(reportfile).st_size > 0:
        with open(reportfile, "r") as fsr:
            return fsr.read()
    else:
        htmlcontent = urllib2.urlopen(url).read()
        tree = lxml.html.fromstring(htmlcontent)
        reportcontent = tree.cssselect("div#content")[0].text_content()
        with open(reportfile, "w") as fsw:
            fsw.write(reportcontent.encode("utf-8"))
        return reportcontent

def getkeywords(reportcontent):
    filteredwords = [u"，", u"、", u"的", u"。", u"和", u"	", u"”", u"；", u"　",
                     u"“", u"！", u"○", u"\r\n", u"）", u"（", u"了", u"以", u"把",u"在", u"要", u"新", u"为", u"是"]
    keywords = jieba.cut(reportcontent)
    data = dict(Counter(keywords))
    for filterword in filteredwords:
        data.pop(filterword, None)
    #return sorted(data.items(), key=lambda d:d[1], reverse=True)
    return data

def preparedata(keywords):
    keyworddatafile = "keyworddata.txt"

    try:
        with open(keyworddatafile, "w+") as fs:
            for keyword, times in keywords[0:100]:
                fs.write("{}\n".format(keyword.encode("utf-8")))
        return keyworddatafile
    except OSError as error:
        print(error)
        return None

def wordcloudshow(keywordsfrequency):
    background_image = imread("heart.jpg")
    wordcloudobject = wordcloud.WordCloud(font_path="/library/fonts/microsoft/simsun.ttf",
            mask=background_image,
            background_color="white",
            max_font_size=300,
            random_state=30).generate_from_frequencies(keywordsfrequency, 200)

    image_colors = ImageColorGenerator(background_image)
    wordcloudobject.recolor(color_func=image_colors)
    plt.imshow(wordcloudobject)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    reportcontent = download19report()
    wordcloudshow(getkeywords(reportcontent))



