import random
import sys

# method and global variables import from fcm.py
from fcm import alphabet, get_chance, make_dic, default_path


def generate_text(model: dict, prior: str, k: int, length: int, alpha: float) -> str:
    """
    Returns the calculated probability of a char to appear after a context.

    :param model: Dictionary containing contexts and event counts.
    :param prior: String from which we start generating.
    :param k: Context size.
    :param length: Number of characters to be generated.
    :param alpha: Smoothing parameter.
    :return: String consisting of the prior and the generated text.
    """
    context = tuple(prior[-k:])
    n = 0
    if force_seed:
        random.seed(10)
    text = prior
    while n < length:
        chances = {}
        if context in model:  # if we found the context in the model we get each chars chances from it
            for c in alphabet:
                chances[c] = get_chance(model[context], c, alpha)

         
            next = random.choices(list(chances.keys()), weights=list(chances.values()))  # random char based on the models probabilities

        else:  # if the context didnt occur, we get a random character from the models alphabet
            next = random.choices(alphabet)
        text += next[0]
        context = tuple([a for a in context[1:]] + next)  # update the context

        n += 1
    return text


if __name__ == "__main__":
    k = 3
    a = 0
    p = default_path
    l = 200
    s = 10
    force_seed = False
    prior = "goddess"
    args = sys.argv
    for i in range(len(args)):
        if i % 2 == 0:
            if args[i - 1] == "-k":
                k = int(args[i])
            elif args[i - 1] == "-a":
                a = float(args[i])
            elif args[i - 1] == "-p":
                p = args[i]
            elif args[i - 1] == "-l":
                l = int(args[i])
            elif args[i - 1] == "-pr":
                prior = args[i]
        if args[i] == "-f":
            force_seed = True
    if len(args) == 1:
        print("Executing without params, try using:\n\nk: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "p: Path to text file;\n"
              "l: Length of generated text;\n"
              "pr: Starting initial context.\n"
              "f: Force hardcoded seed.(Just param is needed, no value)\n\n")
    elif len(args) == 2 and args[len(args) - 1] == "-h":
        print("Use:\n\nk: Context size;\n"
              "a: Alpha smoothing parameter;\n"
              "p: Path to text file;\n"
              "l: Length of generated text;\n"
              "pr: Starting initial context.\n"
              "f: Force hardcoded seed.(Just param is needed, no value)\n\n")
    if 0 <= a <= 1 and (len(args) >= 1 and args[len(args) - 1] != "-h"):
        
        if len(prior)>=k:
            print("Generating text with:\nk=", k, "\na=", a, "\np=", p, "\nl:", l, "\nprior:", prior, "\nforce seed:", force_seed, "\n-----\n")
            d = make_dic(p, k)
            print(generate_text(d, prior, k, l, a))
        else:
            print("Prior length must be equal or larger than k")
    else:
        if not (0 <= a <= 1):
            print("Alpha must be >=0 & <=1, exiting...")
