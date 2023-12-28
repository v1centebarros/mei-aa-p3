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
def lossy_counting(text, bucket_size=100, epsilon=0.01):
    current_bucket = 1
    letter_count = defaultdict(int)
    frequencies = defaultdict(int)

    for i, letter in enumerate(text):
        if letter.isalpha():
            letter_count[letter] += 1

            # Check if the current bucket is full
            if (i + 1) % bucket_size == 0:
                # Update frequencies and remove infrequent items
                for letter, count in list(letter_count.items()):
                    if count + current_bucket * epsilon < current_bucket:
                        del letter_count[letter]
                    else:
                        frequencies[letter] = count
                current_bucket += 1

    # Include counts from the last bucket if it's not full
    for letter, count in letter_count.items():
        frequencies[letter] = max(frequencies[letter], count)

    return dict(frequencies)


@benchmark
def lossy_counting_gigachad(text, k=None, error=0.01, N=10):
    counter_map = defaultdict(int)
    total = 0
    delta = 0
    window_width = k if k is not None else ceil(1 / error)

    for letter in text:
        if letter.isalpha():
            # Increment the count for the letter
            counter_map[letter] += 1
            total += 1

            # Update counters and remove infrequent items
            threshold = floor(total / window_width)
            if threshold != delta:
                delta = threshold
                for item, count in list(counter_map.items()):
                    if count < delta:
                        counter_map.pop(item)

    # Get the most frequent N items
    most_frequent = sorted(counter_map.keys(), key=lambda x: counter_map[x], reverse=True)[:N]
    return {letter: counter_map[letter] for letter in most_frequent}
