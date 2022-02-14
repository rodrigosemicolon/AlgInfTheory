import math


class DictionaryModel:
    def __init__(self, lang,content, k, a):
        self.__k = k
        self.__alphabet = []
        self.__n_occurrences_all_c = 0
        self.__all_possible_contexts = 0
        self.__non_occ_contexts = 0
        self.__name = lang
        self.__dic = self.__make_dic(content, k)
        self._information_amount = self.__calc_information_amount(a)

    def __str__(self):
        return str(self.__dic)

    def __calc_information_amount(self, alpha) -> float:
        # nao sei se isto aplica-se a isto
        # verificar casos com 0, possiveis estrangeirismos e/ou erros ortograficos
        non_existing_entropy = 0
        if alpha != 0:
            all_context_occ = self.__n_occurrences_all_c + self.__all_possible_contexts * len(self.__alphabet) * alpha
            prob_empty_context = (alpha * len(self.__alphabet)) / all_context_occ
            aux = alpha / (alpha * len(self.__alphabet))
            empty_context_entropy = -aux * math.log(aux, 2) * len(self.__alphabet)
            non_existing_entropy += (prob_empty_context * empty_context_entropy) * self.__non_occ_contexts

        return sum([self.get_context_entropy(self.__dic[s], alpha) for s in self.__dic]) + non_existing_entropy

    def get_context_entropy(self, next_chars: dict, alpha: float) -> float:
        result = 0
        for c in self.__alphabet:
            pec = self.__get_chance(next_chars, c, alpha)
            if pec > 0:
                result += pec * math.log(pec, 2)
        return - result

    def __get_chance(self, next_chars: dict, event: str, alpha: float) -> float:
        totalsum = sum(next_chars.values())
        occurrences = 0
        if event in next_chars.keys():
            occurrences = next_chars[event]
        return (occurrences + alpha) / (totalsum + (alpha * len(self.__alphabet)))

    def __get_chance(self, next_chars: dict, event: str, alpha: float) -> float:
        totalsum = sum(next_chars.values())
        occurrences = 0
        if event in next_chars.keys():
            occurrences = next_chars[event]
        return (occurrences + alpha) / (totalsum + (alpha * len(self.__alphabet)))

    def __make_dic(self, content: str, k: int) -> dict:
        # with open(filepath, "r", encoding="utf8") as f:
        fulltext = content.lower() # meti lower só para ser mais facil testar cenas agora
        matt_dic = {}
        fulltext = self.__split_by_letters(fulltext)

        for a, _ in enumerate(fulltext[:-(k)]):
            context = tuple(fulltext[a:a + k])
            nextword = fulltext[a + k]

            if not context in matt_dic.keys():
                matt_dic[context] = {}

            if not nextword in matt_dic[context].keys():
                matt_dic[context][nextword] = 1
                self.__n_occurrences_all_c += 1
            else:
                current_occ = matt_dic[context][nextword]
                matt_dic[context][nextword] = current_occ + 1
                self.__n_occurrences_all_c += 1

        all_possible_contexts = pow(len(self.__alphabet), k)
        key_count = len(matt_dic.keys())
        self.__non_occ_contexts = all_possible_contexts - key_count  # len(matt_dic.keys())
        return matt_dic

    # TODO fazer regex aqui?
    # retirar pontuação e numeros
    def __split_by_letters(self, text: str) -> list:
        char_l = []

        for char in text:
            if char not in self.__alphabet:
                self.__alphabet.append(char)
            char_l.append(char)

        return char_l

    @property
    def information_amount(self):
        return self._information_amount

    @property
    def name(self):
        return self.__name

    @property
    def dic(self):
        return self.__dic

    @property
    def alphabet(self):
        return self.__alphabet