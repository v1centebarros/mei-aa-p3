import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

nltk.download('punkt')
nltk.download('stopwords')


def process_file(file_path, language='en'):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines = [l.strip() for l in lines]
    text = ' '.join(lines)

    stop_words = get_stopwords(language)

    word_tokens = word_tokenize(text)

    filtered_text = [w.upper() for w in word_tokens if w not in stop_words and w.isalpha()]

    return ''.join(filtered_text)


def get_stopwords(language):
    language_map = {
        'es': 'spanish',
        'gr': 'german',
        'fr': 'french',
        'fi': 'finnish',
        'hu': 'hungarian',
        'du': 'dutch',
        'en': 'english'
    }

    stop_words = set(stopwords.words(language_map.get(language, 'english')))
    return stop_words


def main():
    raw_books_dir = '../books/raw/'
    for filename in tqdm(os.listdir(raw_books_dir)):
        if filename.endswith('.txt'):
            lang = filename.split('_')[0] if '_' in filename else 'en'
            processed_file = process_file(os.path.join(raw_books_dir, filename), lang)
            with open(os.path.join('../books', filename), 'w') as file:
                file.write(processed_file)


if __name__ == '__main__':
    main()
