"""Generates a tag cloud from words found in the given projects python files."""
import builtins
import keyword
import os
import sys
import tokenize
from collections import Counter

import matplotlib.pyplot as plt
from wordcloud import WordCloud

DIR_BLACKLIST = ['.git', 'venv', 'tests']
TOKEN_BLACKLIST = ['self', *keyword.kwlist, *dir(builtins)]


def project_tokens(root):
    def file_tokens(file):
        with open(file, 'rb') as f:
            yield from (token.string
                        for token in tokenize.tokenize(f.readline)
                        if token.type == tokenize.NAME and token.string not in TOKEN_BLACKLIST)

    for root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in DIR_BLACKLIST]
        yield from (token
                    for file in files if file.endswith('.py')
                    for token in file_tokens(os.path.join(root, file)))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py /path/to/python/repo', file=sys.stderr)
        sys.exit(1)

    repo = sys.argv[1]
    tokens = project_tokens(repo)
    token_counts = Counter(tokens)
    tag_cloud = WordCloud().generate_from_frequencies(token_counts)
    plt.figure()
    plt.imshow(tag_cloud, interpolation="bilinear")
    plt.axis("off")

    plt.savefig('tags.png')
