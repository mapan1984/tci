from __future__ import print_function

import sys
import json
import argparse

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen


url = r'''http://fanyi.youdao.com/openapi.do'''

data = {
    'keyfrom': 'hidict',
    'key': '1217482697',
    'type': 'data',
    'doctype': 'json',
    'version': '1.1',
}


def get_response(word):
    data['q'] = word
    url_values = urlencode(data)
    full_url = url + '?' + url_values
    try:
        result = urlopen(full_url).read()
    except Exception:
        print("ERROR: Can not make network connection", file=sys.stderr)
        return None
    else:
        try:
            return json.loads(result.decode('utf-8'))
        except Exception:
            print("ERROR: Can not translate %s" % word, file=sys.stderr)
            return None


def is_valid_result(result):
    error_code = result.get('errorCode')
    if error_code == 0:
        return True
    else:
        print("ERROR: can't translate %s" % result.get("query"), file=sys.stderr)
        return False


def show_summary(result):
    translation = result.get('translation')
    if translation:
        print('Translation:')
        for t in translation:
            print('\t', t)


def show_explains(result):
    basic = result.get('basic')
    if basic:
        explains = basic.get('explains')
        if explains:
            print('Explains:')
            for e in explains:
                print('\t', e)


def show_web(result):
    web = result.get('web')
    if web:
        print('Web:')
        for item in web:
            print("\tKey: ", item.get('key').encode('utf-8'))
            for v in item.get('value'):
                print('\t\tValue: ', v)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str,
                        help="the word that you want to translate")
    parser.add_argument("-s", "--summary", help="show summary translation",
                        action="store_true")
    parser.add_argument("-e", "--explains",
                        help="show base explains, default is true",
                        action="store_true", default=True)
    parser.add_argument("-w", "--web", help="show web translation",
                        action="store_true")
    args = parser.parse_args()

    esc = r''',./<>?:;'"{}[]|\~`!@#$%^&*()-_=+'''
    word = args.word.strip(esc)
    print('[', word, ']')

    result = get_response(word)

    if args.summary:
        show_summary(result)
    if args.explains:
        show_explains(result)
    if args.web:
        show_web(result)


if __name__ == '__main__':
    main()

