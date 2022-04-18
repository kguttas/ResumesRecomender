import pandas as pd
import copy
import pickle
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

class AutoScreeningModel:
    """
    This class is a dummy machine learning model
    """
    def __init__(self, path_model):
        """
        Constructor of class
        """
        self.data = dict()

        self.model = Word2Vec.load(path_model)

    def fit(self, data_in):
        """
        This method is for training data model
        :param data_in: argument of type DataFrame
        :return:
        """

        # Get mean of columns in dataframe
        aux_data = data_in.mean(axis=0)

        # Convert result to list
        aux_data = aux_data.to_dict()

        # Save in class data
        self.data = aux_data

    def predict(self, data_in):
        """
        This method is for evaluate model
        :param data_in: argument of type DataFrame, this contains new data for do predictions.
        :return:
        """

        # Deep copy data for don't modify input data
        new_data = copy.deepcopy(data_in)

        # Iterate over input data
        for key in new_data:

            divider = 1

            try:
                # Get divider , if this is not equal to zero then use for division
                if self.data[key] != 0:
                    divider = self.data[key]
            except KeyError as e:
                # If index key don't exists then print message of error
                print(f"Index not found, message: {str(e)}")

            # Update column with new data divided for divider
            new_data[key] = new_data[key].div(divider)

        return new_data

    def save(self, path_file_data):
        """
        This method is for save model in file.
        :param path_file_data: path to file
        :return:
        """
        file_handler = open(path_file_data, 'wb')
        pickle.dump(self.data, file_handler, 0)
        file_handler.close()

    def load(self, path_file_data):
        """
        this method is for load model from file
        :param path_file_data: path to file
        :return:
        """
        file_handler = open(path_file_data, 'rb')
        self.data = pickle.load(file_handler)
        file_handler.close()

    def generate_corpus(self, df_for_process):
        """
        Este método genera el corpus a partir de un dataframe con la columna 'text'
        :param df_for_process: dataframe con la columna 'text'
        :return: list de palabras que conforman el corpus
        """
        i = 0
        corpus = []
        for words in df_for_process['text']:
            corpus.append(words.split())
            corpus.append(words)

        return corpus

    def build_vocab(self, corpus):
        """
        Este método actualiza el vocabulario del modelo
        :param corpus: list con el corpus
        :return: Nada
        """
        self.model.build_vocab(corpus, update=True)

    def get_most_similar(self, text):
        """
        Este método retorna un listado con las palabras probables más cercanas al input text
        :param text: palabra
        :return: listado de palabras cercanas
        """
        return self.model.wv.most_similar(positive=[text])

    def vectors(self, x, df: pd.DataFrame):

        # Creating a list for storing the vectors (description into vectors)
        # global word_embeddings
        word_embeddings = []

        # Reading the each book description
        for line in df['text']:
            avgword2vec = None
            count = 0
            for word in line.split():
                if word in self.model.wv.key_to_index:
                    count += 1
                    if avgword2vec is None:
                        avgword2vec = self.model.wv[word]
                    else:
                        avgword2vec = avgword2vec + self.model.wv[word]

            if avgword2vec is not None:
                avgword2vec = avgword2vec / count

                word_embeddings.append(avgword2vec)
        return word_embeddings

    def recommendations(self, title, df: pd.DataFrame, top):

        # Calling the function vectors

        word_embeddings = self.vectors(df, df)

        # finding cosine similarity for the vectors

        cosine_similarities = cosine_similarity(word_embeddings, word_embeddings)

        # taking the title and book image link and store in new data frame called books
        books = df[['_id', 'raw_text', 'file_name']]
        # Reverse mapping of the index
        indices = pd.Series(df.index, index=df['_id'].values.astype('str')).drop_duplicates()

        idx = indices[title]

        # print(len(word_embeddings))
        sim_scores = list(enumerate(cosine_similarities[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # print(sim_scores)

        top_recount =  len(sim_scores) if len(sim_scores) < (top + 1) else top + 1

        sim_scores = sim_scores[1:top_recount]  # DESDE 1 PARA OCULTAR LA OFERTA
        book_indices = [i[0] for i in sim_scores]
        scores_values = [i[1] for i in sim_scores]
        recommend = books.iloc[book_indices]

        output = []

        countIndex = 0
        for index, row in recommend.iterrows():
            # print(row['title'] )
            # print(scores_values[countIndex])

            output.append(
                [countIndex + 1,
                 row['raw_text'],
                 row['_id'], row['file_name'], scores_values[countIndex], index])

            countIndex += 1

            # response = requests.get(row['image_link'])
            # img = Image.open(BytesIO(response.content))
            # plt.figure()
            # plt.imshow(img)
            # plt.title(row['title'])

        result = pd.DataFrame(output,
                              columns=["rank", "common_texts", "title", "file_name", "cosine_similarity", "index_df"])

        return result
