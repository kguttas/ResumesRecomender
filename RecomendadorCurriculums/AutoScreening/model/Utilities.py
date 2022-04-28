from tika import parser  # pip install tika
import uuid
import os
import pandas as pd
from .CleanText import CleanText


class Utilities:

    def __init__(self):
        print("Init Utilities...")

    def convert_resumes_files2dataframe(self, path_pdf_files):
        """
        Convierte archivos de tipo PDF a texto y retorna un dataframe con este esto
        :param path_pdf_files:
        :return: dataframe con el texto contenido en los PDFs
        """

        path_resumes_process = path_pdf_files

        data_raw = []

        for file in os.listdir(path_resumes_process):
            path_file = path_resumes_process + '/' + file

            print(path_file)

            raw = parser.from_file(path_file)

            data = {"_id": str(uuid.uuid4()), "text": str(raw['content']).strip(), "file_name": file}

            data_raw.append(data)

        df_CVs = pd.DataFrame(data_raw, columns=['_id', 'text', 'file_name'])

        return df_CVs

    def convert_text_job_offer(self, text):
        """
        Convierte el texto de la oferta de trabajo un dataframe con ID
        :param text:
        :return:
        """

        id_offer = str(uuid.uuid4())

        df_offer = pd.DataFrame([
            {"_id": id_offer,
             "text": text.strip(),
             "file_name": ''}
        ])

        return df_offer

    def concat_joboffer_CVs(self, df_offer, df_CVs):
        """
        Concatena el dataframe de la oferta de empleo con el dataframe de los CVs
        :param df_offer: dataframe oferta de empleo
        :param df_CVs: dataframe CVs
        :return: dataframes concatenados
        """
        df_for_process = pd.concat([df_CVs, df_offer], ignore_index=True)
        return df_for_process

    def preprocess_text(self, df_for_process, path_nltk_data):
        """
        Esta funcíon preprocesa el texto aplicando distintas técnicas para depurar el texto usadas en NLP
        :param df_for_process: dataframe con el texto
        :return: dataframe con el texto depurado
        """

        ct = CleanText(path_nltk_data)

        df_for_process["raw_text"] = df_for_process["text"]
        df_for_process['text'] = ct.cleanner_process(df_for_process["text"])

        return df_for_process

