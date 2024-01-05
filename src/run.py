import json
import os
from collections import OrderedDict
from math import floor

from tqdm import tqdm

FILE_PATH = "../books/"
RESULTS_FILE = "../results/results.json"
from algorithms import exact_counter, fixed_probability_counter, lossy_counting
from utils import log, Stats, CounterResult

books = [book for book in os.listdir(FILE_PATH) if book.endswith(".txt")]
algorithms = [exact_counter, fixed_probability_counter, lossy_counting]


def sort_result(result, time):
    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    k = {k: {"result": OrderedDict(sorted_result[:k]), "time": time} for k in [3, 5, 10]}
    k[0] = {"result": OrderedDict(sorted_result), "time": time}
    return k


def run_exact_counter(text):
    result, time = exact_counter(text)
    return sort_result(result, time)


def run_fixed_probability_counter(text, runs=500):
    results = []
    average_result = {}
    average_time = 0

    for _ in tqdm(range(runs)):
        result, time = fixed_probability_counter(text)
        results.append(result)
        average_time += time

    for letter in results[0]:
        average_result[letter] = floor(sum(result[letter] for result in results) / len(results))

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


def run_stats_lossy(results):
    for book in books:

        for k in ["3", "5", "10"]:
            exact_counter_result = CounterResult(results[book]["exact_counter"]["0"]["result"],
                                                 results[book]["exact_counter"]["0"]["time"])
            counter = CounterResult(results[book]["lossy_counting"][k]["result"],
                                    results[book]["lossy_counting"][k]["time"])
            stats = Stats(exact_counter_result, counter)
            stats.save_results(f"../results/{book}_lossy_counting_{k}.json", _type="json")


def run_stats_probability(results):
    for book in books:
        exact_counter_result = CounterResult(results[book]["exact_counter"]["0"]["result"],
                                             results[book]["exact_counter"]["0"]["time"])
        probability_counter_result = CounterResult(results[book]["fixed_probability_counter"]["0"]["result"],
                                                   results[book]["fixed_probability_counter"]["0"]["time"])

        stats = Stats(exact_counter_result, probability_counter_result)
        stats.save_results(f"../results/{book}_probability_counter.json", _type="json")


if __name__ == "__main__":
    if not os.path.exists("../results"):
        os.mkdir("../results")

    # if not os.path.exists(RESULTS_FILE):
    marathon()

    results = json.load(open(RESULTS_FILE, "r"))

    run_stats_lossy(results)
    run_stats_probability(results)
