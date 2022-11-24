import re
import sqlite3 as sl
import pymorphy2


def normalize(s):
    morph = pymorphy2.MorphAnalyzer()
    st = set()
    opt = re.sub(r'[^\w\s]', '', s)
    for x in opt.split():
        p = morph.parse(x)[0]
        if morph.parse(x)[0].tag.POS not in ['NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']:
            st.add(p.normal_form.lower())
    return st


def search_film_by_description(description):
    result_of_search = {}
    con = sl.connect('db.db')
    cur = con.cursor()
    result = cur.execute("SELECT * FROM ITEMS").fetchall()
    norm_request_set = normalize(description)
    for el in result:
        if len(normalize(el[2]).intersection(norm_request_set)) / len(norm_request_set) >= 0.5:
            result_of_search[el[0]] = {'title': el[1], 'link': f'https://wink.ru/media_items/{el[0]}'}
    return result_of_search


print(search_film_by_description(input()))