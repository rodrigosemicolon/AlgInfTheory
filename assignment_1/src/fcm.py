import math
import sys

# Global variables
alphabet = []  # alphabet seen in the file
n_occurrences_all_c = 0  # number of recorded occurrences in the file
non_occ_contexts = 0  # number of possible contexts that never occurred in the file
all_possible_contexts = 0  # number of total possible contexts taking into account the context and alphabet size
default_path = "../example/example.txt"


def split_by_letters(text: str) -> list:
    global alphabet
    """
    Iterate received string argument char by char and return a list with the split text
    while simulteanously updating our alphabet.

    :param text: String to split.
    :return: A list with the split text.
    """
    char_l = []
    for char in text:
        if char not in alphabet:
            alphabet.append(char)
        char_l.append(char)

    return char_l


def make_dic(filepath: str, k: int) -> dict:
    """
    Reads a text file and then splits the text. Iterate over the split text and create a
    dictionary with all possible contexts and events.

    :param filepath: Path for file.
    :param k: Context size.
    :return: Dictionary containing all the possible contexts as keys and all their
    respective possible next chars with a counter as values.
    """
    global n_occurrences_all_c, all_possible_contexts, non_occ_contexts
    with open(filepath, "r", encoding="utf8") as f:
        fulltext = f.read()
        matt_dic = {}
        fulltext = split_by_letters(fulltext)

        for a, _ in enumerate(fulltext[:-(k)]):
            context = tuple(fulltext[a:a + k])
            nextword = fulltext[a + k]

            if not context in matt_dic.keys():
                matt_dic[context] = {}

            if not nextword in matt_dic[context].keys():
                matt_dic[context][nextword] = 1
                n_occurrences_all_c += 1
            else:
                current_occ = matt_dic[context][nextword]
                matt_dic[context][nextword] = current_occ + 1
                n_occurrences_all_c += 1

        all_possible_contexts = pow(len(alphabet), k)
        key_count = len(matt_dic.keys())
        non_occ_contexts = all_possible_contexts - key_count  # len(matt_dic.keys())
    return matt_dic


def get_chance(next_chars: dict, event: str, alpha: float) -> float:
    """
    Returns the calculated probability of a char to appear after a context.

    :param next_chars: All the possible chars of a given context.
    :param event: The next char to consider for a probability.
    :param alpha: Smoothing parameter.
    :return: Probability of an event.
    """
    totalsum = sum(next_chars.values())
    occurrences = 0
    if event in next_chars.keys():
        occurrences = next_chars[event]
    return (occurrences + alpha) / (totalsum + (alpha * len(alphabet)))


def get_context_chance(next_chars: dict, alpha: float) -> float:
    """
    Returns the probability of a given context.
    :param next_chars: All the possible chars of a given context.
    :param alpha: Smoothing parameter.
    :return: Probability of a context.
    """
    context_occ = sum(next_chars.values()) + len(alphabet) * alpha
    all_context_occ = n_occurrences_all_c + all_possible_contexts * len(alphabet) * alpha

    return context_occ / all_context_occ


def get_context_entropy(next_chars: dict, alpha: float) -> float:
    """
    Calculates the entropy of a given context considering the alpha as a smoothing parameter.

    :param next_chars: All the chars and their frequencies of a given context.
    :param alpha: Smoothing parameter.
    :return: Negative result of the calculated context entropy.
    """
    result = 0
    for c in alphabet:
        pec = get_chance(next_chars, c, alpha)
        if pec > 0:
            result += pec * math.log(pec, 2)
    return - result


def get_total_entropy(dic: dict, alpha: float) -> float:
    """
        Returns the total entropy of a text given a dictionary and alpha smoothening parameter.
        It first calculates the context entropy for a non-occurring but possible context (given the alphabet), then it multiplies
        it to the number of all non-occurring but possible contexts
        Finally we add that to the sum of the context entropy of the recorded contexts
    :param dic: Dictionary with contexts
    :param alpha: Smoothing parameter
    :return: Float with the calculated total entropy.
    """
    non_existing_entropy = 0
    if alpha != 0:
        all_context_occ = n_occurrences_all_c + all_possible_contexts * len(alphabet) * alpha
        prob_empty_context = (alpha * len(alphabet)) / all_context_occ
        aux = alpha / (alpha * len(alphabet))
        empty_context_entropy = -aux * math.log(aux, 2) * len(alphabet)
        non_existing_entropy += (prob_empty_context * empty_context_entropy) * non_occ_contexts

    return sum([get_context_entropy(dic[s], alpha) * get_context_chance(dic[s], alpha) for s in dic]) + non_existing_entropy


if __name__ == "__main__":
    # default values
    k = 3
    a = 0
    p = default_path
    args = sys.argv
    for i in range(len(args)):
        if i % 2 == 0:
            if args[i - 1] == "-k":
                k = int(args[i])
            elif args[i - 1] == "-a":
                a = float(args[i])
            elif args[i - 1] == "-p":
                p = args[i]
    if len(args) == 1:
        print("Executing without params, try using:\n\nk: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "p: Path to text file.\n\n")
    elif len(args) == 2 and args[len(args) - 1] == "-h":
        print("Use:\n\nk: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "p: Path to text file.\n\n")

    if 0 <= a <= 1 and (len(args) >= 1 and args[len(args) - 1] != "-h"):
        print("Calculating total entropy with:\nk=", k, "\na=", a, "\np=", p, "\n-----\n")
        d = make_dic(p, k)
        print("Calculated total:", get_total_entropy(d, a))
    else:
        if not (0 <= a <= 1 ):
            print("Alpha must be >=0 & <=1, exiting...")
