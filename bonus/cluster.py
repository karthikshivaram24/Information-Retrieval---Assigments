"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter
from collections import ChainMap
import collections
import gzip
import math

import numpy as np


class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k
        self.clusters = collections.defaultdict(list)
        self.clusters_id = collections.defaultdict(list)
        self.means = []
        self.documents = []
        self.vocabulary = set()

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector), rounded to 2 decimal places.
        See Log.txt for expected output.
        The order of operations is:
        1) initialize means
        2) Loop
          2a) compute_clusters
          2b) compute_means
          2c) print sizes and error
        """
        ###TODO
        pass

        initial_means = documents[:self.k]
        self.means = initial_means

        i = 0

        while(i< iters):

            self.clusters = collections.defaultdict(list)
            self.clusters_id = collections.defaultdict(list)
            self.compute_clusters(documents)
            cluster_size = []
            for cluster in self.clusters_id:
                cluster_size.append(len(self.clusters_id[cluster]))
            print(cluster_size)
            self.compute_means(self.clusters)
            print("{0:.2f}".format(self.error(documents)))
            # self.means = []
            i += 1


    def compute_means(self,clusters):
        """ Compute the mean vectors for each cluster (results stored in an
        instance variable of your choosing)."""
        ###TODO
        pass

        list_keys = []

        for cluster in clusters:
            result_map = {}
            list_of_dicts = clusters[cluster]
            for d in list_of_dicts:
                result_map.update(d)
            list_keys.append(result_map.keys())

        self.means =  [{} for _ in range(self.k)]

        for mean in range(self.k):
                for term in list_keys[mean]:
                    term_sum = 0.0
                    for doc in clusters[mean]:
                        if term not in doc:
                            term_sum += 0.0
                        else:
                            term_sum += doc[term]
                    if term_sum == 0.0 :
                        self.means[mean][term] = 0.0
                    else:
                        self.means[mean][term] = term_sum / len(clusters[mean])



    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable of your choosing). """
        ###TODO
        pass
        means_q = self.means
        dist_dic = collections.defaultdict(list)
        for mean in range(len(means_q)):
            self.clusters[mean] = []
        for doc in range(len(documents)):
            for mean in range(len(means_q)):
                mean_norm = self.sqnorm(means_q[mean])
                dist = self.distance(documents[doc],means_q[mean],mean_norm)
                dist_dic[doc].append(dist)
            min_dis = min(dist_dic[doc])
            index = dist_dic[doc].index(min_dis)
            self.clusters[index].append(documents[doc])
            self.clusters_id[index].append(doc)


    def sqnorm(self, d):
        """ Return the vector length of a dictionary d, defined as the sum of
        the squared values in this dict. """
        ###TODO
        pass
        sum = 0.0
        for key in d.keys():

            sum+= d[key] ** 2

        return sum

    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
        ###TODO
        pass
        dot_product = 0.0
        doc_norm = self.sqnorm(doc)


        for i in doc:
            if(i in mean):
                dot_product += doc[i] * mean[i]
            else:
                dot_product += 0.0


        temp = (doc_norm + mean_norm)  - (2 * dot_product)

        if(temp > 0.0):
            result = math.sqrt(temp)
        else:
            result = 0.0

        return result


    def error(self, documents):
        """ Return the error of the current clustering, defined as the total
        Euclidean distance between each document and its assigned mean vector."""
        ###TODO
        pass
        total_sum = 0.0
        for doc in range(len(documents)):

            inner_sum = 0.0

            for mean in range(len(self.means)):

                rij = 0

                if(doc in self.clusters_id[mean]):
                    rij = 1

                mean_temp_norm = self.sqnorm(self.means[mean])

                dis = self.distance(documents[doc],self.means[mean],mean_temp_norm)

                inner_sum += rij * dis

            total_sum += inner_sum

        return total_sum


    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster. These are the
        documents that are the closest to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (sorted alphabetically).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
        ###TODO
        pass

        mean_norms = []

        for i in range(self.k):
            mean_norms.append(self.sqnorm(self.means[i]))


        clusters_dist = collections.defaultdict(list)


        for cluster in self.clusters:
            for doc in self.clusters[cluster]:
                dist = self.distance(doc,self.means[cluster],mean_norms[cluster])
                clusters_dist[cluster].append((doc,dist))


        for cluster in clusters_dist:
            print("Cluster " + str(cluster))
            docs_list_tups = clusters_dist[cluster]
            sorted_list = sorted(docs_list_tups,key=lambda x: x[1],reverse = True)

            j = 0
            while(j < n):
                if(len(sorted_list[j][0]) > 3):
                    values = list(sorted_list[j][0].keys())
                    values.sort()
                    output =  " ".join(value for value in values)
                    print(output)
                    j+= 1


def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    ###TODO
    pass
    temp = {}
    temp_docs = docs.copy()
    for doc in docs:
        for term in doc:
            if(term not in temp ):
                temp[term] = 1
            else:
                temp[term] += 1

    for doc in range(len(docs)) :
        te = temp_docs[doc]
        for term in list(te):
            if(temp[term] < min_df):
                del temp_docs[doc][term]

    counters = []

    for doc in range(len(temp_docs)):
        if len(temp_docs[doc]) > 0:
            counters.append(Counter(temp_docs[doc]))

    return counters


def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with gzip.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles


def main():
    profiles = read_profiles('profiles.txt.gz')
    print('read', len(profiles), 'profiles.')
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()
