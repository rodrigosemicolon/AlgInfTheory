# Global variables
import math
import os
import sys
import time

from matplotlib import pyplot as plt
from dictionary import DictionaryModel
from fcm import default_path, make_dic, n_occurrences_all_c, all_possible_contexts, alphabet, non_occ_contexts, get_context_chance, get_context_entropy, get_chance

DEF_TARGET_PATH = "../example/targets/"
DEF_REFERENCE_PATH = "../example/models/"
# ERROR_METHOD = 'replace'
# ERROR_METHOD = 'ignore'
DEF_MODEL_PATH = "../example/models/"
DEF_BOOK_PATH = "../example/_books/"




def compare_langs(target, references, k, a):
    vals = {}
    with open(target, "r", encoding="utf8") as t:
        arr = {}
        for lang in references:
            arr[lang] = 0
            vals[lang] = []
        fulltext = t.read().lower()
        curr_context = tuple(fulltext[:k])
        for c in fulltext[k + 1:]:
            for r in references:
                if curr_context in references[r].dic.keys():
                    prob = get_chance(references[r].dic[curr_context], c, a)
                    if prob > 0:
                        arr[r] = float(arr[r]) + math.log(prob, 2)
                        # vals[r].append(math.log(prob, 2))

                elif a > 0:
                    arr[r] = arr[r] + math.log((a / (a * len(references[r].alphabet))), 2)
                    # vals[r].append(math.log((a / (a * len(references[r].alphabet))), 2))
            curr_context = tuple([a for a in curr_context[1:]] + list(c))
    # plt.xticks(range(k, len(fulltext)), list(fulltext[k:]))
    # for ref in references:
    #     filtered = lowpass(vals[ref.name], 0.7)
    #     plt.plot(range(k + 1, len(fulltext)), filtered, label=ref.name)
    #     threshold = math.log(len(ref.alphabet), 2) / 2
    #     stranger = get_stran(filtered, -threshold)
    #     print("the model considers ", ref.name, ": ", stranger)
    #     for interval in (stranger):
    #         word = ""
    #         """
    #         if interval[0][0] ==k+1:
    #             for j in range(interval[0][0]-k-1,interval[0][1]+1):
    #                 word+=fulltext[j]
    #         else:
    #             for j in range(interval[0][0],interval[0][1]+1):
    #                 word+=fulltext[j]
    #         print(word)
    #         """
    #         for j in range(interval[0][0] - k - 1, interval[0][1] + 1):
    #             word += fulltext[j]
    #         print(word)
    #     t = [-threshold for v in vals[ref.name]]
    #     plt.plot(range(k + 1, len(fulltext)), t, label=ref.name + " threshold")
    # plt.legend(loc="upper left")
    #
    # plt.show()
    return {k: -v for k, v in sorted(arr.items(), key=lambda item: item[1], reverse=True)}


def lowpass(data, alpha):
    max = -float("inf")
    filtered = [0 for i in data]
    filtered[0] = alpha * data[0]
    for i in range(1, len(data)):
        filtered[i] = filtered[i - 1] + alpha * (data[i] - filtered[i - 1])
        if filtered[i] > max:
            max = filtered[i]
    return filtered


def calc_bits(model,target,k,a):

    #arr = {}
    totalbits = 0
    #vals = {}
    fulltext = target.lower()
    curr_context = tuple(fulltext[:k])
    for c in fulltext[k + 1:]:
        if curr_context in model.dic.keys():
            prob = get_chance(model.dic[curr_context], c, a)
            if prob > 0:
                totalbits = totalbits - math.log(prob, 2) #sign
                #vals[r].append(-math.log(prob, 2))

        elif a > 0:
            totalbits = totalbits - math.log((a / (a * len(model.alphabet))), 2) #sign
            #vals[r].append(-math.log((a / (a * len(references[r].alphabet))), 2))
        curr_context = tuple([a for a in curr_context[1:]] + list(c))

    return totalbits #{k: v for k, v in sorted(arr.items(), key=lambda item: item[1], reverse=False)}

