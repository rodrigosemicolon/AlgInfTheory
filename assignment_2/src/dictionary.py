class DictionaryModel:
    def __init__(self, lang, content, k, a):
        self.__k = k
        self.__alphabet = []
        self.__n_occurrences_all_c = 0
        self.__all_possible_contexts = 0
        self.__non_occ_contexts = 0
        self.__name = lang
        self.__dic = self.__make_dic(content, k)

    def __str__(self) -> str:
        """
        Returns a representation of the dictionary.

        :return: A string representing the object.
        """
        return self.__name + "\n" + str(self.__dic)

    def __make_dic(self, content: str, k: int) -> dict:
        """
        Splits a text. Iterate over the split text and creates a
        dictionary with all possible contexts and events.

        :param content: Text content.
        :param k: Context size.
        :return: Dictionary containing all the possible contexts as keys and all their
        respective possible next chars with a counter as values.
        """
        fulltext = content.lower()
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
        self.__non_occ_contexts = all_possible_contexts - key_count
        return matt_dic

    def __split_by_letters(self, text: str) -> list:
        """
        Iterates over a received string argument char by char and return a list with the split text
        while simultaneously updating the alphabet.

        :param text: String to split.
        :return: A list with the split text.
        """
        char_l = []

        for char in text:
            if char not in self.__alphabet:
                self.__alphabet.append(char)
            char_l.append(char)

        return char_l

    @property
    def name(self):
        return self.__name

    @property
    def dic(self):
        return self.__dic

    @property
    def alphabet(self):
        return self.__alphabet
