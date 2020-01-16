from bs4 import BeautifulSoup

from koalanlp.Util import initialize, finalize
from koalanlp import API

import hanja
import sys
import os

load_path = sys.argv[1]

files = [f for f in os.listdir(load_path) if os.path.isfile(load_path + '/' + f) and f.endswith("story")]
for fi in files:
    print('id: {}'.format(fi))
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

    print(len([c for c in content if hanja.is_hanja(c)]))