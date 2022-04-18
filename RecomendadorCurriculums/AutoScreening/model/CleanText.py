import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re

class CleanText:

    def __init__(self):

        nltk.download('wordnet')

        nltk.download('omw-1.4')

        nltk.download('stopwords')

        self.data_original = None
        self.data_clean = None

    def removeNonAscii(self, s):
        return "".join(i for i in s if ord(i) < 128)

    def make_lower_case(self, text):
        return text.lower()

    def remove_stop_words(self, text):
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)
        return text

    def remove_html(self, text):
        html_pattern = re.compile('<.*?>')
        return html_pattern.sub(r'', text)

    def remove_punctuation(self, text):
        tokenizer = RegexpTokenizer(r'\w+')
        text = tokenizer.tokenize(text)
        text = " ".join(text)
        return text

    def cleanner_process(self, data_original):

        all_text = list()

        new_text = list()

        # Remover saltos de lineas
        for item in data_original:

            text = [word.replace('\n', " ").replace('\x0c', " ") for word in item if word not in string.punctuation]

            text = ''.join(text)

            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        new_text = list()

        for item in all_text:

            text = self.remove_stop_words(item)

            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        new_text = list()

        for item in all_text:
            text = self.removeNonAscii(item)

            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        new_text = list()

        for item in all_text:
            text = self.remove_html(item)

            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        new_text = list()

        for item in all_text:
            text = self.remove_punctuation(item)

            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        new_text = list()

        # Transformar el texo a minusculas
        for item in all_text:

            text = [word.lower() for word in item]

            text = ''.join(text)

            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        #print(all_text)

        # Remover caracteres distintos a letras

        regex = re.compile('[^a-zA-Z ]')

        new_text = list()

        for item in all_text:
            text = regex.sub('', item)
            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        new_text = list()

        for item in all_text:
            text = re.sub(r'^https?:\/\/.*[\r\n]*', '', item, flags=re.MULTILINE)
            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        # Remover palabras de largo 1 a 3
        # new_text = list()
        #
        # for item in all_text:
        #     text = re.sub(r'\b\w{1,3}\b', ' ', item)
        #     new_text.append(text)
        #
        # all_text = new_text.copy()
        #
        # print(len(all_text))

        # Remover espacios extras
        new_text = list()

        for item in all_text:
            text = re.sub(" +", " ", item)
            new_text.append(text)

        all_text = new_text.copy()

        print(len(all_text))

        # aplicar Stemm
        # ps = nltk.PorterStemmer()
        #
        # new_list = list()
        # for item in all_text:
        #     new_text = " ".join([ps.stem(word) for word in item.split(' ')])
        #
        #     new_list.append(new_text)
        #
        # all_text = new_list.copy()
        #
        # print(len(all_text))

        # Lematizar
        wn = nltk.WordNetLemmatizer()

        new_list = list()
        for item in all_text:
            new_text = " ".join([wn.lemmatize(word) for word in item.split(' ')])

            new_list.append(new_text)

        all_text = new_list.copy()

        print(len(all_text))

        return all_text


