from bs4 import BeautifulSoup

from koalanlp.Util import initialize, finalize
from koalanlp import API

import hanja
import sys
import os

load_path = sys.argv[1]
save_path = sys.argv[2]

files = [f for f in os.listdir(load_path) if os.path.isfile(load_path + '/' + f) and f.endswith("story")]
for fi in files:
    print('id: {}\n'.format(fi))
    with open(load_path + '/' + fi, 'r', encoding='utf-8') as f:
        # get title
        assert "<<<TITLE>>>\n" == f.readline()

        title = ""
        content = ""

        line = f.readline()
        while line != '<<<CONTENT>>>\n':
            title += line
            line = f.readline()
        content = f.read()

    # remove html tags
    bs = BeautifulSoup(content, 'html.parser')
    content = bs.text

    # remove byline
    

    # remove non-sentential form

    # replace hanja to hangul

    # remove 조사

    # save processed files
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open(save_path + '/' + fi, 'w', encoding='utf-8') as f:
        f.write("<<<TITLE>>>\n")
        f.write(title + "\n")
        f.write("<<<CONTENT>>>\n")
        f.write(content)
