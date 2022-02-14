# Global variables
import math
import os
import sys
import time

from matplotlib import pyplot as plt
from dictionary import DictionaryModel
from fcm import default_path, make_dic, n_occurrences_all_c, all_possible_contexts, alphabet, non_occ_contexts, get_context_chance, get_context_entropy, get_chance
from language import calc_bits
DEF_TARGET_PATH = "../example/targets/"
DEF_REFERENCE_PATH = "../example/models/"
# ERROR_METHOD = 'replace'
# ERROR_METHOD = 'ignore'
DEF_MODEL_PATH = "../example/models/"
DEF_BOOK_PATH = "../example/_books/"


def get_stran(data, thresh):
    blocks = []
    i = 0
    flag = [False for i in data]
    for i in range(len(data)):
        if data[i] <= thresh and not flag[i]:
            val = data[i]
            beg = i
            end = i
            for j in range(i + 1, len(data)):
                if data[j] >= thresh:
                    val += data[j]
                    flag[j] = True
                    end = j
                else:
                    break
            if beg != end:
                blocks.append(((beg, end), val))
        flag[i] = True

    return blocks


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
                        vals[r].append(math.log(prob, 2))

                elif a > 0:
                    arr[r] = arr[r] + math.log((a / (a * len(references[r].alphabet))), 2)
                    vals[r].append(math.log((a / (a * len(references[r].alphabet))), 2))
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


# def read_model(model_path: str, k: int, a: float) -> DictionaryModel:
#     with open(model_path, "r", encoding="utf-8") as model:
#         return DictionaryModel(model_path.split("/")[3][:-4], model.read(), k, a)

def read_models(path,k, a) -> dict:
    # l_langs = []
    #dicts = {}
    lang_models=[]
    for f in os.walk(path):
        #print(f)
        for model_file in f[2]:
            #lang = f[0].split("/")[-1]
            name = model_file.split(".txt")[0]
            #print(name)
            with open(path + model_file, "r", encoding="utf-8") as concatenated_books:
                
                lang_models.append(DictionaryModel(name,concatenated_books.read(),k,a))
                #dicts[lang] = DictionaryModel(lang, concatenated_books.read(), k, a)
    return lang_models#dicts

def cat_references(reference_path,model_path):
    for f in os.walk(reference_path):
        lang = f[0].split("/")[-1]
        #print("lang")
        fulltext=""
        for ref_file in f[2]:
            with open(f[0] + "/" + ref_file,"r",encoding="utf8") as ref:
                fulltext+=ref.read()+"\n"
        with open(model_path + lang + ".txt","w",encoding="utf8") as mod:
            mod.write(fulltext)

def recognition(models,targetfile,k,a):
    scores={}
    with open(targetfile,"r",encoding="utf8") as tfile:
        target_text=tfile.read()
    for model in models:
        scores[model.name]=calc_bits(model,target_text,k,a)
    sorted_scores={k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=False)}
    return sorted_scores
if __name__ == "__main__":
    #cat_references("../example/c_books/","../example/models/")
    #x=read_models("../example/models/",k,a)
    #for m in x:
    #    print(m.name)
    #print(recognition(x,"../example/example3.txt",k,a))
    
    k = -1
    a = -1
    mp, tp, rp = -1, -1, -1
    args = sys.argv
    args = sys.argv
    k_flag=False
    a_flag=False
    tp_flag=False
    mp_flag=False
    rp_flag=False
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
            elif args[i-1] == "-rp":
                rp=args[i]
                rp_flag=True 
    if len(args) == 1:
        print("Executing without params, try using:\n\n"
              "k: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "tp: Path to specific target text file;\n"
              "mp: Path to specific reference model text file;\n"
              "rp: Path to a folder containing folders which contain texts that will make up a model (optional)\n")
        sys.exit()
    elif len(args) == 2 and args[len(args) - 1] == "-h":
        print("Use:\n\n"
              "k: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "tp: Path to specific target text file;\n"
              "mp: Path to specific reference model text file;\n"
              "rp: Path to a folder containing folders which contain texts that will make up a model (optional)\n")
        sys.exit()
    if not (k_flag and a_flag and tp_flag and mp_flag):
        print("Not all parameters have valid values")
        sys.exit()        
    if rp_flag:
        cat_references(rp,mp)
    models = read_models(mp,k,a)
    scores = recognition(models,tp,k,a)
    for k in scores:
        print(k,scores[k])

 
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
