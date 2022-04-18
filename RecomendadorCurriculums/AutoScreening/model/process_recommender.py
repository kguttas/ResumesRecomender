from RecomendadorCurriculums.AutoScreening.model import Utilities
from RecomendadorCurriculums.AutoScreening.model import AutoScreeningModel

class ProcessRecommender:

    def __init__(self, path_model_word2vec, path_resumes, top_recommendation, text_offer):
        print("Process Recommender")

        self.path_model_word2vec = path_model_word2vec
        self.path_resumes = path_resumes
        self.top_recommendation = top_recommendation
        self.text_offer = text_offer

    def start(self):
        print("Start process...")

        util = Utilities.Utilities()

        df_CVs = util.convert_resumes_files2dataframe(self.path_resumes)

        print(df_CVs.head())

        df_offer = util.convert_text_job_offer(self.text_offer)

        print(df_offer)

        id_offer = df_offer["_id"].iloc[0]
        print(id_offer)

        df_for_process = util.concat_joboffer_CVs(df_offer, df_CVs)

        # print(df_for_process)

        df_text_clean = util.preprocess_text(df_for_process)

        # print(df_text_clean)

        model = AutoScreeningModel.AutoScreeningModel(self.path_model_word2vec)

        corpus = model.generate_corpus(df_text_clean)

        # print(corpus)

        model.build_vocab(corpus)

        # Solo para probar
        #most_similar = model.get_most_similar("dharamvirsinghgmailcom")

        # print(most_similar)

        recommended = model.recommendations(id_offer, df_text_clean, self.top_recommendation)

        return recommended


