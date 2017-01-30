""" Assignment 1

Here you will implement a search engine based on cosine similarity.

The documents are read from documents.txt.gz.

The index will store tf-idf values using the formulae from class.

The search method will sort documents by the cosine similarity between the
query and the document (normalized only by the document length, not the query
length, as in the examples in class).

The search method also supports a use_champion parameter, which will use a
champion list (with threshold 10) to perform the search.

"""
from collections import defaultdict
from collections import Counter
import codecs
import gzip
import math
import re


class Index(object):

    def __init__(self, filename=None, champion_threshold=10):
        """ DO NOT MODIFY.
        Create a new index by parsing the given file containing documents,
        one per line. You should not modify this. """
        if filename:  # filename may be None for testing purposes.
            self.documents = self.read_lines(filename)
            print("done1")
            toked_docs = [self.tokenize(d) for d in self.documents]
            print("done2")
            self.doc_freqs = self.count_doc_frequencies(toked_docs)
            print("done3")
            self.index = self.create_tfidf_index(toked_docs, self.doc_freqs)
            print("done4")
            self.doc_lengths = self.compute_doc_lengths(self.index)
            print("done5")
            self.champion_index = self.create_champion_index(self.index, champion_threshold)
            print("done6")

    def compute_doc_lengths(self, index):
        """
        Return a dict mapping doc_id to length, computed as sqrt(sum(w_i**2)),
        where w_i is the tf-idf weight for each term in the document.

        E.g., in the sample index below, document 0 has two terms 'a' (with
        tf-idf weight 3) and 'b' (with tf-idf weight 4). It's length is
        therefore 5 = sqrt(9 + 16).

        >>> lengths = Index().compute_doc_lengths({'a': [[0, 3]], 'b': [[0, 4]]})
        >>> lengths[0]
        5.0
        """
        ###TODO
        pass
        lengths_map = {}
        list_docwieght = defaultdict(list)
        for term in index:
            doc_list = index[term]
            for item in doc_list:
                if item[0] in list_docwieght:
                    list_docwieght[item[0]].append(item[1])
                else:
                    list_docwieght[item[0]].append(item[1])
        for doc_id in list_docwieght:
            sum = 0
            for item in list_docwieght[doc_id]:
                sum += item ** 2
            length = sum ** (0.5)
            lengths_map[doc_id] = length

        return lengths_map



    def create_champion_index(self, index, threshold=10):
        """
        Create an index mapping each term to its champion list, defined as the
        documents with the K highest tf-idf values for that term (the
        threshold parameter determines K).

        In the example below, the champion list for term 'a' contains
        documents 1 and 2; the champion list for term 'b' contains documents 0
        and 1.

        >>> champs = Index().create_champion_index({'a': [[0, 10], [1, 20], [2,15]], 'b': [[0, 20], [1, 15], [2, 10]]}, 2)
        >>> champs['a']
        [[1, 20], [2, 15]]
        """
        ###TODO
        pass

        champion_index = {}

        for term in index:
            list_pair = index[term]
            sorted_list_pair = sorted(list_pair, key= lambda list: list[1] , reverse = True)
            champion_index[term] = sorted_list_pair[:threshold]

        return champion_index



    def create_tfidf_index(self, docs, doc_freqs):
        """
        Create an index in which each postings list contains a list of
        [doc_id, tf-idf weight] pairs. For example:

        {'a': [[0, .5], [10, 0.2]],
         'b': [[5, .1]]}

        This entry means that the term 'a' appears in document 0 (with tf-idf
        weight .5) and in document 10 (with tf-idf weight 0.2). The term 'b'
        appears in document 5 (with tf-idf weight .1).

        Parameters:
        docs........list of lists, where each sublist contains the tokens for one document.
        doc_freqs...dict from term to document frequency (see count_doc_frequencies).

        Use math.log10 (log base 10).

        >>> index = Index().create_tfidf_index([['a', 'b', 'a'], ['a']], {'a': 2., 'b': 1., 'c': 1.})
        >>> sorted(index.keys())
        ['a', 'b']
        >>> index['a']
        [[0, 0.0], [1, 0.0]]
        >>> index['b']  # doctest:+ELLIPSIS
        [[0, 0.301...]]
        """
        ###TODO
        pass

        tfdf_index = {}

        doc_term_tdf = {}

        all_terms = set({})

        for sub_list in docs:
              for item in sub_list:
                  all_terms.add(item)

        for term in all_terms:
            for sub_list in docs:
                doc_index = docs.index(sub_list)
                term_freq = 0

                for key in sub_list:
                    if key == term:
                        term_freq +=1
                if term in doc_term_tdf:
                    doc_term_tdf[term].append([doc_index,term_freq])
                else:
                    doc_term_tdf[term] = [[doc_index,term_freq]]


        idf_map = {}

        for key_term in doc_freqs:
            idf_value = math.log10(len(docs)/doc_freqs[key_term])
            idf_map[key_term] = idf_value


        for term in doc_term_tdf :
            doc_list = doc_term_tdf[term]
            for item in doc_list:
                 weight = 0
                 if item[1] > 0 :
                     idf = idf_map[term]
                     weight = (1 + math.log10(item[1])) * (idf)
                 if term in tfdf_index:
                     tfdf_index[term].append([item[0],weight])
                 elif term not in tfdf_index:
                     tfdf_index[term] = [[item[0],weight]]

        return tfdf_index


    def count_doc_frequencies(self, docs):
        """ Return a dict mapping terms to document frequency.
        >>> res = Index().count_doc_frequencies([['a', 'b', 'a'], ['a', 'b', 'c'], ['a']])
        >>> res['a']
        3
        >>> res['b']
        2
        >>> res['c']
        1
        """
        ###TODO
        pass
        unified_list = []
        doc_freq_dummy = {}
        actual_doc_freq = {}
        for term_list in docs:
            unified_list.extend(term_list)
        for term in unified_list:
            if term not in doc_freq_dummy:
                doc_freq_dummy[term] = set({})
        for doc_terms in docs:
            for term in doc_terms:
                if term in doc_freq_dummy:
                    doc_freq_dummy[term].add(docs.index(doc_terms))

        for key in doc_freq_dummy:
            if key not in actual_doc_freq:
                actual_doc_freq[key] = len(doc_freq_dummy[key])

        return actual_doc_freq




    def query_to_vector(self, query_terms):
        """ Convert a list of query terms into a dict mapping term to inverse document frequency (IDF).
        Compute IDF of term T as N / log10(document frequency of T), where N is the total number of documents.
        You may need to use the instance variables of the Index object to compute this. Do not modify the method signature.

        If a query term is not in the index, simply omit it from the result.

        Parameters:
          query_terms....list of terms

        Returns:
          A dict from query term to IDF.
        """
        ###TODO
        pass
        index  = Index()
        doc_freq = index.doc_freqs
        n = len(index.documents)
        query_vector = {}

        for term in query_terms:
            if term in doc_freq :
                if doc_freq[term] > 0:
                    idf = n/(math.log10(doc_freq[term]))
                else:
                    idf = 0
                if term not in query_vector:
                    query_vector[term] = idf

        return query_vector




    def search_by_cosine(self, query_vector, index, doc_lengths):
        """
        Return a sorted list of doc_id, score pairs, where the score is the
        cosine similarity between the query_vector and the document. The
        document length should be used in the denominator, but not the query
        length (as discussed in class). You can use the built-in sorted method
        (rather than a priority queue) to sort the results.

        The parameters are:

        query_vector.....dict from term to weight from the query
        index............dict from term to list of doc_id, weight pairs
        doc_lengths......dict from doc_id to length (output of compute_doc_lengths)

        In the example below, the query is the term 'a' with weight
        1. Document 1 has cosine similarity of 2, while document 0 has
        similarity of 1.

        >>> Index().search_by_cosine({'a': 1}, {'a': [[0, 1], [1, 2]]}, {0: 1, 1: 1})
        [(1, 2.0), (0, 1.0)]
        """
        ###TODO
        pass

        scores = defaultdict(lambda: 0)
        for query_term, query_weight in query_vector.items():
                 for doc_id, doc_weight in index[query_term]:
                        scores[doc_id] += query_weight * doc_weight  # part of dot product

        for doc_id in scores:
             scores[doc_id] /= doc_lengths[doc_id]
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def search(self, query, use_champions=False):
        """ Return the document ids for documents matching the query. Assume that
        query is a single string, possible containing multiple words. Assume
        queries with multiple words are AND queries. The steps are to:

        1. Tokenize the query (calling self.tokenize)
        2. Convert the query into an idf vector (calling self.query_to_vector)
        3. Compute cosine similarity between query vector and each document (calling search_by_cosine).

        Parameters:

        query...........raw query string, possibly containing multiple terms (though boolean operators do not need to be supported)
        use_champions...If True, Step 4 above will use only the champion index to perform the search.
        """
        ###TODO
        pass

        #index = Index()
        doc_length = self.doc_lengths
        final_index = self.index

        query_tokens = self.tokenize(query)
        query_vector = self.query_to_vector(query_tokens)

        if(use_champions == True):
            final_index = self.champion_index

        cosine_sim = self.search_by_cosine(query_vector,final_index,doc_length)

        return cosine_sim



    def read_lines(self, filename):
        """ DO NOT MODIFY.
        Read a gzipped file to a list of strings.
        """
        return [l.strip() for l in gzip.open(filename, 'rt').readlines()]

    def tokenize(self, document):
        """ DO NOT MODIFY.
        Convert a string representing one document into a list of
        words. Retain hyphens and apostrophes inside words. Remove all other
        punctuation and convert to lowercase.

        >>> Index().tokenize("Hi there. What's going on? first-class")
        ['hi', 'there', "what's", 'going', 'on', 'first-class']
        """
        return [t.lower() for t in re.findall(r"\w+(?:[-']\w+)*", document)]


def main():
    """ DO NOT MODIFY.
    Main method. Constructs an Index object and runs a sample query. """
    print("start")
    indexer = Index('documents.txt.gz')
    for query in ['pop love song', 'chinese american', 'city']:
        print('\n\nQUERY=%s' % query)
        print("stage1")
        print('\n'.join(['%d\t%e' % (doc_id, score) for doc_id, score in indexer.search(query)[:10]]))
        print('\n\nQUERY=%s Using Champion List' % query)
        print('\n'.join(['%d\t%e' % (doc_id, score) for doc_id, score in indexer.search(query, True)[:10]]))

if __name__ == '__main__':
    main()
