# Global variables
import math
import matplotlib.pyplot  as plt
from dictionary import DictionaryModel
from fcm import default_path, make_dic, n_occurrences_all_c, all_possible_contexts, alphabet, non_occ_contexts, get_context_chance, get_context_entropy, get_chance

default_target_path = "./example/target.txt"


def compare_langs(target, references, a, k):
    dic_results = {}
    max = 0
    vals={}
    with open(target,"r",encoding="utf8") as t:
        arr={}
        for lang in references:
            arr[lang.name]=0
            vals[lang.name]=[]
        fulltext=t.read().lower()
        curr_context = tuple(fulltext[:k])
        for c in fulltext[k+1:]:
            for r in references:
                if curr_context in r.dic.keys():
                    prob=get_chance(r.dic[curr_context],c,a)
                    if prob>0:
                        arr[r.name]=float(arr[r.name]) + math.log(prob,2)
                        vals[r.name].append(math.log(prob,2))

                elif a>0:
                    arr[r.name]=arr[r.name] + math.log((a/(a*len(r.alphabet))),2)  
                    vals[r.name].append(math.log((a/(a*len(r.alphabet))),2))                 
            curr_context= tuple([a for a in curr_context[1:]] + list(c))
    plt.xticks(range(k,len(fulltext)),list(fulltext[k:]))
    for ref in references:
        filtered=lowpass(vals[ref.name],0.7)
        plt.plot(range(k+1,len(fulltext)),filtered,label=ref.name) 
        threshold = math.log(len(ref.alphabet),2)/2
        stranger=get_stran(filtered,-threshold)
        print("the model considers ",ref.name, ": ",stranger)
        for interval in (stranger):
            word=""
            """
            if interval[0][0] ==k+1:
                for j in range(interval[0][0]-k-1,interval[0][1]+1):
                    word+=fulltext[j]
            else:
                for j in range(interval[0][0],interval[0][1]+1):
                    word+=fulltext[j]
            print(word)
            """
            for j in range(interval[0][0]-k-1,interval[0][1]+1):
                word+=fulltext[j]
            print(word)
        t = [-threshold for v in vals[ref.name]]
        plt.plot(range(k+1,len(fulltext)),t,label=ref.name + " threshold") 
    plt.legend(loc="upper left")
    
    plt.show()
   
    return {tup[0]:-tup[1] for tup in arr.items()}
   
def get_stran(data,thresh):
    blocks=[]
    i=0
    flag = [False for i in data]
    for i in range(len(data)):
        if data[i]>=thresh and not flag[i]:
            val=data[i]
            beg=i
            end=i
            for j in range(i+1,len(data)):
                if data[j]>=thresh:
                    val+=data[j]
                    flag[j]=True
                    end=j
                else:
                    break
            if beg!=end:    
                blocks.append(((beg,end),val))
        flag[i]=True

    
    return blocks

def lowpass(data,alpha):
    filtered=[0 for i in data]
    filtered[0]=alpha*data[0]
    for i in range(1,len(data)):
       filtered[i]=filtered[i-1] + alpha*(data[i]-filtered[i-1])
    return filtered
   
    #         if r.name in dic_results:
    #             if dic_results[r.name] > max:
    #                 max = dic_results[r.name]
    # for r in dic_results:
    #     if dic_results[r] == max:
    #         print(r)
    #         print(max)
    #for r in dic_results:
    #    print(r,dic_results[r])
"""
def lowpassfilter(data,weight):
    minimum = min(data)
    #print(minimum)
    #filtered[0]=data[0]#(weight*data[0])
    filtered=[0 for i in data]
    filtered[0]=data[0]*weight
    for i in range(1,len(data)):
        filtered[i]=filtered[i-1] + weight*(data[i]-filtered[i-1])
        print(filtered,"\n\n\n")
    return filtered
"""
if __name__ == "__main__":
    k = 2
    a = 0.1
    p = default_path
    t = default_target_path
    l = 200
    # read dictionaries
    dic_en = DictionaryModel("./example/test_en.txt", k, a)
    dic_es = DictionaryModel("./example/test_es.txt", k, a)
    dic_pt = DictionaryModel("./example/test_pt.txt", k, a)
    print(compare_langs("./example/target.txt", [dic_en, dic_es, dic_pt], a,k))
    
    
    # prior = "god"
    # args = sys.argv
    # for i in range(len(args)):
    #     if i % 2 == 0:
    #         if args[i - 1] == "-k":
    #             k = int(args[i])
    #         elif args[i - 1] == "-a":
    #             a = float(args[i])
    #         elif args[i - 1] == "-p":
    #             p = args[i]
    #         elif args[i - 1] == "-l":
    #             l = int(args[i])
    #         elif args[i - 1] == "-pr":
    #             prior = args[i]
    # if 0 <= a <= 1:
    #     if len(prior) == k:
    #         d = make_dic(p, k)
    #         print("Generated text with:\nk=", k, "\na=", a, "\np=", p, "\nl:", l, "\nprior:", prior, "\n-----\n" + generate_text(d, prior, k, l, a))
    #     else:
    #         print("Context size and given prior size don't match")
    # else:
    #     print("Alpha must be >=0 & <=1, exiting...")
