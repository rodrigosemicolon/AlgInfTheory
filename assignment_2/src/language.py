import math
import sys

from dictionary import DictionaryModel
from fcm import default_path, make_dic, n_occurrences_all_c, all_possible_contexts, alphabet, non_occ_contexts, get_context_chance, get_context_entropy, get_chance


def calc_bits(model: DictionaryModel, target: str, k: int, a: float) -> float:
    """
    Iterates over a text and calculates the estimated amount of bits needed to
    describe it.

    :param model: DictionaryModel object representing our model.
    :param target: Target text.
    :param k: Context size.
    :param a: Alpha smoothening parameter.
    :return: Estimated total amount of bits to describe target text with the model.
    """
    totalbits = 0
    fulltext = target.lower()
    curr_context = tuple(fulltext[:k])
    for c in fulltext[k:]:
        if curr_context in model.dic.keys():
            prob = get_chance(model.dic[curr_context], c, a)
            if prob > 0:
                totalbits = totalbits - math.log(prob, 2)
        elif a > 0:
            totalbits = totalbits - math.log((a / (a * len(model.alphabet))), 2)

        curr_context = tuple([a for a in curr_context[1:]] + list(c))

    return totalbits


def get_bits(filepath: str, filetarget: str, k: int, a: float) -> float:
    """
    Builds a model from filepath and calculates the number of bits necessary to encode the target file with it.


    :param filepath: Path to build the model from.
    :param filetarget: Path to get the target from.
    :param k: Context size.
    :param a: Smoothing parameter.
    :return: The number of bits it takes the model to describe the target
    """
    with open(filepath,"r",encoding="utf-8")as reference_model:
        dic_model = DictionaryModel("undefined", reference_model.read(), k, a)

    

    with open(filetarget, "r", encoding="utf8") as target:
        target_text = target.read()
        return calc_bits(dic_model, target_text, k, a)


if __name__ == "__main__":

    k = -1
    a = -1
    tp, mp = -1, -1
    args = sys.argv
    k_flag = False
    a_flag = False
    tp_flag = False
    mp_flag = False
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
    if len(args) == 1:
        print("Executing without params, try using:\n\n"
              "k: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "tp: Path to specific target text file;\n"
              "mp: Path to specific reference model text file;\n")
        sys.exit()
    elif len(args) == 2 and args[len(args) - 1] == "-h":
        print("Use:\n\n"
              "k: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "tp: Path to specific target text file;\n"
              "mp: Path to specific reference model text file;\n")
        sys.exit()
    if not (k_flag and a_flag and tp_flag and mp_flag):
        print("Not all parameters have valid values")
        sys.exit()

    n_bits = get_bits(mp, tp, k, a)
    print(n_bits)
