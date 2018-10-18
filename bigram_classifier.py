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

#======================================================================================
# Tokenizer function

def tokenizer(str):
  return str.replace("'", " '").replace(",", "").replace(".", "").replace('"', " '").lower().split(" ")


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

def get_bigram_array(file_lines):
  complete_review = ""

  for line in file_lines:
    complete_review += line

  sentences = complete_review.strip().replace("...", ",").replace("!", ".").replace("?", ".").split(".")
  token_array = []

  for sentence in sentences:
    tokenArray = bigram_tokenizer(sentence)

    for i in range(len(tokenArray) - 1):
      token_array.append(tokenArray[i] + " " + tokenArray[i + 1])

  return token_array


def bigram_tokenizer(sentence):
  sentence = "<s> " + sentence.strip()
  return sentence.replace("'", " '").replace("...", ",").replace(",", "").replace(".", " </s>").replace(")", "").replace("(", "").replace("'", " '").lower().split(" ")


def count_bigrams(sentence, sentiment):
  tokenArray = bigram_tokenizer(sentence)
  ngrams[0]["<s>"]["total"] += 1

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


def count_s(file_lines, sentiment):
  complete_review = ""
  token_array = []

  for line in file_lines:
    complete_review += line

  sentences = complete_review.replace("...", ",").replace("!", ".").replace("?", ".").replace(")", "").replace("(", "").replace("'", " '").replace('"', " '").lower().split(".")

  for sentence in sentences:
    count_bigrams(sentence,sentiment)


def prob_bigram(sentiment,k):
  for bigram in bigrams:
    bigram_tokens = bigram.split(" ")

    if bigram_tokens[0] in ngrams[0]:
      bigrams[bigram]["prob_"+sentiment]= math.log((float(bigrams[bigram][sentiment]+k) / float(ngrams[0][bigram_tokens[0]][sentiment]+ len(bigrams)*k)),2)


def test(testArray, vocab):
  result_positive=0
  result_negative=0

  for word in testArray:
      if word in vocab:
        if 'prob_positive' in vocab[word]:
          result_positive += vocab[word]["prob_positive"]
        if 'prob_negative' in vocab[word]:
          result_negative += vocab[word]["prob_negative"]
  # print('pos',result_positive, 'neg', result_negative)

  if result_positive > result_negative:
    return ("P")
  else:
    return ("N")


def ranking(vocab):
  for gram in vocab:
    if vocab[gram]["positive"] >= 50:
      ngrams[0][gram]["rank_positive"]= ngrams[0][gram]["prob_positive"]/ngrams[0][gram]["negative"]
      ngrams[0][gram]["rank_negative"]= ngrams[0][gram]["prob_negative"]/ngrams[0][gram]["positive"]
    else:
      ngrams[0][gram]["rank_positive"]=0
      ngrams[0][gram]["rank_negative"]=0

#======================================================================================
# Main function

# ngrams[0]["<s>"] = {"total": 0, "positive": 0, "negative": 0}

# for i in range(n_range):
#   filename = "N-train" + str(i) + ".txt"
#   file = open("train/"+filename, "r")
#   file_lines = file.readlines()

#   #Count words
#   count_words(file_lines, "negative")
#   count_grams(file_lines, "negative", 1)
#   count_s(file_lines, "negative")


# #Reads the files with positive movie reviews
# for i in range(n_range, p_range):
#   filename = "P-train" + str(i) + ".txt"
#   file = open("train/"+filename, "r")
#   file_lines = file.readlines()

#   #Count words
#   count_words(file_lines, "positive")
#   count_grams(file_lines, "positive", 1)
#   count_s(file_lines, "positive")

# # run probability functions for negative and positive reviews
# prob_bigram("negative", 1)
# prob_bigram("positive", 1)

# #Reads the test files with negative movie reviews
# f= open("results1.txt","w+")
# for i in range(0,25):
#   filename = "N-test" + str(i) + ".txt"
#   file = open("test/"+filename, "r")
#   file_lines = file.readlines()
#   testArray = get_bigram_array(file_lines)
#   # print (testArray)
#   f.write("%s %s\n" %("N-test" + str(i), test(testArray, bigrams)))


# #Reads the test files with positive movie reviews
# for i in range(25,50):
#   # testArray = []
#   filename = "P-test" + str(i) + ".txt"
#   file = open("test/"+filename, "r")
#   file_lines = file.readlines()
#   testArray = get_bigram_array(file_lines)
#   f.write("%s %s\n" %("P-test" + str(i), test(testArray, bigrams)))

# f.close()




# Read titles and classify genres

def split_files(filename, state):
  file= open(filename,"r")
  file_lines = file.readlines()
  file.close()
  f = open(filename,"w")
  if state== "train":
    print("no")
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


# split_files("data/train/train_movie_lines.txt", "train")
# split_files("data/test/test_movie_lines.txt", "test")
# split_files("data/train/train_movie_characters_metadata.txt", "train")
# split_files("data/test/test_movie_characters_metadata.txt", "test")
# split_files("data/train/train_movie_conversations.txt", "train")
# split_files("data/test/test_movie_conversations.txt", "test")