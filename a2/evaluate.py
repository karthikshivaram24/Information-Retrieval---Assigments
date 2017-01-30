""" Assignment 2
"""
import abc

import numpy as np


class EvaluatorFunction:
    """
    An Abstract Base Class for evaluating search results.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, hits, relevant):
        """
        Do not modify.
        Params:
          hits...A list of document ids returned by the search engine, sorted
                 in descending order of relevance.
          relevant...A list of document ids that are known to be
                     relevant. Order is insignificant.
        Returns:
          A float indicating the quality of the search results, higher is better.
        """
        return


class Precision(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute precision.

        >>> Precision().evaluate([1, 2, 3, 4], [2, 4])
        0.5
        """
        ###TODO
        pass
        true_positives = len(set(hits).intersection(relevant))
        precision = (true_positives) / len(hits)

        #print(precision)
        return precision

    def __repr__(self):
        return 'Precision'


class Recall(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute recall.

        >>> Recall().evaluate([1, 2, 3, 4], [2, 5])
        0.5
        """
        ###TODO
        pass
        true_positives = len(set(hits).intersection(relevant))

        recall = (true_positives) / len(relevant)
        #print("recall " + str(recall))
        return recall

    def __repr__(self):
        return 'Recall'


class F1(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute F1.

        >>> F1().evaluate([1, 2, 3, 4], [2, 5])  # doctest:+ELLIPSIS
        0.333...
        """
        ###TODO
        pass
        precision = Precision()

        recall = Recall()

        prec = precision.evaluate(hits,relevant)

        rec = recall.evaluate(hits,relevant)

        f_measure = 0.0

        if prec + rec > 0:
            f_measure = (2.0 * prec * rec) / (prec + rec)

        return f_measure

    def __repr__(self):
        return 'F1'


class MAP(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute Mean Average Precision.

        >>> MAP().evaluate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 4, 6, 11, 12, 13, 14, 15, 16, 17])
        0.2
        """
        ###TODO
        pass

        precision = Precision()

        temp_dictionary = {} # To help calculate relevant precission measure

        for i in hits:
            if i in relevant:
                temp_dictionary[i] = "Y"
            else :
                temp_dictionary[i] = "N"

        prec_forrelandretrieved = [] # this list shall contain all the precission scores for doc ids that are in hit and relevant

        for i in hits:
            prec = precision.evaluate(hits[:i],relevant)
            if temp_dictionary[i] == "Y":
                prec_forrelandretrieved.append(prec)

        sum_prec = 0.0

        for j in prec_forrelandretrieved:
            sum_prec += j

        mAp = sum_prec / len(relevant)

        return mAp
    def __repr__(self):
        return 'MAP'

