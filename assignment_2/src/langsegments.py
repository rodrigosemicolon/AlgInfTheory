import math
import sys

from matplotlib import pyplot as plt
from dictionary import DictionaryModel
from fcm import default_path, make_dic, n_occurrences_all_c, all_possible_contexts, alphabet, non_occ_contexts, get_context_chance, get_context_entropy, get_chance
from language import calc_bits
from recognizer import cat_references, read_models


def get_stran(data: list, thresh: float) -> list:
    """
    From a list of values, return the intervals in which the values are equal or less than the threshold
    :param data: List with values of the -log(p) for each occurring context and event in target.
    :param thresh: Threshold to build the intervals from.
    :return:
    """
    blocks = []

    flag = [False for i in data]
    for i in range(len(data)):
        if data[i] <= thresh and not flag[i]:
            val = data[i]
            beg = i
            end = i
            for j in range(i + 1, len(data)):
                if data[j] <= thresh:
                    val += data[j]
                    flag[j] = True
                    end = j
                else:
                    break

            
            blocks.append(((beg, end + k), val))
        flag[i] = True

    return blocks


def compare_langs(target: str, models: list, k: int, a: float, show_graph: bool) -> None:
    """
    Opens target text and iterates over it k by k chars and checks its probability in each model and stores it in a list 
    for each model.
    It then goes ahead and detects intervals where each language feels it can describe the target interval with a 
    small number of bits.
    to be plotted if show_graph == True.

    :param target: Path of the target text.
    :param models: All the available models for different languages.
    :param k: Context size.
    :param a: Alpha smoothening parameter.
    :param show_graph: Boolean to determine if we show the graph at the end or not.
    """
    vals = {}
    with open(target, "r", encoding="utf8") as t:
        for lang in models:
            vals[lang.name] = []
        fulltext = t.read().lower()
        curr_context = tuple(fulltext[:k])
        for c in fulltext[k:]:
            for m in models:
                if curr_context in m.dic.keys():
                    prob = get_chance(m.dic[curr_context], c, a)
                    if prob > 0:
                        vals[m.name].append(-math.log(prob, 2))
                elif a > 0:
                    vals[m.name].append(-math.log((a / (a * len(m.alphabet))), 2))
            curr_context = tuple([a for a in curr_context[1:]] + list(c))

        if show_graph and len(fulltext) <= 50:
            plt.xticks(range(0, len(fulltext[k:])), list(fulltext[k:]))

        for m in models:
            filtered = lowpass(vals[m.name], fw)
            if show_graph:
                plt.plot(range(0, len(filtered)), filtered, label=m.name)
            threshold = math.log(len(m.alphabet), 2) / 2
            stranger = get_stran(filtered, threshold)

            print("the model considers the target ", m.name, "in:")
            for interval in (stranger):
                word = "[" + str(interval[0][0]) + "," + str(interval[0][1]) + "] : "
                for j in range(interval[0][0], interval[0][1] + 1):
                    word += fulltext[j]

                """
                for j in range(interval[0][0], interval[0][1] + 1):
                    word += fulltext[j]
                """
                print(word)
            t = [threshold for v in vals[m.name]]
            if show_graph:
                plt.plot(range(0, len(vals[m.name])), t, label=m.name + " threshold")
        if show_graph:
            plt.legend(loc="upper left")
            plt.show()


def lowpass(data: list, alpha: float) -> list:
    """
    Applies a low pass filter to given data.

    :param data: Data to filter.
    :param alpha: Smoothening parameter, diferent from the models smoothening parameter.
    :return: Filtered data.
    """
    filtered = [0 for i in data]
    filtered[0] = alpha * data[0]
    for i in range(1, len(data)):
        filtered[i] = filtered[i - 1] + alpha * (data[i] - filtered[i - 1])

    return filtered


if __name__ == "__main__":
    k = -1
    a = -1
    mp, tp, rp = -1, -1, -1
    fw = 0.4
    args = sys.argv
    k_flag = False
    a_flag = False
    tp_flag = False
    mp_flag = False
    rp_flag = False
    show_graph = False
    for i in range(len(args)):
        if i % 2 == 0:
            if args[i - 1] == "-k":
                k = int(args[i])
                if k > 0:
                    k_flag = True
            elif args[i - 1] == "-a":
                a = float(args[i])
                if 0 <= a <= 1:
                    a_flag = True
            elif args[i - 1] == "-tp":
                tp = args[i]
                tp_flag = True
            elif args[i - 1] == "-mp":
                mp = args[i]
                mp_flag = True
            elif args[i - 1] == "-rp":
                rp = args[i]
                rp_flag = True
            elif args[i - 1] == "-sg":
                if int(args[i]) > 0:
                    show_graph = True
            elif args[i - 1] == "-fw":
                if float(args[i]) > 0:
                    fw = float(args[i])
    if len(args) == 1:
        print("Executing without params, try using:\n\n"
              "k: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "tp: Path to specific target text file;\n"
              "mp: Path to models folder;\n"
              "rp: Path to a folder containing reference folders which contain texts that will make up the models (optional)\n"
              "sg: Display the results visually if set to 1 (optional)\n"
              "fw: Weight used in the low pass filter (optional)\n")
        sys.exit()
    elif len(args) == 2 and args[len(args) - 1] == "-h":
        print("Use:\n\n"
              "k: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "tp: Path to specific target text file;\n"
              "mp: Path to models folder;\n"
              "rp: Path to a folder containing reference folders which contain texts that will make up the models (optional)\n"
              "sg: Display the results visually if set to 1 (optional)\n"
              "fw: Weight used in the low pass filter (optional)\n")
        sys.exit()
    if not (k_flag and a_flag and tp_flag and mp_flag):
        print("Not all parameters have valid values")
        sys.exit()
    if rp_flag:
        cat_references(rp, mp)
    models = read_models(mp, k, a)
    compare_langs(tp, models, k, a, show_graph)
