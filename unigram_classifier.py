# -*- coding: utf-8 -*-
#!/usr/bin/python
import operator
import math

n_range = 300
p_range = 600

total_words_review = {"positive": 0, "negative": 0}
ngrams = [{}, {}, {}]
ourVocab = {}
simpleVocab = [{}, {}, {}, {}]
movieArray={}

#======================================================================================
# Tokenizer function

def tokenizer(str):
  return str.replace("'", " '").replace(",", "").replace(".", "").lower().split(" ")


#======================================================================================
# Count the total amount of words in a given review

def count_words(file_lines, sentiment):
  for line in file_lines:
    tokenArray = tokenizer(line)

    if sentiment == "positive":
      total_words_review["positive"] += len(tokenArray)
    if sentiment == "negative":
      total_words_review["negative"] += len(tokenArray)

#======================================================================================
# Aggregates the total of words per positive and negative sentiment and its total
# Save the ngrams and count occurrences

def count_grams(file_lines, sentiment, level):
  for line in file_lines:
    tokenArray = tokenizer(line)

    i = 0
    while i < len(tokenArray) - (level - 1):
      bigram_token = tokenArray[i]

      j = 1
      while j < level - 1:
        bigram_token = bigram_token + " " + tokenArray[i + j]
        j += 1

      if level == 1:
        bigram_token = tokenArray[i]
      elif level == 2:
        bigram_token = tokenArray[i] + " " + tokenArray[i + 1]
      elif level == 3:
        bigram_token = tokenArray[i] + " " + tokenArray[i + 1] + " " + tokenArray[i + 2]

      if bigram_token in ngrams[level-1]:
        ngrams[level-1][bigram_token]["total"] += 1
      else:
        ngrams[level-1][bigram_token] = {"positive": 0, "negative": 0, "total": 1}

      if sentiment == "positive":
        ngrams[level-1][bigram_token]["positive"] += 1
      if sentiment == "negative":
        ngrams[level-1][bigram_token]["negative"] += 1

      i += 1

bigrams = {}

def bigram_tokenizer(sentence):
  sentence = "<s> " + sentence.strip()
  return sentence.replace("'", " '").replace("...", ",").replace(",", "").replace(".", " </s>").lower().split(" ")

def count_bigrams(sentence, sentiment):
  tokenArray = bigram_tokenizer(sentence)

  i = 0

  while i < len(tokenArray) - 1:
    bigram_token = tokenArray[i] + " " + tokenArray[i + 1]

    if bigram_token in bigrams:
      bigrams[bigram_token]["total"] += 1
    else:
      bigrams[bigram_token] = {"positive": 0, "negative": 0, "total": 1}

    if sentiment == "positive":
      bigrams[bigram_token]["positive"] += 1
    if sentiment == "negative":
      bigrams[bigram_token]["negative"] += 1

    i += 1

#======================================================================================
# Sort the grams by target: total, negative or positive

def sortGrams(vocab, target):
  return sorted(vocab.items(), key=lambda x: x[1][target])


#======================================================================================
# Save in ourVocab the grams which the occurrences are greater or equal to 25

def save25(vocab):
  for gram in vocab:
    if vocab[gram]["total"] >= 25:
      ourVocab[gram] = vocab[gram]["total"]

#======================================================================================
# Save the words that occure a specific number of times in a given vocab

def simpleSave(vocab, number):
  for gram in vocab:
    if vocab[gram]["total"] == number:
      simpleVocab[number-1][gram] = vocab[gram]["total"]

#======================================================================================
# Returns the conditional probablity per sentiment on a given vocab

def cond_probability(vocab, sentiment, k):
  result = 0
  # print(vocab);
  for gram in vocab:

    # frequency of word wi (vocab[gram]) in the positive/negative reviews divided by
    # the total number of words in the positive/negative reviews

    result += math.log((float(vocab[gram][sentiment] +k) / float(total_words_review[sentiment] + len(vocab)*k)),2);
    vocab[gram]["prob_"+sentiment]= math.log((float(vocab[gram][sentiment]+k) / float(total_words_review[sentiment] + len(vocab)*k)),2);


  return result



def prob_bigram(file_lines, sentiment, k):
  complete_review = ""
  token_array = []

  for line in file_lines:
    complete_review += line

  complete_review = complete_review.replace("...", ",")
  complete_review = complete_review.replace("!", ".").replace("?", ".")

  sentences = complete_review.split(".")

  for sentence in sentences:
    count_bigrams(sentence, sentiment)

  for bigram in bigrams:

    # bigramArray = tokenizer(bigram)

    for unigram in ngrams[0]:
      if bigram.split(" ")[0] == unigram:
        # print(vocab2[bigram][sentiment], vocab1[unigram][sentiment])
        bigrams[bigram]["prob_positive"]= math.log((float(bigrams[bigram]["positive"]+k) / float(ngrams[0][unigram]["positive"]+ len(bigrams)*k)),2)
        bigrams[bigram]["prob_negative"]= math.log((float(bigrams[bigram]["negative"]+k) / float(ngrams[0][unigram]["negative"]+ len(bigrams)*k)),2)



def test(testarray, vocab):
  result_positive=0
  result_negative=0

  for word in testArray:
    for gram in vocab:
      if word==gram:
        result_positive += vocab[gram]["prob_positive"]
        result_negative += vocab[gram]["prob_negative"]
  # print("pos", result_positive, "neg", result_negative)
  if result_positive > result_negative:
    return ("P")
  else:
    return ("N")


  def rank(vocab):
    for gram in vocab:
      ngrams[0][gram]["rank_positive"]= ngrams[0][gram]["prob_positive"]/ngrams[0][gram]["negative"]
      ngrams[0][gram]["rank_negative"]= ngrams[0][gram]["prob_negative"]/ngrams[0][gram]["positive"]


