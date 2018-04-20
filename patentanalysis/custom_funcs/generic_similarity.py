import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import MySQLdb

conn = MySQLdb.connect(host="localhost",user="root",passwd="b2y25n14",db="mysite",charset="utf8")

# stop_words = pd.read_excel("C:\Users\U582788\Desktop\OTC\Analytics\APAC\Stop words.xlsx", sheetname="Sheet1", header=0)
stop_words = pd.read_excel("..\patentanalysis\custom_funcs\dicts\Stop words.xlsx", sheetname="Sheet1", header=0)
stop_words_list = stop_words["STOPWORD"].tolist()


# get comparison pool
def gen_comparison_pool(task_id, user_id, cur_field):

    sql = ""
    if task_id == -1: # All Tasks
        sql = "select pub_num, " + str(cur_field) + " from mysite.patentanalysis_publication as a inner join mysite.patentanalysis_pubcolrel as b on (a.id = b.publication_id)"
    elif task_id == 0: # All My Tasks
        sql = "select pub_num, " + str(cur_field) + " from mysite.patentanalysis_publication as a inner join mysite.patentanalysis_pubcolrel as b inner join mysite.patentanalysis_collection as c on (a.id = b.publication_id) and (c.id = b.collection_id) where user_id = " + str(user_id)
    else:
        sql = "select pub_num, " + str(cur_field) + " from mysite.patentanalysis_publication as a inner join mysite.patentanalysis_pubcolrel as b on (a.id = b.publication_id) where b.collection_id = " + str(task_id)

    data_mysql = pd.read_sql(sql, conn, index_col="pub_num")

    return data_mysql.index.values, data_mysql[cur_field]

# term frequency similarity
def find_similar(comparison_pool, user_input, threshold=None):
    # if patent in comparison pool
    # corpus = comparison_pool
    # patent_index = selected_patent.index

    # Michael - Get Comparison Pool data from database
    comparison_corpus_number, comparison_corpus = gen_comparison_pool(comparison_pool['task_id'], comparison_pool['user_id'], comparison_pool['cur_field'])

    # if patent not in comparison pool
    user_input = pd.Series(user_input)
    corpus = comparison_corpus.append(user_input, ignore_index=True)
    corpus = corpus.str.replace("\d+", "")
    patent_index = len(corpus) - 1

    count_vectorizer = CountVectorizer(analyzer="word", ngram_range=(1, 1), min_df=0, stop_words=stop_words_list)
    tm = count_vectorizer.fit_transform(corpus)


    # output top 20 words and frequency
    tm_dense = tm.todense()
    tm_vector = np.array(tm_dense[patent_index])[0]
    features = pd.DataFrame(count_vectorizer.get_feature_names(), columns=["word"])

    # ind = tm_vector.argsort()[-20:]
    ind1 = tm_vector.argsort()[-20:]
    ind2 = np.where(tm_vector > 0)[0]
    ind = list(set(ind1).intersection(set(ind2)))

    # ind = np.where(tm_vector > 5)[0]
    features_filter = features[features.index.isin(ind)]
    word_freq_table = features_filter.join(pd.DataFrame(tm_vector, columns=["frequency"]))


    # generate similarity matrix
    similarities = cosine_similarity(tm)
    vector = similarities[patent_index]

    # set default value for threshold
    threshold_default = 0.0
    for i in vector:
        count = len(np.where(vector > i)[0])
        if count == 6:
            threshold_default = i
    if threshold is None:
        threshold = threshold_default

    sim_index = np.where(vector > threshold)[0]
    sim_index = sim_index[sim_index != patent_index]
    sim_score = vector[sim_index]
    sim_pub_num = comparison_corpus_number[sim_index]
    sim_pub_score = pd.DataFrame({'score': sim_score, 'pub_num': sim_pub_num})
    sim_pub_score.sort_values(by=['score'], ascending=[0], inplace=True)
    return word_freq_table, sim_pub_score['pub_num'], sim_pub_score['score']

# comparison_pool = {'task_id': 0, 'user_id': 2, 'cur_field': 'abstract_dwpi'}
# user_input = """Composition for lamination comprises thiocarbonate linked to carboxylic acid reactive, polyol-polyisocyanate, polyol-polyisocyanate-polyol, polyol-carboxylic acid or epoxy-containing or thionyl chloride-hydroxy-containing curable compound
# """
# word_list, sim_pub_num, sim_score = find_similar(comparison_pool, user_input)
# print sim_pub_num, sim_score