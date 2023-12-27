import json
import logging
import pickle
import time
from collections import namedtuple
from math import sqrt
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)
Result = namedtuple('Result', ['time', 'result', 'algorithm'])


def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        result_sorted = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return Result(time.perf_counter() - start, result_sorted, func.__name__)

    return wrapper


class Stats:
    def __init__(self, exact_result, approx_result):
        self.exact_counts: dict[str, int] = dict(exact_result.result)
        self.approx_counts: dict[str, int] = dict(approx_result.result)
        self.letters = set(self.exact_counts.keys()).union(set(self.approx_counts.keys()))

    def mean_absolute_error(self):
        total_error = sum(abs(self.exact_counts[letter] - self.approx_counts.get(letter, 0)) for letter in self.letters)
        return total_error / len(self.letters)

    def mean_relative_error(self):
        total_relative_error = sum(
            abs(self.exact_counts[letter] - self.approx_counts.get(letter, 0)) / self.exact_counts[letter] for letter in
            self.letters if self.exact_counts[letter] != 0)
        return total_relative_error / len(self.letters)

    def mean_accuracy_ratio(self):
        total_accuracy_ratio = sum(
            self.approx_counts.get(letter, 0) / self.exact_counts[letter] for letter in self.letters if
            self.exact_counts[letter] != 0)
        return total_accuracy_ratio / len(self.letters)

    def smallest_value(self):
        return min(self.approx_counts.values())

    def largest_value(self):
        return max(self.approx_counts.values())

    def mean(self):
        return sum(self.approx_counts.values()) / len(self.approx_counts)

    def mean_absolute_deviation(self):
        mean = self.mean()
        total_deviation = sum(abs(count - mean) for count in self.approx_counts.values())
        return total_deviation / len(self.approx_counts)

    def standard_deviation(self):
        mean = self.mean()
        total_squared_deviation = sum((count - mean) ** 2 for count in self.approx_counts.values())
        return sqrt(total_squared_deviation / len(self.approx_counts))

    def maximum_deviation(self):
        mean = self.mean()
        return max(abs(count - mean) for count in self.approx_counts.values())

    def variance(self):
        mean = self.mean()
        total_squared_deviation = sum((count - mean) ** 2 for count in self.approx_counts.values())
        return total_squared_deviation / len(self.approx_counts)

    def __true_positives(self):
        return sum(
            1 for letter in self.approx_counts if self.approx_counts[letter] > 0 and self.exact_counts[letter] > 0)

    def precision(self, tolerance=0.1):
        true_positives = sum(
            1 for letter in self.approx_counts
            if abs(self.approx_counts[letter] - self.exact_counts.get(letter, 0)) <= tolerance * self.exact_counts.get(
                letter, 1)
        )
        total_positives = sum(1 for letter in self.approx_counts if self.approx_counts[letter] > 0)

        return true_positives / total_positives if total_positives else 0

    def recall(self):
        true_positives = self.__true_positives()
        total_relevant = sum(1 for letter in self.exact_counts if self.exact_counts[letter] > 0)
        return true_positives / total_relevant if total_relevant else 0

    def __save_pickle(self, filename, results):
        with open(filename, 'wb') as file:
            pickle.dump(results, file)

    def __save_json(self, filename, results):
        with open(filename, 'w') as file:
            json.dump(results, file, indent=4)

    def save_results(self, filename, _type='pickle'):
        results = {'mean_absolute_error': self.mean_absolute_error(), 'mean_relative_error': self.mean_relative_error(),
                   'mean_accuracy_ratio': self.mean_accuracy_ratio(), 'smallest_value': self.smallest_value(),
                   'largest_value': self.largest_value(), 'mean': self.mean(),
                   'mean_absolute_deviation': self.mean_absolute_deviation(),
                   'standard_deviation': self.standard_deviation(),
                   'maximum_deviation': self.maximum_deviation(), 'variance': self.variance(),
                   'precision': self.precision(),
                   'recall': self.recall()}

        match _type:
            case 'pickle':
                self.__save_pickle(filename, results)
            case 'json':
                self.__save_json(filename, results)
            case _:
                log.error(f'Invalid file type {_type}')
