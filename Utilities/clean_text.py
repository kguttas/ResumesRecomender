import string
import re
import nltk


class CleanText:

    def __init__(self):

        nltk.download('wordnet')

        self.data_original = None
        self.data_clean = None

    def cleanner_process(self, data_original):

        all_text = list()

        for item in data_original:

            text = [word.replace('\n', " ").replace('\x0c', " ") for word in item if word not in string.punctuation]

            text = ''.join(text)

            all_text.append(text)

        # Remover caracteres distintos a letras

        regex = re.compile('[^a-zA-Z ]')

        new_text = list()

        for item in all_text:
            text = regex.sub('', item)
            new_text.append(text)

        all_text = new_text.copy()

        # Remover palabras de largo 1 a 3
        new_text = list()

        for item in all_text:
            text = re.sub(r'\b\w{1,3}\b', ' ', item)
            new_text.append(text)

        all_text = new_text.copy()

        # Remover espacios extras
        new_text = list()

        for item in all_text:
            text = re.sub(" +", " ", item)
            new_text.append(text)

        all_text = new_text.copy()

        ps = nltk.PorterStemmer()

        new_list = list()
        for item in all_text:
            new_text = " ".join([ps.stem(word) for word in item.split(' ')])

            new_list.append(new_text)

        #all_text = new_list.copy()

        wn = nltk.WordNetLemmatizer()

        new_list = list()
        for item in all_text:
            new_text = " ".join([wn.lemmatize(word) for word in item.split(' ')])

            new_list.append(new_text)

        #all_text = new_list.copy()

        return all_text


