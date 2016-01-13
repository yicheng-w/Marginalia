from string import ascii_letters

def get_snippets_from_site(site, to_search):
    """
    get_snippets_from_site: returns the sublist of to_search that appears in
    site

    Args:
        site (string): the haystack
	to_search (list of strings): self-explanatory
    
    Returns:
        a list of strings that is a sublist of to_search that appeared in site,
        ordered by which one appeared first
    
    Example:
        get_snippets_from_site("I am awesome", ["this", "is", "awesome"]) -->
        ['am', 'awesome']
    """

    ret_val = []

    site = site.split()

    for i in to_search:
        if i in site:
            ret_val.append(i)

    return ret_val

def get_index_of_proximity(site, to_search):
    """
    get_index_of_proximity: returns the index of proximity of a specific search,
        the index of proximity is defined as the number of words matched
        divided by the total distance between the matched words. The higher the
        index the better the match

        if only one element of to_search is matched, returns 0??? FIXME

        return -1 if no element is matched

    Args:
        site (string): the site to search in
	to_search (list of strings): the list of string to match
    
    Returns:
        a float, the index of proximity
    """

    total_distance = 0

    indices = []

    site = site.split()

    for i in to_search:
        if i in site:
            indices.append(site.index(i))

    indices.sort()
    
    if (len(indices) == 0):
        return -1

    elif (len(indices) == 1):
        return 0

    else:
        for i in range(1,len(indices)):
            total_distance += indices[i] - indices[i - 1]

        return len(indices) / float(total_distance)

def abstract_site_from_words(text, list_of_words):
    """
    abstract_site_from_words: get an abstraction of the text based on the words

    Args:
        text (string): the text to abstract
	list_of_words (list of strings): the list to abstract
    
    Returns:
        a string that is the abstracted text
    
    Example:
        abstract_site_from_words("blah blah blah blah hello world blah blah
            blah", ['hello']) --> "... blah blah hello world blah ..."
    """

    text = text.split()

    result = ""
    indices = [0]

    for i in list_of_words:
        indices.append(text.index(i))

    indices.append(len(text) - 1)

    indices.sort()

    i = 1
    blockstart = 0

    for i in range(1, len(indices)):
        if indices[i] - indices[i - 1] > 10:
            result += " ".join(text[blockstart : indices[i - 1] + 6]) + '... '
            blockstart = indices[i] - 5

    if indices[-1] - indices[-2] > 6:
        result += " ".join(text[blockstart : indices[-2] + 6]) + "..."

    else:
        result += " ".join(text[blockstart : indices[-1] + 6])

    return result


if __name__ == "__main__":
    f = open('testext.txt', 'r').read()

    snippet = get_snippets_from_site(f, ['this', 'is', 'a', 'pineapple'])

    print "Snippet: " + str(snippet)

    index = get_index_of_proximity(f, ['this', 'is', 'a', 'pineapple'])

    abstracted = abstract_site_from_words(f, snippet)

    print "Abstracted: " + abstracted

    print "Index: " + str(index)

    print str(get_index_of_proximity(f,  ['pineapple', 'fruit', 'furnishings.', 'country.', 'material']))

    print abstract_site_from_words(f, ['pineapple', 'fruit', 'furnishings.', 'country.', 'material'])
