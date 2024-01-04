import json
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import ceil


def plot_count_per_algorithm(results, title, k=3, show=False, save=False):
    k = str(k)
    books = results.keys()
    num_books = len(books)
    algorithms = ["exact_counter", "fixed_probability_counter", "lossy_counting"]

    num_cols = 3
    num_rows = ceil(num_books / num_cols)

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(10 * num_cols, 5 * num_rows), constrained_layout=True)

    axs = axs.flatten()

    for i, book in enumerate(books):
        letters = results[book]["exact_counter"][k]["result"].keys()
        values = {algorithm: [results[book][algorithm][k]["result"].get(letter, 0) for letter in letters] for
                  algorithm in algorithms}

        x = np.arange(len(letters))
        width = 0.25
        multiplier = 0

        for attribute, measurement in values.items():
            axs[i].bar(x + multiplier * width, measurement, width, label=attribute)
            multiplier += 1

        axs[i].set_ylabel('Counts')
        axs[i].set_xlabel('Most frequent letters')
        axs[i].set_title(book)
        axs[i].set_xticks(x + width / 2)
        axs[i].set_xticklabels(letters)
        axs[i].legend(loc='upper right')

    # Remove unused subplots
    for i in range(num_books, num_rows * num_cols):
        fig.delaxes(axs[i])

    fig.suptitle(title, fontsize=16)

    if show:
        plt.show()

    if save:
        plt.savefig(f'../plots/{title}.png')


def plot_exact_counter_of_each_letter_per_book(results, title, show=False, save=False):
    books = results.keys()
    letters_counters = defaultdict(dict)

    # Accumulate counts for each letter in each book
    for book in books:
        for letter, count in results[book]["exact_counter"]["0"]["result"].items():
            letters_counters[letter][book] = count

    # Convert to DataFrame and sort by index (letters)
    df = pd.DataFrame(letters_counters).T
    df = df.fillna(0).sort_index()

    # Plotting
    num_books = len(df.columns)
    total_width = 0.8  # You can adjust this for wider gaps
    single_width = total_width / num_books
    bar_positions = np.arange(len(df.index))

    fig, ax = plt.subplots()

    # Adjusting bar positions for spacing
    gap_width = 0.1  # Space between groups
    group_width = num_books * single_width + gap_width

    for i, book in enumerate(df.columns):
        ax.bar(bar_positions + i * single_width - (group_width - single_width) / 2, df[book],
               width=single_width, label=book)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels(df.index)

    ax.legend(loc='upper right')
    ax.set_title(title)
    ax.set_xlabel('Letter')
    ax.set_ylabel('Occurrences')

    if show:
        plt.show()

    if save:
        plt.savefig(f'../plots/{title}.png')


def main():
    results = json.load(open("../results/results.json", "r"))

    for k in [3, 5, 10]:
        plot_count_per_algorithm(results, f"Most frequent letters with k={k}", k=k, save=True)

    plot_exact_counter_of_each_letter_per_book(results, "Exact counter of each letter per book", save=True)


if __name__ == "__main__":
    main()
