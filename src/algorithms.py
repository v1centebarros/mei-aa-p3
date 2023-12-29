import random
from collections import defaultdict
from math import ceil, floor

from utils import benchmark


@benchmark
def exact_counter(text):
    letter_count = defaultdict(int)

    for letter in text:
        if letter.isalpha():
            letter_count[letter] += 1

    return letter_count


@benchmark
def fixed_probability_counter(text, probability=1 / 32):
    letter_count = defaultdict(int)

    for letter in text:
        if letter.isalpha() and random.random() < probability:
            letter_count[letter] += 1

    # Scale up the counts to estimate actual frequencies
    for letter in letter_count:
        letter_count[letter] *= int(1 / probability)

    return letter_count


@benchmark
def lossy_counting(text: str, k: int = 10, error: float = None):
    letter_count = defaultdict(int)
    bucket_width = k if error is None else ceil(1 / error)
    total = 0
    delta = 0

    for letter in text:
        if letter.isalpha():
            if letter not in letter_count:
                letter_count[letter] = delta + 1
            else:
                letter_count[letter] += 1
            total += 1

            # Update counters and remove infrequent items
            threshold = floor(total / bucket_width)
            if threshold != delta:
                delta = threshold
                for item, count in list(letter_count.items()):
                    if count < delta:
                        letter_count.pop(item)

    return letter_count
