import os

FILE_PATH = "../books/"
from algorithms import exact_counter, fixed_probability_counter, lossy_counting
from utils import log

books = [book for book in os.listdir(FILE_PATH) if book.endswith(".txt")]
algorithms = [exact_counter, fixed_probability_counter, lossy_counting]


def main():
    for book in books:
        with open(os.path.join(FILE_PATH, book), "r") as f:
            book_text = f.read()
            for algorithm in algorithms:
                log.info(f"Running {algorithm.__name__} on {book}")
                print(algorithm(book_text))


if __name__ == "__main__":
    main()
