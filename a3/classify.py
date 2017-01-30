"""
Assignment 3. Implement a Multinomial Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

from collections import defaultdict
import collections
import glob
import math
import os


class Document(object):
    """ A Document. Do not modify.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename=None, label=None, tokens=None):
        """ Initialize a document either from a file, in which case the label
        comes from the file name, or from specified label and tokens, but not
        both.
        """
        if label:  # specify from label/tokens, for testing.
            self.label = label
            self.tokens = tokens
        else:  # specify from file.
            self.filename = filename
            self.label = 'spam' if 'spmsg' in filename else 'ham'
            self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):
    def __init__(self, condprob=None, priors=None, vocab=None):
        self.conditional_prob_map = condprob
        self.prior_map = priors
        self.vocabulary_set = vocab

    def get_word_probability(self, label, term):
        """
        Return Pr(term|label). This is only valid after .train has been called.

        Params:
          label: class label.
          term: the term
        Returns:
          A float representing the probability of this term for the specified class.

        >>> docs = [Document(label='spam', tokens=['a', 'b']), Document(label='spam', tokens=['b', 'c']), Document(label='ham', tokens=['c', 'd'])]
        >>> nb = NaiveBayes()
        >>> nb.train(docs)
        >>> nb.get_word_probability('spam', 'a')
        0.25
        >>> nb.get_word_probability('spam', 'b')
        0.375
        """
        ###TODO
        pass
        cond_prob = self.conditional_prob_map
        result = 0.0
        if term in cond_prob:
            temp = cond_prob[term]
            for tup in temp:
                if tup[0] == label:
                    result = tup[1]

        return result

    def get_top_words(self, label, n):
        """ Return the top n words for the specified class, using the odds ratio.
        The score for term t in class c is: p(t|c) / p(t|c'), where c'!=c.

        Params:
          labels...Class label.
          n........Number of values to return.
        Returns:
          A list of (float, string) tuples, where each float is the odds ratio
          defined above, and the string is the corresponding term.  This list
          should be sorted in descending order of odds ratio.

        >>> docs = [Document(label='spam', tokens=['a', 'b']), Document(label='spam', tokens=['b', 'c']), Document(label='ham', tokens=['c', 'd'])]
        >>> nb = NaiveBayes()
        >>> nb.train(docs)
        >>> nb.get_top_words('spam', 2)
        [(2.25, 'b'), (1.5, 'a')]
        """
        ###TODO
        pass
        cond_prob = self.conditional_prob_map
        odds_ratio_results = []

        for term in cond_prob:
            odds_ratio = 0.0
            temp_list = cond_prob[term]
            # print(temp_list)
            if temp_list[0][0] == label:
                odds_ratio = temp_list[0][1] / temp_list[1][1]

            elif temp_list[1][0] == label:
                odds_ratio = temp_list[1][1] / temp_list[0][1]

            odds_ratio_results.append((odds_ratio, term))

        odds_ratio_results.sort(key=lambda tup: tup[0], reverse=True)

        return odds_ratio_results[:n]

    def train(self, documents):
        """
        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your
        book. Store these as instance variables, to be used by the classify
        method subsequently.
        Params:
          documents...A list of training Documents.
        Returns:
          Nothing.
        """
        ###TODO
        pass
        all_tokens = []
        classes = ["spam", "ham"]
        N = len(documents)
        N_spam = 0.0
        N_ham = 0.0
        spam_text = []
        ham_text = []
        for doc in documents:
            label = doc.label
            tokens = doc.tokens
            all_tokens.append(tokens)
            if label == "spam":
                N_spam += 1.0
                spam_text.append(tokens)
            if label == "ham":
                N_ham += 1.0
                ham_text.append(tokens)

        prior_spam = N_spam / N
        prior_ham = N_ham / N

        vocabulary = set([val for sublist in all_tokens for val in sublist])

        spam_text = [val for sublist in spam_text for val in sublist]

        ham_text = [val for sublist in ham_text for val in sublist]

        spam_map = collections.Counter(spam_text)

        ham_map = collections.Counter(ham_text)

        sum_spam_term_count = 0.0

        sum_ham_term_count = 0.0

        for cls in classes:
            if cls == "spam":
                for term in vocabulary:
                    if term in spam_map:
                        sum_spam_term_count += (spam_map[term] + 1.0)
                    else:
                        sum_spam_term_count += 1.0
            elif cls == "ham":
                for term in vocabulary:
                    if term in ham_map:
                        sum_ham_term_count += (ham_map[term] + 1.0)
                    else:
                        sum_ham_term_count += 1.0

        conditional_prob = defaultdict(list)

        for cls in classes:
            if cls == "spam":
                for term in vocabulary:
                    if term in spam_map:
                        cond_prob = (spam_map[term] + 1.0) / sum_spam_term_count
                        conditional_prob[term].append(("spam", cond_prob))
                    else:
                        cond_prob = 1.0 / (sum_spam_term_count)
                        conditional_prob[term].append(("spam", cond_prob))

            elif cls == "ham":
                for term in vocabulary:
                    if term in ham_map:
                        cond_prob = (ham_map[term] + 1.0) / sum_ham_term_count
                        conditional_prob[term].append(("ham", cond_prob))
                    else:
                        cond_prob = 1.0 / sum_ham_term_count
                        conditional_prob[term].append(("ham", cond_prob))

        self.conditional_prob_map = conditional_prob
        self.prior_map = {"spam": prior_spam, "ham": prior_ham}
        self.vocabulary_set = vocabulary

    def classify(self, documents):
        """ Return a list of strings, either 'spam' or 'ham', for each document.
        Params:
          documents....A list of Document objects to be classified.
        Returns:
          A list of label strings corresponding to the predictions for each document.
        """
        ###TODO
        pass

        classes = ["spam", "ham"]
        priors = self.prior_map
        conditional_prob = self.conditional_prob_map
        results = defaultdict(list)
        label = []
        for doc in documents:
            common_tokens_W = []
            tokens = doc.tokens
            # terms = set(tokens)
            for word in tokens:
                if word in self.vocabulary_set:
                    common_tokens_W.append(word)
            # common_term_W = set(terms).intersection(self.vocabulary_set)
            for cls in classes:
                score_c = math.log(priors[cls])
                for token in common_tokens_W:
                    temp = conditional_prob[token]
                    cond_prob = 0.0
                    if temp[0][0] == cls:
                        cond_prob = temp[0][1]
                    elif temp[1][0] == cls:
                        cond_prob = temp[1][1]
                    score_c += math.log(cond_prob)
                results[documents.index(doc)].append((cls, score_c))

        for doc_id in sorted(results.keys()):
            tup_list = results[doc_id]
            if tup_list[0][1] >= tup_list[1][1]:
                label.append(tup_list[0][0])
            else:
                label.append(tup_list[1][0])

        return label


