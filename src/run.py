import json
import os
from collections import OrderedDict

FILE_PATH = "../books/"
RESULTS_FILE = "../results/results.json"
from algorithms import exact_counter, fixed_probability_counter, lossy_counting
from utils import log, Stats, CounterResult

books = [book for book in os.listdir(FILE_PATH) if book.endswith(".txt")]
algorithms = [exact_counter, fixed_probability_counter, lossy_counting]


def sort_result(result, time):
    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    k = {k: {"result": OrderedDict(sorted_result[:k]), "time": time} for k in [3, 5, 10]}
    return k


def run_exact_counter(text):
    result, time = exact_counter(text)
    return sort_result(result, time)


def run_fixed_probability_counter(text, runs=100):
    results = []
    average_result = {}
    average_time = 0

    for i in range(runs):
        log.info(f"Running fixed probability counter {i + 1} of {runs}")
        result, time = fixed_probability_counter(text)
        results.append(result)
        average_time += time

    for letter in results[0]:
        average_result[letter] = sum(result[letter] for result in results) / len(results)

    return sort_result(average_result, average_time / runs)


def run_lossy_counting(text):
    k = {}
    for i in [3, 5, 10]:
        log.info(f"Running lossy counting with k={i}")
        result, time = lossy_counting(text, i)
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        k[i] = {"result": OrderedDict(sorted_result), "time": time}

    return k


def marathon():
    results = {}
    for book in books:
        results[book] = {}
        with open(os.path.join(FILE_PATH, book), "r") as f:
            book_text = f.read()
            log.info(f"Running exact counter on {book}")
            results[book]["exact_counter"] = run_exact_counter(book_text)
            log.info(f"Running fixed probability counter on {book}")
            results[book]["fixed_probability_counter"] = run_fixed_probability_counter(book_text)
            log.info(f"Running lossy counting on {book}")
            results[book]["lossy_counting"] = run_lossy_counting(book_text)

    json.dump(results, open(RESULTS_FILE, "w"), indent=4, ensure_ascii=False)


def run_stats(results):
    for book in books:
        for algorithm in ["fixed_probability_counter", "lossy_counting"]:
            log.info(f"Running statistics on {book} with {algorithm}")
            for k in ["3", "5", "10"]:
                exact_counter_obg = CounterResult(results[book]["exact_counter"][k]["result"],
                                                  results[book]["exact_counter"][k]["time"])
                counter = CounterResult(results[book][algorithm][k]["result"], results[book][algorithm][k]["time"])
                stats = Stats(exact_counter_obg, counter)
                stats.save_results(f"../results/{book}_{algorithm}_{k}.json", _type="json")


if __name__ == "__main__":
    if not os.path.exists("../results"):
        os.mkdir("../results")

    if not os.path.exists(RESULTS_FILE):
        marathon()

    results = json.load(open(RESULTS_FILE, "r"))

    run_stats(results)
