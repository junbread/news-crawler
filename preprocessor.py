from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from koalanlp.Util import initialize, finalize
from koalanlp import API
from koalanlp.proc import SentenceSplitter, Tagger
from textrankr import TextRank

import hanja
import sys
import os
import re

def process(target):
        
    # remove bylines
    target = re.sub(r'\. *\S+ +\S+ +\w+@(\w+\.)+\w+', '.', target)
    target = re.sub(r'\S+ +\S+ +\w+@(\w+\.)+\w+', '.', target)

    # remove parentheses
    target = re.sub(r'\([^)]+\)', ' ', target)
    target = re.sub(r'\[[^)]+\]', ' ', target)
    target = re.sub(r'\<[^)]+\>', ' ', target)
    target = re.sub(r'\【[^)]+\】', ' ', target)

    # replace hanja to hangul
    hanja.translate(target, 'substitution')

    # remove special characters except necessary punctuations
    target = re.sub(r'[^A-Za-zㄱ-ㅎㅏ-ㅣ가-힣0-9\%\-\_\.\,\?\!\/\"\'ㆍ·。、“”‘’『』《》〈〉「」\~○×□…\ ]', ' ', target)

    # initialize korean language analyzers
    splitter = SentenceSplitter(API.HNN)
    tagger = Tagger(API.KHAIII, kha_resource="/usr/local/share/khaiii")

    # split text into sentences
    sentences = splitter(target)    

    # regularize sentences (ex: 해서->하여서)
    target_regularized = ''
    for sent in sentences:
        sent = tagger.tagSentence(sent)
        sent_regularized = []
        for word in sent[0].words:
            word_regularized = ''
            for m in word.morphemes:
                if m.tag.startswith('J'): # if 조사
                    word_regularized += ' ' # add space
                word_regularized += m.surface
            sent_regularized.append(word_regularized)
        target_regularized += '\n' + ' '.join(sent_regularized)
    
    # regularize whitespaces
    target_regularized = re.sub(r' +', ' ', target_regularized)

    return target_regularized

if len(sys.argv) != 3:
    print("Usage: python preprocessor.py <load_path> <save_path>")
    sys.exit()

initialize(KHAIII='LATEST', HNN='LATEST')

load_path = sys.argv[1]
save_path = sys.argv[2]

files = [f for f in os.listdir(load_path) if os.path.isfile(os.path.join(load_path, f)) and f.endswith("story")]
for fi in files:
    print('id: {}'.format(fi))
    with open(os.path.join(load_path, fi), 'r', encoding='utf-8') as f:
        # get title
        assert "@title\n" == f.readline()

        title = ""
        content = ""

        line = f.readline()
        while line != '@content\n':
            title += line
            line = f.readline()
        content = f.read()

    # specify skip target article titles (e.g. photo only articles)
    if any(x in title for x in ['포토','사진', '경향이 찍은 오늘']):
        print("skipped")
        continue

    # initialize html parser
    bs = BeautifulSoup(content, 'html.parser')
    
    # remove html tag
    content = ''
    summary = ''
    for elem in bs.children: # get article body
        if type(elem) is Tag: # html tag
            if elem.name == 'br':
                content += '\n'
            elif elem.name == 'p':
                content += elem.text + '\n'
            else:
                content += elem.text
        elif type(elem) is NavigableString: # plain text
            content += elem
    
    # get summary (the first paragraph of a article)
    flag_paragraph_change = False
    for sent in content.split('\n'):
        if len(sent.strip()) == 0: # newline
            flag_paragraph_change = True # if previous sentence is newline
            if not len(summary):
                continue
            else:
                break
        
        flag_paragraph_change = False
        if sent.strip().endswith('.'): # only if the sentence ends with '.' (full sentence)
            summary += sent

    # process text
    content = process(content)
    
    textrank = TextRank(content)
    summary = textrank.summarize()

    print(summary)

    # save processed files
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open(os.path.join(save_path, fi), 'w', encoding='utf-8') as f:
        f.write("@title\n")
        f.write(title.strip() + "\n")
        f.write("@summary\n")
        f.write(summary.strip() + "\n")
        f.write("@content\n")
        f.write(content.strip() + "\n")

finalize()