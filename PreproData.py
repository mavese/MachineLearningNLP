import json
import spacy
import pprint

def main():

	## Get list of word vectors
	# wordEmb = []
	# with open("word_emb.json") as f:
	# 	wordEmb = json.load(f)


	# ## Get dictionary of words to indexes
	# wordDic = {}
	# with open("word_dictionary.json") as f:
	# 	wordDic = json.load(f)

	jsnDic = {}
	with open("dev-v2.0.json") as f:
		jsnDic = json.load(f)

	jsnDic = jsnDic['data'][0]['paragraphs']

	contexts = []
	questions = []
	isPossibles = []
	answers = []

	i = 0
	for item in jsnDic:
		contextString = item['context'].replace("''", '" ').replace("``", '" ')
		contexts.append(tokenizeWords(contextString))
		questions.append([])
		isPossibles.append([])
		answers.append([])
		
		for ques in item['qas']:
			questionString = ques['question'].replace("''", '" ').replace("``", '" ')
			questions[i].append(tokenizeWords(questionString))
			isPossibles[i].append(not ques['is_impossible'])
			ind = []
			q = []
			for ans in ques['answers']:
				ind.append(ans['answer_start']) #convert to tokens
				q.append(ans['text'])
			if ind:
				idx = max(set(ind), key=ind.count)
				answers[i].append((idx, len(q[ind.index(idx)])))

		i += 1
	pp =pprint.PrettyPrinter()
	pp.pprint(answers)
	# cDoc = nlp(context)

	# qDoc = nlp(question)

	# aDoc = nlp(answer)

	# vectorized = []
	# for word in cDoc:
	# 	if word.text in wordDic:
	# 		vectorized.append(wordEmb[wordDic[word.text]])

	# for vector in vectorized:
	# 	print(vector)

def tokenizeWords(corpus, useLarge=False):
	nlp = spacy.load("en_core_web_sm") if not useLarge else spacy.load("en_core_web_lg")
	return [word.text for word in nlp(corpus)]

if __name__ == '__main__':
	main()