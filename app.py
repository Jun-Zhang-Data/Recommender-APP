import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

data = pd.read_csv('movies.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(data['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

data = data.reset_index()
indices = pd.Series(data.index, index=data['title'])
all_titles = [data['title'][i] for i in range(len(data['title']))]

def recommendations_(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    titles = data['title'].iloc[movie_indices]
    dates = data['release_date'].iloc[movie_indices]
    retrieved_data = pd.DataFrame(columns=['Title','Year'])
    retrieved_data['Title'] = titles
    retrieved_data['Year'] = dates
    return retrieved_data

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
            
    if flask.request.method == 'POST':
        m = flask.request.form['movie_name']
        m = m.title()
#        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        if m not in all_titles:
            return(flask.render_template('unretrieved.html',name=m))
        else:
            retrieved_movies = recommendations_(m)
            m_names = []
            m_dates = []
            for i in range(len(retrieved_movies)):
                m_names.append(retrieved_movies.iloc[i][0])
                m_dates.append(retrieved_movies.iloc[i][1])

            return flask.render_template('retrieved.html',movie_names=m_names,movie_date=m_dates,search_name=m)

if __name__ == '__main__':
    app.run()