def split_files(filename, state):
  file= open(filename,"r")
  file_lines = file.readlines()
  file.close()
  f = open(filename,"w")
  if state== "train":
    for line in file_lines:
      l=line.split(" +++$+++ ")
      num=int(l[2][1:])
      if num<566:
        f.write(line)

  elif state == "test":
    for line in file_lines:
      l=line.split(" +++$+++ ")
      num=int(l[2][1:])
      if num>565:
        f.write(line)
      
  f.close()


def lines_movie(moviefile, titlefile):
  linesfile= open(moviefile,"r")
  movie_lines = linesfile.readlines()
  titlefile= open(titlefile,"r")
  title_lines = titlefile.readlines()
  for line1 in title_lines:
      l=line1.replace("\n", "").split(" +++$+++ ")
      movieArray[l[0]]={}
      movieArray[l[0]]["title"]=l[1]
      movieArray[l[0]]["genre"]=l[5]

  for line2 in movie_lines:
      l=line2.replace("\n", "").split(" +++$+++ ")
      new_l= tokenizer(l[4])
      if "script" in movieArray[l[2]]:
        movieArray[l[2]]["script"].append(new_l)
      else:
        movieArray[l[2]]["script"]=[new_l]

  linesfile.close()
  titlefile.close()
  

#======================================================================================
# Main function
# Read titles and classify genres


lines_movie("data/train/movie_lines.txt", "data/train/movie_titles_metadata.txt")
print(movieArray)

# split_files("data/train/movie_lines.txt", "train")
# split_files("data/test/movie_lines.txt", "test")
# split_files("data/train/movie_characters_metadata.txt", "train")
# split_files("data/test/movie_characters_metadata.txt", "test")
# split_files("data/train/movie_conversations.txt", "train")
# split_files("data/test/movie_conversations.txt", "test")



#Reads the files with negative movie reviews
# for i in range(n_range):
#   filename = "N-train" + str(i) + ".txt"
#   file = open("train/"+filename, "r")
#   file_lines = file.readlines()

#   #Count words
#   count_words(file_lines, "negative")

#   # Count the unigrams
#   count_grams(file_lines, "negative", 1)

#   # Count the bigrams
#   count_grams(file_lines, "negative", 2)

#   # Count the trigrams
#   count_grams(file_lines, "negative", 3)

#Reads the files with positive movie reviews
# for i in range(n_range, p_range):
#   filename = "P-train" + str(i) + ".txt"
#   file = open("train/"+filename, "r")
#   file_lines = file.readlines()

#   #Count words
#   count_words(file_lines, "positive")

#   # Count the unigrams
#   count_grams(file_lines, "positive", 1)

#   # Count the bigrams
#   count_grams(file_lines, "positive", 2)

#   # Count the trigrams
#   count_grams(file_lines, "positive", 3)


# print ("N=1: ", len(ngrams[0]))
# print ("N=2: ", len(ngrams[1]))
# print ("N=3: ", len(ngrams[2]))

# Save the grams in ourVocab, the ones that occur >= 25 times
save25(ngrams[0])
save25(ngrams[1])
save25(ngrams[2])

# Extract the 10 more frequent words
sorted_n1 = sortGrams(ngrams[0], "total")
# print ("N=1: ", sorted_n1)

# print ("Length of our vocabulary: ", len(ourVocab))

for i in range(0, 5):
  for j in range(0, 3):
    simpleSave(ngrams[j], i)

# The double loop above refactors:
# simpleSave(ngrams[0], 1)
# simpleSave(ngrams[1], 1)
# simpleSave(ngrams[2], 1)
# simpleSave(ngrams[0], 2)
# simpleSave(ngrams[1], 2)
# simpleSave(ngrams[2], 2)
# simpleSave(ngrams[0], 3)
# simpleSave(ngrams[1], 3)
# simpleSave(ngrams[2], 3)
# simpleSave(ngrams[0], 4)
# simpleSave(ngrams[1], 4)
# simpleSave(ngrams[2], 4)

# print ("Words that have 1 occurence: ", len(simpleVocab[0]))
# print ("Words that have 2 occurences: ", len(simpleVocab[1]))
# print ("Words that have 3 occurences: ", len(simpleVocab[2]))
# print ("Words that have 4 occurences: ", len(simpleVocab[3]))

# print ("Total number of words in negative reviews",  total_words_review["negative"])
# print ("Total number of words in positive reviews",  total_words_review["positive"])

# print ("Conditional probability of positive language model with k=1", cond_probability(ngrams[0], "positive", 1))
# print ("Conditional probability of negative language model with k=1", cond_probability(ngrams[0], "negative", 1))

# print ("Conditional probability of positive language model with k=0.75", cond_probability(ngrams[0], "positive", 0.75))
# print ("Conditional probability of negative language model with k=0.75", cond_probability(ngrams[0], "negative", 0.75))



#Reads the test files with negative movie reviews
# file= open("movie_lines.txt","r")
# trainArray=[]
  
# file_lines = file.readlines()
# for line in file_lines:
#   l=line.replace("\n", "").split(" +++$+++ ")
#   print(l[])
  # testArray += tokenizer(line)

  # f.write("%s %s\n" %("N-test" + str(i), test(testArray, ngrams[0])))


# #Reads the test files with positive movie reviews
# for i in range(25,50):
#   testArray=[]
#   filename = "P-test" + str(i) + ".txt"
#   file = open("test/"+filename, "r")
#   file_lines = file.readlines()
#   for line in file_lines:
#     testArray += tokenizer(line)
#   # f.write("%s %s\n" %("P-test" + str(i), test(testArray, ngrams[0])))



