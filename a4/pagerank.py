""" Assignment 6: PageRank. """
from bs4 import BeautifulSoup
from sortedcontainers import SortedList, SortedSet, SortedDict
from collections import Counter
from collections import defaultdict
import glob
import os
import re


def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    """ Return a dictionary mapping each url to its PageRank.
    The formula is R(u) = (1/N)(1-b) + b * (sum_{w in B_u} R(w) / (|F_w|)

    Initialize all scores to 1.0.

    Params:
      urls.......SortedList of urls (names)
      inlinks....SortedDict mapping url to list of in links (backlinks)
      outlinks...Sorteddict mapping url to list of outlinks
    Returns:
      A SortedDict mapping url to its final PageRank value (float)

    >>> urls = SortedList(['a', 'b', 'c'])
    >>> inlinks = SortedDict({'a': ['c'], 'b': set(['a']), 'c': set(['a', 'b'])})
    >>> outlinks = SortedDict({'a': ['b', 'c'], 'b': set(['c']), 'c': set(['a'])})
    >>> sorted(compute_pagerank(urls, inlinks, outlinks, b=.5, iters=0).items())
    [('a', 1.0), ('b', 1.0), ('c', 1.0)]
    >>> iter1 = compute_pagerank(urls, inlinks, outlinks, b=.5, iters=1)
    >>> iter1['a']  # doctest:+ELLIPSIS
    0.6666...
    >>> iter1['b']  # doctest:+ELLIPSIS
    0.333...
    """
    ###TODO
    pass

    pagerank = defaultdict.fromkeys(urls,1.0)
    # print(pagerank)

    for iter in range(iters):
        for url in urls:
            sum_temp = 0.0
            for cs in inlinks[url]:
                length = len(outlinks[cs])
                sum_temp += pagerank[cs]/length

            pagerank[url] = (1.0 - b)*(1.0/len(urls)) + (b*sum_temp)

    return pagerank


def get_top_pageranks(inlinks, outlinks, b, n=50, iters=20):
    """
    >>> inlinks = SortedDict({'a': ['c'], 'b': set(['a']), 'c': set(['a', 'b'])})
    >>> outlinks = SortedDict({'a': ['b', 'c'], 'b': set(['c']), 'c': set(['a'])})
    >>> res = get_top_pageranks(inlinks, outlinks, b=.5, n=2, iters=1)
    >>> len(res)
    2
    >>> res[0]  # doctest:+ELLIPSIS
    ('a', 0.6666...
    """
    ###TODO
    pass
    urls = inlinks.keys()
    pageranks = compute_pagerank(urls,inlinks,outlinks,b,iters)

    result = sorted(pageranks.items(), key=lambda x: x[1],reverse = True)

    return result[:n]




def read_names(path):
    """ Do not mofify. Returns a SortedSet of names in the data directory. """
    return SortedSet([os.path.basename(n) for n in glob.glob(path + os.sep + '*')])


def get_links(names, html):
    """
    Return a SortedSet of computer scientist names that are linked from this
    html page. The return set is restricted to those people in the provided
    set of names.  The returned list should contain no duplicates.

    Params:
      names....A SortedSet of computer scientist names, one per filename.
      html.....A string representing one html page.
    Returns:
      A SortedSet of names of linked computer scientists on this html page, restricted to
      elements of the set of provided names.

    >>> get_links({'Gerald_Jay_Sussman'},
    ... '''<a href="/wiki/Gerald_Jay_Sussman">xx</a> and <a href="/wiki/Not_Me">xx</a>''')
    SortedSet(['Gerald_Jay_Sussman'], key=None, load=1000)
    """
    ###TODO
    pass

    name_links = set()

    hrefs = re.findall('<a href="?\'?([^"\'>]*)', html)

    name_list = set()

    for href in hrefs:
        replaced_string = href.replace("/wiki/","")
        name_list.add(replaced_string)

    for name in names:
        if name in name_list:
            name_links.add(name)


    return SortedSet(name_links)



def read_links(path):
    """
    Read the html pages in the data folder. Create and return two SortedDicts:
      inlinks: maps from a name to a SortedSet of names that link to it.
      outlinks: maps from a name to a SortedSet of names that it links to.
    For example:
    inlinks['Ada_Lovelace'] = SortedSet(['Charles_Babbage', 'David_Gelernter'], key=None, load=1000)
    outlinks['Ada_Lovelace'] = SortedSet(['Alan_Turing', 'Charles_Babbage'], key=None, load=1000)

    You should use the read_names and get_links function above.

    Params:
      path...the name of the data directory ('data')
    Returns:
      A (inlinks, outlinks) tuple, as defined above (i.e., two SortedDicts)
    """
    ###TODO
    pass
    data = {}
    in_links = SortedDict()
    out_links = SortedDict()
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as my_file:
                data[dir_entry] = my_file.read()


    names = read_names(path)

    for name in names :
        in_links[name] = SortedSet()
        out_links[name] = SortedSet()

    for name in names:
        temp_set = get_links(names,data[name])
        if name in temp_set:
            temp_set.remove(name)
        out_links[name] = temp_set

    for key,values in out_links.items():
        for value in values:
            in_links[value].add(key)

    return(in_links,out_links)

def print_top_pageranks(topn):
    """ Do not modify. Print a list of name/pagerank tuples. """
    print('Top page ranks:\n%s' % ('\n'.join('%s\t%.5f' % (u, v) for u, v in topn)))


def main():
    """ Do not modify. """
    if not os.path.exists('data'):  # download and unzip data
       from urllib.request import urlretrieve
       import tarfile
       urlretrieve('http://cs.iit.edu/~culotta/cs429/pagerank.tgz', 'pagerank.tgz')
       tar = tarfile.open('pagerank.tgz')
       tar.extractall()
       tar.close()

    inlinks, outlinks = read_links('data')
    print('read %d people with a total of %d inlinks' % (len(inlinks), sum(len(v) for v in inlinks.values())))
    print('read %d people with a total of %d outlinks' % (len(outlinks), sum(len(v) for v in outlinks.values())))
    topn = get_top_pageranks(inlinks, outlinks, b=.8, n=20, iters=10)
    print_top_pageranks(topn)


if __name__ == '__main__':
    main()