def get_bits(filepath,filetarget,k,a):
    dic_model = DictionaryModel("undefined",filepath, k, a)

    with open(filetarget,"r",encoding="utf8") as target:
        target_text = target.read()
        return calc_bits(dic_model,target_text,k,a)




if __name__ == "__main__":
    
    k = -1
    a = -1
    tp, mp = -1, -1
    args = sys.argv
    k_flag=False
    a_flag=False
    tp_flag=False
    mp_flag=False
    for i in range(len(args)):
        if i % 2 == 0:
            if args[i - 1] == "-k":
                k = int(args[i])
                if k>0:
                    k_flag=True
            elif args[i - 1] == "-a":
                a = float(args[i])
                if a>=0 and a<=1:
                    a_flag=True
            elif args[i - 1] == "-tp":
                tp = args[i]
                tp_flag=True
            elif args[i - 1] == "-mp":
                mp = args[i]
                mp_flag=True 
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
    
    n_bits= get_bits(mp,tp,k,a)
    print(n_bits)
    #reference_models = read_models(k, a)
    #values = compare_langs(st, reference_models, k, a)
    """
        # 1
        print("Number of bits to compress target 't' from reference model 'r':")
        print(f"Model Ref.:{sr}\n"
              f"Target:{st}\n"
              f"With k={k} and a={a}\n"
              f"The result is:{values[sr.split('/')[3][:2]]}")

        # 2,3
        print("\nLanguage recognition for target 't' with n reference models:\n"
              f"Target:{st}\n")
        count = 0
        for lang in values:
            if count == 0:
                count += 1
                print(f"{lang.upper()}->{values[lang]}(BEST MATCH FOR OVERALL TARGET LANGUAGE)")
            else:
                print(f"{lang.upper()}->{values[lang]}")

        # 4

        # 5
    
    """
# def compare_langs_test(k, a):
#     vals = {}
#     refs = read_models(k, a)
#     references = {"pt": refs["pt"], "en": refs["en"]}
#     with open("../example/target.txt", "r", encoding="utf8") as t:
#         arr = {}
#         for lang in references:
#             arr[lang] = 0
#             vals[lang] = []
#         fulltext = t.read().lower()
#         curr_context = tuple(fulltext[:k])
#         for c in fulltext[k + 1:]:
#             for r in references:
#                 if curr_context in references[r].dic.keys():
#                     prob = get_chance(references[r].dic[curr_context], c, a)
#                     if prob > 0:
#                         arr[r] = float(arr[r]) + math.log(prob, 2)
#                         vals[r].append(-math.log(prob, 2))
#
#                 elif a > 0:
#                     arr[r] = arr[r] + math.log((a / (a * len(references[r].alphabet))), 2)
#                     vals[r].append(-math.log((a / (a * len(references[r].alphabet))), 2))
#             curr_context = tuple([a for a in curr_context[1:]] + list(c))
#     plt.xticks(range(k, len(fulltext)), list(fulltext[k:]))
#     for ref in references:
#         filtered = lowpass(vals[ref], 0.1)
#         plt.plot(range(k + 1, len(fulltext)), filtered, label=ref)
#         threshold = - math.log(len(references[ref].alphabet), 2) / 2
#         stranger = get_stran(filtered, threshold)
#         print("the model considers ", ref, ": ", stranger)
#         for interval in (stranger):
#             word = ""
#             """
#             if interval[0][0] ==k+1:
#                 for j in range(interval[0][0]-k-1,interval[0][1]+1):
#                     word+=fulltext[j]
#             else:
#                 for j in range(interval[0][0],interval[0][1]+1):
#                     word+=fulltext[j]
#             print(word)
#             """
#             for j in range(interval[0][0] - k - 1, interval[0][1] + 1):
#                 word += fulltext[j]
#             print(word)
#         t = [-threshold for v in vals[ref]]
#         plt.plot(range(k + 1, len(fulltext)), t, label=ref + " threshold")
#     plt.legend(loc="upper left")
#
#     plt.show()
#     return {k: -v for k, v in sorted(arr.items(), key=lambda item: item[1], reverse=True)}
#
#
# compare_langs_test(3, 0.1)
