import pandas as pd
import re

import MySQLdb

conn = MySQLdb.connect(host="localhost",user="root",passwd="b2y25n14",db="mysite",charset="utf8")

# chemical_ref = pd.read_csv("C:\Users\U582788\Desktop\OTC\Analytics\APAC\Chemical.csv", usecols=[1])
chemical_ref = pd.read_csv("..\patentanalysis\custom_funcs\dicts\Chemical.csv", usecols=[1])
chemical_ref["lowercase"] = chemical_ref.itemLabel.str.lower()
chemical_ref["lowercase"] = " " + chemical_ref.lowercase + " "

def extract(field, collection_id):
    cur_field = field
    # cur_field = 'title_dwpi'
    # collection_id = 4
    sql = "select pub_num, " + str(cur_field) + " from mysite.patentanalysis_publication as a inner join mysite.patentanalysis_pubcolrel as b on (a.id = b.publication_id) where b.collection_id = " + str(collection_id)
    data_mysql = pd.read_sql(sql, conn, index_col="pub_num")

    dic_list = {}

    # import time
    # start =time.clock()

    for ind, line in enumerate(data_mysql[cur_field]):
        patent = line
        punc_to_remove = ".!;"   #to be added if more
        pattern = r"[{}]".format(punc_to_remove)
        patent = re.sub(pattern, " ", patent)
        patent = patent.encode("gbk", "ignore")
        patent = patent.replace(", ", " ")

        match_word = [word for word in chemical_ref.lowercase if word in patent]
        match_index = chemical_ref.index[chemical_ref.lowercase.isin(match_word)]

        result = chemical_ref.itemLabel[chemical_ref.index.isin(match_index)]
        if len(result) > 0:
            for v in result.values:
                if v in dic_list.keys():
                    dic_list[v] = dic_list[v] + 1
                else:
                    dic_list[v] = 1
            # print result.values, data_mysql.index[ind]

    # end1 = time.clock()
    # print "Running  " + str(end1 - start)

    # dic_list = sorted(dic_list.items(), key=lambda d: d[1], reverse=True)

    return dic_list

# print extract('abstract_dwpi', 7)