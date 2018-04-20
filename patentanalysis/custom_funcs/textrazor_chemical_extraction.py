import pandas as pd
import re

import MySQLdb
import textrazor

conn = MySQLdb.connect(host="localhost",user="root",passwd="b2y25n14",db="mysite",charset="utf8")

keylist = ["00fb1d8fc6decc5632f09c4bb8b4bc0f92fefd005663d4e8b7d3c7e9", "4cec93786c4fc7f140c13ca2e94a95c138493d74ea5316921ccf2d8f"]

def remainCount():
    # count remaining usable times
    remain_count = 0

    for key in keylist:
        textrazor.api_key = key
        account_manager = textrazor.AccountManager()
        account_stat = account_manager.get_account()
        remain_usage = 500 - account_stat.requests_used_today

        remain_count = remain_count + remain_usage

    return remain_count

def extract(field, collection_id):

    cur_field = field

    remain = remainCount()
    # print remain

    # cur_field = 'title_dwpi'
    # collection_id = 7
    sql = "select pub_num, " + str(cur_field) + " from mysite.patentanalysis_publication as a inner join mysite.patentanalysis_pubcolrel as b on (a.id = b.publication_id) where b.collection_id = " + str(collection_id)
    data_mysql = pd.read_sql(sql, conn, index_col="pub_num")

    dic_list = {}

    # if remain < len(data_mysql[cur_field]):
    #     return False;

    textrazor.api_key = keylist[1] #can't be put outside function
    client = textrazor.TextRazor(extractors=["entities"]) #can't be put outside function

    i = 0

    try:
        for line in data_mysql[cur_field]:

            i = i + 1

            response = client.analyze(line)
            response_list = [(entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types) for entity in response.entities()]
            response_dataframe = pd.DataFrame(response_list, columns=["Entity", "Relevance Score", "Confidence Score", "Category"])
            response_dataframe = response_dataframe.drop_duplicates(subset="Entity", keep="first")
            response_result = response_dataframe[response_dataframe.Category.astype(str).str.contains("chem")]

            if len(response_result.values) > 0:
                for v in response_result.values:
                    val = v[0]
                    if val in dic_list.keys():
                        dic_list[val] = dic_list[val] + 1
                    else:
                        dic_list[val] = 1
    except Exception:
        print "except ",i, dic_list, Exception.message
    except textrazor.TextRazorAnalysisException:
        print "textrazor error ",i, dic_list, textrazor.TextRazorAnalysisException.message
    finally:
        # dic_list = sorted(dic_list.items(), key=lambda d: d[1], reverse=True)
        print i, dic_list

    return dic_list

# extract()
