import requests
import sys
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
LANGUAGES = ('arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
             'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish')


def translate_info(_to_lang, _from_lang):
    _to_lang, _from_lang = _to_lang.lower(), _from_lang.lower()
    if translate_to not in LANGUAGES and translate_to != 'all':
        print(f"Sorry, the program doesn't support {translate_to}")
        sys.exit()
    if translate_from not in LANGUAGES:
        print(f"Sorry, the program doesn't support {translate_from}")
        sys.exit()
    return _to_lang, _from_lang


def complete_url(_word):
    return f'https://context.reverso.net/translation/{from_lang}-{to_lang}/{_word}'


def trans_words(soup):
    no_results = soup.select('.no-results')
    if no_results:
        print(f'Sorry, unable to find {word}')
        sys.exit()
    print(f'{to_lang} Translations:')
    words_results = soup.find_all('a', attrs={'class': 'translation'})
    translated_words = []
    for tag in words_results[1:5]:
        translated_words.append(tag.text.strip())
    if translate_to == 'all':
        t.write(f'\n{to_lang} Translations:\n')
        for o in translated_words:
            t.write(o + '\n')
            print(o + '\n')
    else:
        print(*translated_words, sep='\n')


def sentences(soup):
    print(f'\n{to_lang} Examples:')
    sentences_results_left = soup.select('.example > .src')
    sentences_results_right = soup.select('.example > .trg')
    translated_sentences = []
    for tag_left, tag_right in zip(sentences_results_left[:5], sentences_results_right[:5]):
        translated_sentences.append(tag_left.text.replace('\n', '').replace('  ', ''))
        translated_sentences.append(tag_right.text.replace('\n', '').replace('  ', ''))
    if translate_to == 'all':
        t.write(f'\n{to_lang} Examples:\n')
    for i, j in enumerate(translated_sentences):
        if translate_to == 'all':
            if i % 2 == 0:
                t.write(j + ':')
                print(j + ':')
            else:
                t.write(j + '\n')
                print(j + '\n')
        else:
            if i % 2 == 0:
                print(j + ':')
            else:
                print(j + '\n')


def main():
    url = complete_url(word)
    try:
        response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=30)
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        sys.exit()
    soup = BeautifulSoup(response.text, 'html.parser')
    trans_words(soup)
    sentences(soup)


print("""Hello, you're welcome to the translator. Translator supports:
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish""")

translate_from, translate_to, word = sys.argv[1:]
to_lang, from_lang = translate_info(translate_to, translate_from)

if translate_to == 'all':
    t = open(f'{word}.txt', 'w', encoding='utf-8')
    for x in LANGUAGES:
        if x == translate_from:
            continue
        to_lang = x
        main()
    t.close()

else:
    main()
