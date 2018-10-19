import nltk
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

movies={}
characters={}
movie_lines=[]

categories = ["comedy", "romance", "adventure", "biography", "drama", "history",
"action", "crime", "thriller", "mystery", "sci-fi", "fantasy", "horror", "music", "western",
"war", "adult", "musical", "animation", "sport", "family", "short", "film-noir", "documentary"]

######### LOAD MOVIES #########
with open('data/train/movie_titles_metadata.txt', 'r', errors='ignore') as f:
  lines = f.readlines()

for line in lines:
  l = list(map(lambda x: x.strip(), line.split("+++$+++")))

  d = {
    "movieID": l[0],
    "title": l[1],
    "year": l[2],
    "rating": l[3],
    "votes": l[4],
    "genre": eval(l[5]),
    "lines": [],
    "target": 0
  }

  movies[l[0]] = d

######### LOAD MOVIE LINES #########
with open('data/train/movie_lines.txt', 'r', errors='ignore') as f:
  lines = f.readlines()

for line in lines:
  l = list(map(lambda x: x.strip(), line.lower().split("+++$+++")))
  d = {
    "lineID": l[0],
    "characterID": l[1],
    "movieID": l[2],
    "characterName": l[3],
    "line": l[4]
  }

  movie_lines.append(d)

  movies[l[2]]["lines"].append(l[4])


  # print (movies[l[2]]["genre"])
  # print (movies[l[2]]["title"])

  movies[l[2]]["target"] = categories.index(movies[l[2]]["genre"][0])

train = {
  "data": [],
  "target": []
}

for key in movies:

  train["data"].append(' '.join(movies[key]["lines"]))

  train["target"].append(movies[key]["target"])
  if key == "m108":
    print (train["target"])


count_vect = CountVectorizer()

X_train_counts = count_vect.fit_transform(train["data"])

X_train_counts.shape
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape

clf = MultinomialNB().fit(X_train_tfidf, train["target"])

docs_new = ['love you darling', 'hell', 'kill', 'fbi', 'crap', 'darling', 'honey', "happy", "I'm just glad we're still together, Lisa, because I need you this yearen"]
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, cat in zip(docs_new, predicted):
  print ("The sentence:", doc)
  print ("Belongs to the genre:", categories[cat])
  print ()
  # print('%r => %s' % (doc, twenty_train.target_names[category]))






######### LOAD CHARACTERS #########
with open('data/train/movie_characters_metadata.txt', 'r', errors='ignore') as f:
  lines = f.readlines()

for line in lines:
  l = list(map(lambda x: x.strip(), line.split("+++$+++")))
  d = {
    "characterID": l[0],
    "name": l[1],
    "movieId": l[2],
    "title": l[3],
    "gender": l[4],
    "relevance": l[5],
    "lines": [],
    "tokens": []
  }

  characters[l[0]] = d

######### LOAD CHARACTERS LINES #########
tokenizer = RegexpTokenizer(r'\w+')

# count_vect = CountVectorizer()

for ml in movie_lines:
  characters[ml["characterID"]]["lines"].append(ml["line"])
  # characters[ml["characterID"]]["tokens"].append(tokenizer.tokenize(ml["line"]))



# X_train_counts = count_vect.fit_transform(characters[ml["characterID"]]["lines"])
# X_train_counts.shape

# print (X_train_counts.shape)

# tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
# X_train_tf = tf_transformer.transform(X_train_counts)
# X_train_tf.shape



# clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

# docs_new = ['God', 'FBI']
# X_new_counts = count_vect.transform(docs_new)
# X_new_tfidf = tfidf_transformer.transform(X_new_counts)

# predicted = clf.predict(X_new_tfidf)

# for doc, category in zip(docs_new, predicted):
#   print('%r => %s' % (doc, twenty_train.target_names[category]))

# 'God is love' => soc.religion.christian
# 'OpenGL on the GPU is fast' => comp.graphics


def getMovieLines(movieId):
  return 1

def getCharacterLines(characterId):
  return 1

def getMovieMeta(movieId):
  return 1

def getCharacterMeta(characterId):
  return 1

def getMoviesByGenre(genreId):
  return 1

genres = {}

def getMovieGenres():
  for i in movies:
    current_genres = movies[i]["genre"]

    for genre in current_genres:

      if genre in genres:
        genres[genre] += 1
      else:
        genres[genre] = 1

  # for genre in genres:
  #   print (genre, genres[genre])

getMovieGenres()

  # f.write("%s %s\n" %("N-test" + str(i), test(testArray, ngrams[0])))


categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

twenty_train.target_names