import markovify
import sys

def make_markov():
	with open('tweet-corpus.txt','r') as f:
		text = f.read()

	model = markovify.NewlineText(text)
	return model


def tweet(model, length=140, out=sys.stdout):
	tweet = model.make_short_sentence(length) + '\n'
	out.write(tweet)


if __name__ == '__main__':
	model = make_markov()
	for _ in range(10):
		tweet(model)