import math
import os
import sys
import time


from dictionary import DictionaryModel
from fcm import default_path, make_dic, n_occurrences_all_c, all_possible_contexts, alphabet, non_occ_contexts, get_context_chance, get_context_entropy, get_chance
from language import calc_bits


def read_models(path: str, k: int, a: float) -> list:
    """
    Gets models from text files in path.

    :param path: Path to the models folder.
    :param k: Context size.
    :param a: Alpha smoothening parameter.
    :return: List of all models in path folder.
    """
    lang_models = []
    for f in os.walk(path):
        for model_file in f[2]:
            name = model_file.split(".txt")[0]
            with open(path + model_file, "r", encoding="utf-8") as concatenated_books:
                lang_models.append(DictionaryModel(name, concatenated_books.read(), k, a))

    return lang_models


def cat_references(reference_path: str, model_path: str) -> None:
    """
    For each folder in reference_path, concatenate all its files and save it in model_path
    :param reference_path: Path containing all the folders with the references.
    :param model_path: Path where all the concatenated files will be.
    """
    for f in os.walk(reference_path):
        lang = f[0].split("/")[-1]
        fulltext = ""
        if lang == "":
            continue

        for ref_file in f[2]:
            with open(f[0] + "/" + ref_file, "r", encoding="utf8") as ref:
                fulltext += ref.read() + "\n"
        with open(model_path + lang + ".txt", "w", encoding="utf8") as mod:
            mod.write(fulltext)


def recognition(models: list, targetfile: str, k: int, a: float) -> dict:
    """
    Returns the scores for each reference model compared to a
    certain target.

    :param models: List with all the reference models.
    :param targetfile: Path to target.
    :param k: Context size.
    :param a: Alpha smoothening param.
    :return: Dictionary ordered by score.
    """
    scores = {}
    with open(targetfile, "r", encoding="utf8") as tfile:
        target_text = tfile.read()
        for model in models:
            scores[model.name] = calc_bits(model, target_text, k, a)
        sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=False)}
    return sorted_scores


if __name__ == "__main__":
    k = -1
    a = -1
    mp, tp, rp = -1, -1, -1
    args = sys.argv
    k_flag = False
    a_flag = False
    tp_flag = False
    mp_flag = False
    rp_flag = False
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
    if len(args) == 1:
        print("Executing without params, try using:\n\n"
              "k: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "tp: Path to specific target text file;\n"
              "mp: Path to models folder;\n"
              "rp: Path to a folder containing reference folders which contain texts that will make up models (optional)\n")
        sys.exit()
    elif len(args) == 2 and args[len(args) - 1] == "-h":
        print("Use:\n\n"
              "k: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "tp: Path to specific target text file;\n"
              "mp: Path to models folder;\n"
              "rp: Path to a folder containing reference folders which contain texts that will make up models (optional)\n")
        sys.exit()
    if not (k_flag and a_flag and tp_flag and mp_flag):
        print("Not all parameters have valid values")
        sys.exit()
    if rp_flag:
        cat_references(rp, mp)
    models = read_models(mp, k, a)
    scores = recognition(models, tp, k, a)
    for k in scores:
        print(k, scores[k])
