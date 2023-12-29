import random
from collections import defaultdict
from math import ceil, floor

from utils import benchmark


@benchmark
def exact_counter(text):
    letter_map = defaultdict(int)

    for letter in text:
        if letter.isalpha():
            letter_map[letter] += 1

    return letter_map


@benchmark
def fixed_probability_counter(text, probability=1 / 32):
    letter_map = defaultdict(int)

    for letter in text:
        if letter.isalpha() and random.random() < probability:
            letter_map[letter] += 1

    # Scale up the counts to estimate actual frequencies
    for letter in letter_map:
        letter_map[letter] *= int(1 / probability)

    return letter_map


@benchmark
def lossy_counting(text: str, k: int = 10, error: float = None):
    letter_map = defaultdict(int)
    bucket_width = k if error is None else ceil(1 / error)
    total = 0
    delta = 0

    for letter in text:
        if letter.isalpha():
            if letter not in letter_map:
                letter_map[letter] = delta + 1
            else:
                letter_map[letter] += 1
            total += 1

            # Update counters and remove infrequent items
            threshold = floor(total / bucket_width)
            if threshold != delta:
                delta = threshold
                for item, count in list(letter_map.items()):
                    if count < delta:
                        letter_map.pop(item)

    return letter_map
