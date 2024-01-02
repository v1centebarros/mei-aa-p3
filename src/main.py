import json
import os

from utils import calculate_total_and_unique_characters

FILE_PATH = "../books/"
books = [book for book in os.listdir(FILE_PATH) if book.endswith(".txt")]


def main():
    results = {}
    for book in books:
        with open(os.path.join(FILE_PATH, book), "r") as f:
            book_text = f.read()
            total_characters, unique_characters = calculate_total_and_unique_characters(book_text)
            results[book] = {"total_characters": total_characters, "total_unique_characters": len(unique_characters),
                             "unique_characters": list(unique_characters)}

    with open("../results/character_counts.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
