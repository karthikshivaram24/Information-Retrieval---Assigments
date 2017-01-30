""" Assignment 2
"""
import abc
from collections import defaultdict
import math

import index


def idf(term, index):
    """ Compute the inverse document frequency of a term according to the
    index. IDF(T) = log10(N / df_t), where N is the total number of documents
    in the index and df_t is the total number of documents that contain term
    t.

    Params:
      terms....A string representing a term.
      index....A Index object.
    Returns:
      The idf value.

    >>> idx = index.Index(['a b c a', 'c d e', 'c e f'])
    >>> idf('a', idx) # doctest:+ELLIPSIS
    0.477...
    >>> idf('d', idx) # doctest:+ELLIPSIS
    0.477...
    >>> idf('e', idx) # doctest:+ELLIPSIS
    0.176...
    """
    ###TODO
    pass
    df_t = index.doc_freqs
    N = len(index.documents)
    idf = math.log10(N/df_t[term])

    return idf

class ScoringFunction:
    """ An Abstract Base Class for ranking documents by relevance to a
    query. """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def score(self, query_vector, index):
        """
        Do not modify.

        Params:
          query_vector...dict mapping query term to weight.
          index..........Index object.
        """
        return


class RSV(ScoringFunction):
    """
    See lecture notes for definition of RSV.

    idf(a) = log10(3/1)
    idf(d) = log10(3/1)
    idf(e) = log10(3/2)
    >>> idx = index.Index(['a b c', 'c d e', 'c e f'])
    >>> rsv = RSV()
    >>> rsv.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.4771...
    """

    def score(self, query_vector, index):
        ###TODO
        pass
        doc_freq = index.doc_freqs
        n = len(index.documents)
        docs = index.documents

        doc_queryterm ={}

        for doc in docs:
            for term_key in query_vector:
                if term_key in doc:
                    if docs.index(doc) not in doc_queryterm:
                        doc_queryterm[docs.index(doc)] = set([term_key])
                    else:
                        doc_queryterm[docs.index(doc)].add(term_key)

        rsv_scores ={}

        for doc_id in doc_queryterm:
            if doc_id not in rsv_scores:
                rsv_scores[doc_id+1] = 0.0
            sum_idf = 0.0
            for term in doc_queryterm[doc_id]:
                sum_idf += math.log10(n/doc_freq[term])
            rsv_scores[doc_id+1] = sum_idf

        return rsv_scores


    def __repr__(self):
        return 'RSV'


class BM25(ScoringFunction):
    """
    See lecture notes for definition of BM25.

    log10(3) * (2*2) / (1(.5 + .5(4/3.333)) + 2) = log10(3) * 4 / 3.1 = .6156...
    >>> idx = index.Index(['a a b c', 'c d e', 'c e f'])
    >>> bm = BM25(k=1, b=.5)
    >>> bm.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.61564032...
    """
    def __init__(self, k=1, b=.5):
        self.k = k
        self.b = b

    def score(self, query_vector, index):
        ###TODO
        pass
        doc_freq = index.doc_freqs
        n = len(index.documents)
        docs = index.documents
        doc_len,mean = index.doc_lengths,index.mean_doc_length
        #mean = index.mean_doc_length
        tf_index = index.index


        doc_queryterm ={}

        for doc in docs:
            for term_key in query_vector:
                if term_key in doc:
                    if docs.index(doc) not in doc_queryterm:
                        doc_queryterm[docs.index(doc)] = set([term_key])
                    else:
                        doc_queryterm[docs.index(doc)].add(term_key)

        bm25_scores ={}

        for doc_id in doc_queryterm:
            if doc_id not in bm25_scores:
                bm25_scores[doc_id+1] = 0.0
            sum_idf = 0.0
            for term in doc_queryterm[doc_id]:
                #print(doc_len)
                ratio = doc_len[doc_id+1]/mean
                if term in tf_index:
                    lis = tf_index[term]
                    #print(lis)
                    for tup in lis:
                        if tup[0] == doc_id + 1:
                            sum_idf += (math.log10(n/doc_freq[term]) * (((self.k + 1) * tup[1]) / (self.k * ((1-self.b) + (self.b * ratio ) ) + tup[1])))
            bm25_scores[doc_id+1] = sum_idf

        return bm25_scores


    def __repr__(self):
        return 'BM25 k=%d b=%.2f' % (self.k, self.b)


class Cosine(ScoringFunction):
    """
    See lecture notes for definition of Cosine similarity.  Be sure to use the
    precomputed document norms (in index), rather than recomputing them for
    each query.

    >>> idx = index.Index(['a a b c', 'c d e', 'c e f'])
    >>> cos = Cosine()
    >>> cos.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.792857...
    """
    def score(self, query_vector, index):
        ###TODO
        pass
        doc_norm = index.doc_norms
        docs = index.documents
        doc_freq = index.doc_freqs
        in_dex = index.index

        doc_queryterm ={}

        for doc in docs:
           # print(doc)
            for query_term in query_vector:
                if query_term in doc:
                    #print(query_term)
                    if docs.index(doc) not in doc_queryterm:
                        #print(set([query_term]))
                        doc_queryterm[docs.index(doc)] = set([query_term])
                    else:
                        doc_queryterm[docs.index(doc)].add(query_term)
                #else:
                    #doc_queryterm[docs.index(doc)] = set()

        cosine_scores ={}

       #print(query_vector)
       #print(doc_queryterm)


        for doc in doc_queryterm:
            if(len(doc_queryterm[doc]) > 0):
                sum_numerator = 0.0
                for term in doc_queryterm[doc]:
                    for tup in in_dex[term]:
                        #print(tup,doc)
                        if tup[0] == doc + 1:
                            tf = tup[1]
                            df = doc_freq[term]
                            tf_idf = ((1 + math.log10(tf)) * math.log10(len(docs)/df))
                            numerator = tf_idf * query_vector[term]
                            sum_numerator += numerator
                            #cosine = numerator / doc_norm[doc+1]

                cosine = sum_numerator / doc_norm[doc+1]
                cosine_scores[doc + 1] = cosine
            elif (len(doc_queryterm[doc]) == 0):
                cosine_scores[doc+1] = 0.0

        return cosine_scores




    def __repr__(self):
        return 'Cosine'
