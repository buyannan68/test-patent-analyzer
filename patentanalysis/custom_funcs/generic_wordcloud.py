import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image

# def generate_wordcloud_by_freq(text):
#     wc = WordCloud(
#                 font_path='C:\Windows\Fonts\Arial.ttf',
#                 background_color="white",
#                 max_words=2000,
#                 max_font_size=100,
#                 random_state=42,
#                 )
#
#     alice_coloring = np.array(Image.open("alice_color.png"))
#     image_colors = ImageColorGenerator(alice_coloring)
#
#     wc.generate(text)
#     plt.figure()
#
#     plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
#     plt.axis("off")
#     # plt.show()
#
#     wc.to_file('wc.png')

def generate_wordcloud_by_freq(text, collection_id, field, algorithm):

    alice_coloring = np.array(Image.open("..\patentanalysis\custom_funcs\\alice_color.png"))

    algo = "native" if (algorithm == "Native") else "textrazor"

    wc = WordCloud(
                # mask= alice_coloring,
                font_path='C:\Windows\Fonts\Arial.ttf',
                width=700,
                height=200,
                background_color="white",
                max_words=2000,
                max_font_size=100,
                random_state=42,
                )


    # image_colors = ImageColorGenerator(alice_coloring)

    wc.generate_from_frequencies(text)
    plt.figure()

    # plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.imshow(wc)
    plt.axis("off")

    wc.to_file('..\patentanalysis\static\image\wordcloud\\' + str(collection_id) + "_" + algo + "_" + str(field) + '.png')


# import pandas as pd
# import re
#
# import MySQLdb
#
# conn = MySQLdb.connect(host="localhost",user="root",passwd="b2y25n14,db="mysite",charset="utf8")
#
# chemical_ref = pd.read_csv("C:\Users\U582788\Desktop\OTC\Analytics\APAC\Chemical.csv", usecols=[1])
# # chemical_ref = pd.read_csv("..\patentanalysis\custom_funcs\dicts\Chemical.csv", usecols=[1])
# chemical_ref["lowercase"] = chemical_ref.itemLabel.str.lower()
# chemical_ref["lowercase"] = " " + chemical_ref.lowercase + " "
#
# def extract(field, collection_id):
#     cur_field = field
#     # cur_field = 'title_dwpi'
#     # collection_id = 4
#     sql = "select pub_num, " + str(cur_field) + " from mysite.patentanalysis_publication as a inner join mysite.patentanalysis_pubcolrel as b on (a.id = b.publication_id) where b.collection_id = " + str(collection_id)
#     data_mysql = pd.read_sql(sql, conn, index_col="pub_num")
#
#     dic_list = {}
#
#     # import time
#     # start =time.clock()
#
#     for ind, line in enumerate(data_mysql[cur_field]):
#         patent = line
#         punc_to_remove = ".!;"   #to be added if more
#         pattern = r"[{}]".format(punc_to_remove)
#         patent = re.sub(pattern, " ", patent)
#         patent = patent.encode("gbk", "ignore")
#         patent = patent.replace(", ", " ")
#
#         match_word = [word for word in chemical_ref.lowercase if word in patent]
#         match_index = chemical_ref.index[chemical_ref.lowercase.isin(match_word)]
#
#         result = chemical_ref.itemLabel[chemical_ref.index.isin(match_index)]
#         if len(result) > 0:
#             for v in result.values:
#                 if v in dic_list.keys():
#                     dic_list[v] = dic_list[v] + 1
#                 else:
#                     dic_list[v] = 1
#             # print result.values, data_mysql.index[ind]
#
#     # end1 = time.clock()
#     # print "Running  " + str(end1 - start)
#
#     # dic_list = sorted(dic_list.items(), key=lambda d: d[1], reverse=True)
#
#     return dic_list
#
# generate_wordcloud_by_freq(extract('title_dwpi', 7), 7, 'title_dwpi')