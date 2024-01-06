import json
import os
from collections import defaultdict
from pprint import pprint

from utils import calculate_total_and_unique_characters

FILE_PATH = "../books/"
books = [book for book in os.listdir(FILE_PATH) if book.endswith(".txt")]


def calculate_total_and_unique_characters_main():
    results = {}
    for book in books:
        with open(os.path.join(FILE_PATH, book), "r") as f:
            book_text = f.read()
            total_characters, unique_characters = calculate_total_and_unique_characters(book_text)
            results[book] = {"total_characters": total_characters, "total_unique_characters": len(unique_characters),
                             "unique_characters": list(unique_characters)}

    with open("../results/character_counts.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def main ():
    with open("../results/results.json", "r") as f:
        results = json.load(f)
        new_results = defaultdict(dict)
        # create a list of the top 10 most frequent letters for each book of each algorithm
        for book in results:
            for algorithm in results[book]:

                if algorithm == "lossy_counting":
                    new_results[f"{book}"][algorithm] = defaultdict(dict)
                    for k in ["3", "5", "10"]:
                        new_results[f"{book}"][algorithm][f"{k}"] = list(results[book]["lossy_counting"][k]["result"].keys())
                else:
                    new_results[f"{book}"][algorithm] = list(results[book][algorithm]["10"]["result"].keys())


    json.dump(new_results, open("../results/top_letters.json", "w"), indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
