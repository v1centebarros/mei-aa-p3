import os

FILE_PATH = "../books/"
from algorithms import exact_counter, fixed_probability_counter, lossy_counting,lossy_counting_gigachad
from utils import log, Stats

books = [book for book in os.listdir(FILE_PATH) if book.endswith(".txt")]
algorithms = [exact_counter, fixed_probability_counter, lossy_counting, lossy_counting_gigachad]


def main():
    results = {}
    for book in books:
        results[book] = {}
        with open(os.path.join(FILE_PATH, book), "r") as f:
            book_text = f.read()
            for algorithm in algorithms:
                log.info(f"Running {algorithm.__name__} on {book}")
                results[book][algorithm.__name__] = algorithm(book_text)

    for book in results:
        exact_result = results[book]["exact_counter"]
        for algorithm in algorithms[1:]:
            approx_result = results[book][algorithm.__name__]
            stats = Stats(exact_result, approx_result)
            log.info(f"Results for {algorithm.__name__} on {book}")
            stats.save_results(f"../results/{book}_{algorithm.__name__}.json", "json")


if __name__ == "__main__":
    main()
