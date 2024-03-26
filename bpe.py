"""Example implementation of byte-pair encoding algorithm."""
import re, collections

def get_vocab(filename) -> dict[str,int]:
	"""Returns a dictionary of the file where keys are whitespace 
	separated words withs stop tokens and values are frequencies.

	{'h e l l o </w>': 3, ...}

	Args:
		filename: Of file to be processed into a dictionary

	Returns:
		dict[str,int]
	"""
	vocab = collections.defaultdict(int)
	with open(filename, 'r', encoding='utf-8') as fhand:
		for line in fhand:
			words = line.strip().split()
			for word in words:
				vocab[' '.join(list(word)) + ' </w>'] += 1
	return vocab

def get_stats(vocab):
	"""Returns a dictionary of the byte pairs and their frequencies.

	{'h', 'e': 3,...}

	Args:
		vocab: dict[str,int] of the text returned by get_vocab

	Returns:
		pairs: a dictionary indexed by byte pairs mapping to their frequencies.
	"""
	pairs = collections.defaultdict(int)
	for word, freq in vocab.items():
		symbols = word.split()
		for i in range(len(symobls)-1):
			pairs[symbols[i],symbols[i+1]] += freq
	return pairs

def merge_vocab(pair, v_in):
	"""Given a byte pair and v_in, a dict[str,int] of words returned by get_vocab,
	merges the vocabulary based on the most frequent byte pair.

	pair = 'e', 'l'
	{'h e l l o </w>': 3, ...} -> {'h el l o </w>': 3, ...}

	Args:
		pair: a byte pair
		v_in: input vocabulary

	Returns:
		v_out: output vocabulary, with the most frequent byte pair merged
	"""
	v_out = {}
	bigram = re.escape(' '.join(pair)) # what does this do?
	p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
	for word in v_in:
		w_out = p.sub(''.join(pair), word)
		v_out[w_out] = v_in[word]
	return v_out

def get_tokens(vocab):
	"""
	{'h e l l o </w>': 3, ...} -> {'h': 3, 'e': 3, 'l': 6, ...}
	"""
	tokens = collections.defaultdict(int)
	for word, freq in vocab.items():
		word_tokens = word.split()
		for token in word_tokens:
			tokens[token] += freq
	return tokens
