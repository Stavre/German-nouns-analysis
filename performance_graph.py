from time import time
import matplotlib.pyplot as plt
import numpy as np
from parser import parse



if __name__ == '__main__':
    # list of dictionaries downloaded from dict.cc
    dictionaries = ["de_en", "de_la", "de_nl", "en_es", "en_fr"]

    time_performance = []
    time_performance_multiprocessing = []

    reps = 3

    print("Please wait, this will take some time")

    for dictionary in dictionaries:
        print("Test dictionary " + dictionary + " without multiprocessing")
        start = time()
        for i in range(0, reps):
            parse(dictionary + "_dictionary.txt")
        end = time()
        time_performance.append((end - start) / reps)

    for dictionary in dictionaries:
        print("Test dictionary " + dictionary + " with multiprocessing")
        start = time()
        for i in range(0, reps):
            parse(dictionary + "_dictionary.txt", multiprocessing=True)
        end = time()
        time_performance_multiprocessing.append((end - start) / reps)

    barWidth = 0.25
    br1 = np.arange(len(time_performance))
    br2 = [x + barWidth for x in br1]

    ax = plt.axes()
    ax.set_axisbelow(True)
    ax.yaxis.grid(color="lightgray")  # vertical lines

    plt.bar(br1, time_performance, width=barWidth, label="without multiprocessing")
    plt.bar(br2, time_performance_multiprocessing, width=barWidth, label="with multiprocessing")
    plt.xticks([r + barWidth for r in range(len(time_performance))],
               dictionaries)

    plt.xlabel("Dictionaries")
    plt.ylabel("Time (s)")
    plt.title("Execution time")
    plt.legend()
    plt.savefig("fig.png")
