from pyaspeller import YandexSpeller
import pymorphy2
import random
import time
import requests
from bs4 import BeautifulSoup
from Levenshtein import ratio

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
    while tmp != -1:
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
        if (not q[i].isalpha()):
            q[i] = ' '
    q = ''.join(q)
    q = q.split()
    norm = []
    for i in range(len(q)):
        p = morph.parse(q[i])[0]
        # print(q[i], p.tag)
        if (q[i] == 'не') and (i < len(q) - 1):
            q[i + 1] = 'не' + ' ' + q[i + 1]
            continue
        DELETE = ['PREP', 'CONJ', 'INTJ']
        if all(d != p.tag.POS for d in DELETE):
            norm.append(normal_form(q[i]))
    return norm


def process(query):
    q = clear(query)
    res = []
    for el in q:
        res.append([el] + parse_synonyms(el)[:5])
        # print(f"{el} - {', '.join(parse_synonyms(el)[:10])}")
    return res


def parse_faq():
    # bs = ""
    f = open('parse.txt', 'r', encoding='utf8')
    lines = f.readlines()
    html_selected = [lines[2 * i + 2].rstrip('\n') for i in range(18)]
    # print(html_selected)
    # bs = ''.join(lines)
    f.close()
    # for i in range(18):
    # url = f'https://wink.ru/faq?selected={i}'
    # bs += '\n' + parse_url(url)
    # print(i)
    # print(bs)
    # f = open('parse.txt', 'w', encoding='utf8')
    # f.write(bs + '\n')
    # f.close()

    faq_list = []
    for selected in range(18):
        for i in range(300):
            tmp = html_selected[selected].find(f'"/faq/{i}"')
            tmp2 = html_selected[selected].find('root_r1lbxtse title_t1mrmeg6 root_header1_r1et8e7w')
            if tmp != -1:
                S = html_selected[selected][tmp + 15:tmp + 200]
                L = S.find('>')
                R = S.find('<')
                S2 = html_selected[selected][tmp2:tmp2 + 200]
                L2 = S2.find('>')
                R2 = S2.find('<')
                faq_list.append([selected, i, '*** ' + S2[L2 + 1:R2] + ' *** ' + S[L + 1:R]])
            # if (i == 1):
            # print(S)
    faq_list.sort()
    return (faq_list)


def compare(faq, syn_list):
    q = clear(faq[2])
    # print(q)
    CNT = 0
    for el in syn_list:
        CNT += min(1 - ratio(s1, s2) for s1 in el for s2 in q)
    # if faq[0] == 116 or faq[0] == 2:
    # print(faq, CNT)
    return CNT


faq_list = parse_faq()

while True:
    query = input()
    speller = YandexSpeller()
    query = speller.spelled(query)
    syn_list = process(query)
    faq_list.sort(key=lambda x: compare(x, syn_list))

    for el in faq_list[:10]:
        print(el, compare(el, syn_list))
    print('=====')
