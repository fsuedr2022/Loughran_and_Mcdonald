def convertStrListtoIntList(str_list):
    '''
    Converts the items in a list from a string to an integer
    :param str_list: list of strings
    :return: List of integers
    '''
    int_list = []
    for item in str_list:
        int_list.append(int(item))
    return int_list

def splitEDGARHeader(edgar_header, header_key):
    '''
    splits the edgar header
    :param edgar_header: edgar header value
    :return: list of edgar header values
    '''
    a = edgar_header.get(header_key, -99)
    return a.split('|')
