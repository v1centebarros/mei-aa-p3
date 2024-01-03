import json

import matplotlib.pyplot as plt
import numpy as np


def plot_count_per_algorithm(results, title, k=3, show=True, save=False):
    k = str(k)
    letters = results["quixote_hun.txt"]["exact_counter"][k]["result"].keys()
    algorithms = ["exact_counter", "fixed_probability_counter", "lossy_counting"]
    values = {algorithm: [results["quixote_hun.txt"][algorithm][k]["result"].get(letter, 0) for letter in letters] for
              algorithm in algorithms}

    x = np.arange(len(letters))
    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots(layout="constrained")

    for attribute, measurement in values.items():
        ax.bar(x + multiplier * width, measurement, width, label=attribute)
        multiplier += 1

    ax.set_ylabel('Counts')
    ax.set_title(title)
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(letters)
    ax.legend(loc='upper left')

    if show:
        plt.show()

    if save:
        plt.savefig(f'{title}.png')


def main():
    results = json.load(open("../results/results.json", "r"))
    plot_count_per_algorithm(results, "Most frequent letters in books")


if __name__ == "__main__":
    main()
