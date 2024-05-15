import pandas as pd


data_path = '.'
courses = pd.read_csv(f"{data_path}/courses.csv")

from sklearn.feature_extraction.text import TfidfVectorizer



from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix


def get_recommendations(title):
    data_path = '.'
    courses = pd.read_csv(f"{data_path}/data.csv")
    tfidf = TfidfVectorizer(stop_words='english')
    courses['overview'] = courses['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(courses['overview'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(courses.index, index=courses['name']).drop_duplicates()
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:4]

    movie_indices = [i[0] for i in sim_scores]

    recom = courses['name'].iloc[movie_indices]

    recom = courses['name'].iloc[movie_indices]
    course_recom_1 = recom.iloc[0]
    course_recom_2 = recom.iloc[1]
    course_recom_3 = recom.iloc[2]

    return course_recom_1, course_recom_2, course_recom_3


from flask import Flask, request
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/recommend", methods=["POST"])
def create_summary():

    data = request.get_json()
    input = data.get("input")
    if not input:
        return {"error": "Input is required"}, 400


    rec_1, rec_2, rec_3 = get_recommendations(input)
    summary_data = {
        "rec_1":rec_1,
        "rec_2":rec_2,
        "rec_3":rec_3,
    }
    return summary_data, 201

if __name__ == '__main__':
    app.run(debug=True)
    