def evaluate(predictions, documents):
    """ Evaluate the accuracy of a set of predictions.
    Return a tuple of three values (X, Y, Z) where
    X = percent of documents classified correctly
    Y = number of ham documents incorrectly classified as spam
    X = number of spam documents incorrectly classified as ham

    Params:
      predictions....list of document labels predicted by a classifier.
      documents......list of Document objects, with known labels.
    Returns:
      Tuple of three floats, defined above.
    """
    ###TODO
    pass
    correct_pred = 0.0

    true_labels = []

    X = 0.0
    Y = 0.0

    for doc in documents:
        true_labels.append(doc.label)

    for i, j in zip(predictions, true_labels):
        if i == j:
            correct_pred += 1.0

        elif i != j:
            if j == "spam":
                X += 1.0
            elif j == "ham":
                Y += 1.0

    return (correct_pred / len(predictions), Y, X)


def main():
    """ Do not modify. """
    if not os.path.exists('train'):  # download data
        from urllib.request import urlretrieve
        import tarfile
        urlretrieve('http://cs.iit.edu/~culotta/cs429/lingspam.tgz', 'lingspam.tgz')
        tar = tarfile.open('lingspam.tgz')
        tar.extractall()
        tar.close()
    train_docs = [Document(filename=f) for f in glob.glob("train/*.txt")]
    print('read', len(train_docs), 'training documents.')
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(filename=f) for f in glob.glob("test/*.txt")]
    print('read', len(test_docs), 'testing documents.')
    predictions = nb.classify(test_docs)
    results = evaluate(predictions, test_docs)
    print('accuracy=%.3f, %d false spam, %d missed spam' % (results[0], results[1], results[2]))
    print('top ham terms: %s' % ' '.join('%.2f/%s' % (v, t) for v, t in nb.get_top_words('ham', 10)))
    print('top spam terms: %s' % ' '.join('%.2f/%s' % (v, t) for v, t in nb.get_top_words('spam', 10)))


if __name__ == '__main__':
    main()
