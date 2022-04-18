import os
import urllib.request
from flask import Flask, request, redirect, jsonify
import json
import uuid
import shutil
from RecomendadorCurriculums.AutoScreening.model import process_recommender

import configparser

# Get config variables from file
config = configparser.ConfigParser()

path_config_file = "webapi.conf"

config.read(path_config_file)

print("API REST Naive Model")

app = Flask(__name__)
UPLOAD_FOLDER = os.path.basename('upload_files')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', '3gp', 'mov'])
app.config['UPLOAD_FOLDER'] = config['paths']['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

path_model_word2vec = config['paths']['path_model_word2vec']

path_resumes = config['paths']['path_resumes']

top_recommendation = int(config['paths']['top_recommendation'])

@app.route("/test")
def handle_person():
    return "Hello Person!"


@app.route('/file-upload', methods=['POST'])
def upload_file():
    if request.method == "POST":
        uploaded_files = request.files.getlist("file[]")

        form = request.form

        data_form = request.form.getlist(None)

        job_offer_str = data_form[0]

        job_offer = json.loads(job_offer_str)

        print(job_offer["JobOffer"])

        # Nueva carpeta para el trabajo
        id_name_folfer = str(uuid.uuid4())

        path_folder = os.path.join(app.config["UPLOAD_FOLDER"], id_name_folfer)

        if os.path.exists(path_folder):
            shutil.rmtree(path_folder)

        os.mkdir(path_folder)

        for file in uploaded_files:
            file.save(os.path.join(path_folder, file.filename))

        proc = process_recommender.ProcessRecommender(path_model_word2vec, path_folder, top_recommendation, job_offer["JobOffer"])

        recommended = proc.start()

        recommended["file_name"] =  recommended["file_name"].apply(lambda x: id_name_folfer + "\\" + x)

        result_data = recommended.to_json(orient="records",  date_format='iso')

        return result_data, 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
