import re
import sqlite3 as sl
from pyaspeller import YandexSpeller
import pymorphy2
import random
import time
import requests
from bs4 import BeautifulSoup
from Levenshtein import ratio


def normalize(s):
    morph = pymorphy2.MorphAnalyzer()
    st = set()
    opt = re.sub(r'[^\w\s]', '', s)
    for x in opt.split():
        p = morph.parse(x)[0]
        if morph.parse(x)[0].tag.POS not in ['NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']:
            st.add(p.normal_form.lower())
    return st


morph = pymorphy2.MorphAnalyzer()


def normal_form(word):
    p = morph.parse(word)[0]
    nf = p.normal_form[:7]
    return nf


def parse_url(url):
    time.sleep(0.5)
    head = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36 115Browser/8.3.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36 115Browser/8.6.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/31.0.1650.63 Safari/537.36 115Browser/5.2.6',
        'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.11) Gecko/20080109 (Charlotte/0.9t; http://www.searchme.com/support/)']
    headers = {
        'User-Agent': random.choice(head)}
    response = requests.get(url, headers=headers)
    r = response.text
    r = r.replace('\x00', '')
    # print(response)
    bs = BeautifulSoup(r, "lxml")
    return str(bs)


def parse_synonyms(word):
    RESULT = []
    url = f'https://sinonim.org/s/{word}'
    bs = parse_url(url)
    i = 1
    tmp = bs.find(f'id="as{i}"')
    while tmp != -1 and i <= 5:
        S = bs[tmp:tmp + 100]
        L = S.find('>')
        R = S.find('<')
        RESULT.append(' '.join(map(normal_form, S[L + 1:R].lower().split())))

        i += 1
        tmp = bs.find(f'id="as{i}"')
    return RESULT


def clear(q):
    q = list(q.lower())
    for i in range(len(q)):
        if not q[i].isalpha():
            q[i] = ' '
    q = ''.join(q)
    q = q.split()
    norm = []
    for i in range(len(q)):
        p = morph.parse(q[i])[0]
        # print(q[i], p.tag)
        if (q[i] == '????') and (i < len(q) - 1):
            q[i + 1] = '????' + ' ' + q[i + 1]
            continue
        DELETE = ['PREP', 'CONJ', 'INTJ']
        if all(d != p.tag.POS for d in DELETE):
            norm.append(normal_form(q[i]))
    return norm


def compare(faq, syn_list):
    q = clear(faq[1])
    # print(q)
    CNT = 0
    for el in syn_list:
        CNT += min(1 - ratio(s1, s2) for s1 in el for s2 in q)
    # if faq[0] == 116 or faq[0] == 2:
    # print(faq, CNT)
    return CNT


def process(query):
    q = clear(query)
    res = []
    for el in q:
        res.append([el] + parse_synonyms(el)[:5])
        # print(f"{el} - {', '.join(parse_synonyms(el)[:10])}")
    return res


def search_film_by_description(description):
    speller = YandexSpeller()
    description = speller.spelled(description)
    con = sl.connect('db.db')
    cur = con.cursor()
    result = cur.execute("SELECT * FROM ITEMS").fetchall()
    result = [[x[0], x[1] + " " + x[2] + " " + x[3]] for x in result]
    syn_list = process(description)
    result.sort(key=lambda x: compare(x, syn_list))

    # norm_request_set = normalize(description)
    # for el in result:
    # if len(normalize(el[2]).intersection(norm_request_set)) / len(norm_request_set) >= 0.5:
    # result_of_search[el[0]] = {'title': el[1], 'link': f'https://wink.ru/media_items/{el[0]}'}
    # return result_of_search
    # for el in result[:10]:
    #     print(compare(el, syn_list), el)
    # print('=====')
    return result[0]


print(search_film_by_description(input()))
