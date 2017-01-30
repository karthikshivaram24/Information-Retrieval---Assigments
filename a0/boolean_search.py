""" Assignment 0

You will implement a simple in-memory boolean search engine over the jokes
from http://web.hawkesnest.net/~jthens/laffytaffy/.

The documents are read from documents.txt.
The queries to be processed are read from queries.txt.

Your search engine will only need to support AND queries. A multi-word query
is assumed to be an AND of the words. E.g., the query "why because" should be
processed as "why AND because."
"""
from collections import defaultdict
from collections import Counter
from nltk.stem import PorterStemmer
from itertools import groupby
import re


def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Remove all punctuation and split on whitespace.
    Here is a doctest: 
    >>> tokenize("Hi  there. What's going on?")
    ['hi', 'there', 'what', 's', 'going', 'on']
    """
    ###TODO
    pass
    without_pun = re.sub("[^\w\d\s]", " ", document).lower()
    without_mul_spaces = re.sub("\s+", " ", without_pun)
    tokens = re.split("\s+", without_mul_spaces.strip())
    return tokens


def create_index(tokens):
    """
    Create an inverted index given a list of document tokens. The index maps
    each unique word to a list of document ids, sorted in increasing order.
    Params:
      tokens...A list of lists of strings
    Returns:
      An inverted index. This is a dict where keys are words and values are
      lists of document indices, sorted in increasing order.
    Below is an example, where the first document contains the tokens 'a' and
    'b', and the second document contains the tokens 'a' and 'c'.
    >>> index = create_index([['a', 'b'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [0, 1]
    >>> index['b']
    [0]
    """
    ###TODO
    pass
    porter = PorterStemmer()
    invertedIndex = defaultdict(list)
    for individual_tokenList in tokens:
        normalizedList = []
        for token in individual_tokenList:
            normalizedList.append(porter.stem(token))
        for normalized_token in normalizedList:
            if normalized_token in invertedIndex and tokens.index(individual_tokenList)   :
                invertedIndex[normalized_token].append(tokens.index(individual_tokenList))
            else:
                invertedIndex[normalized_token] = [tokens.index(individual_tokenList)]

    return invertedIndex


def intersect(list1, list2):
    """ Return the intersection of two posting lists. Use the optimize
    algorithm of Figure 1.6 of the MRS text. Your implementation should be
    linear in the sizes of list1 and list2. That is, you should only loop once
    through each list.
    Params:
      list1....A list of document indices, sorted in ascending order.
      list2....Another list of document indices, sorted in ascending order.
    Returns:
      The list of document ids that appear in both lists, sorted in ascending order.
    >>> intersect([1, 3, 5], [3, 4, 5, 10])
    [3, 5]
    >>> intersect([1, 2], [3, 4])
    []
    """
    ###TODO
    pass
    answer = []
    list1_index = 0
    list2_index = 0
    while (len(list1) and len(list2) > 0) and (list1_index < len(list1) and list2_index < len(list2)):
        if (list1[list1_index] == list2[list2_index]):
            answer.append(list1[list1_index])
            list1_index += 1
            list2_index += 1
        elif list1[list1_index] < list2[list2_index]:
            list1_index += 1
        else:
            list2_index += 1
    return answer


def sort_by_num_postings(words, index):
    """
    Sort the words in increasing order of the length of their postings list in
    index. You may use Python's builtin sorted method.
    Params:
      words....a list of strings.
      index....An inverted index; a dict mapping words to lists of document
      ids, sorted in ascending order.
    Returns:
      A list of words, sorted in ascending order by the number of document ids
      in the index.

    >>> sort_by_num_postings(['a', 'b', 'c'], {'a': [0, 1], 'b': [1, 2, 3], 'c': [4]})
    ['c', 'a', 'b']
    """
    ###TODO
    pass
    sorted_list = []
    sorted_index_words = sorted(index, key=lambda k: len(index[k]), reverse=False)
    for sorted_index_word in sorted_index_words:
        if sorted_index_word in words:
            sorted_list.append(sorted_index_word)
    return sorted_list


def search(index, query):
    """ Return the document ids for documents matching the query. Assume that
    query is a single string, possibly containing multiple words. The steps
    are to:
    1. tokenize the query
    2. Sort the query words by the length of their postings list
    3. Intersect the postings list of each word in the query.

    If a query term is not in the index, then an empty list should be returned.

    Params:
      index...An inverted index (dict mapping words to document ids)
      query...A string that may contain multiple search terms. We assume the
      query is the AND of those terms by default.

    E.g., below we search for documents containing 'a' and 'b':
    >>> search({'a': [0, 1], 'b': [1, 2, 3], 'c': [4]}, 'a b')
    [1]
    """
    ###TODO
    pass
    porter = PorterStemmer()
    query_index = {}
    union_queryPostLists = []
    intersected_queryPostings = []
    query_tokens = tokenize(query)
    normalized_queryTokens = []
    for token in query_tokens:
        normalized_queryTokens.append(porter.stem(token))
    for normalized_queryToken in normalized_queryTokens:
        if normalized_queryToken in index:
            query_index[normalized_queryToken] = index[normalized_queryToken]

    for key in query_index:
        union_queryPostLists += query_index[key]
    union_queryPostLists = sorted(union_queryPostLists)
#   print(union_queryPostLists)

    frequency_dict = defaultdict()
    for value in union_queryPostLists:
        if value in frequency_dict:
            frequency_dict[value] += 1
        else:
            frequency_dict[value] = 1

#   print(frequency_dict)

    for key in frequency_dict:     #Has to be a better way for intersection try to modify this
        if frequency_dict[key] % len(query_index) == 0 or  frequency_dict[key] > len(query_index):
            intersected_queryPostings.append(key)
#   print(intersected_queryPostings)
    return sorted(intersected_queryPostings)


def main():
    """ Main method. You should not modify this. """
    documents = open('documents.txt').readlines()
    tokens = [tokenize(d) for d in documents]
    index = create_index(tokens)
    queries = open('queries.txt').readlines()
    for query in queries:
        results = search(index, query)
        print('\n\nQUERY:%s\nRESULTS:\n%s' % (query, '\n'.join(documents[r] for r in results)))


if __name__ == '__main__':
    main()
