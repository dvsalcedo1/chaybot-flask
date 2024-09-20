from nltk.tag import pos_tag
# General format
def rule_code(text,part):
    """
    Rule Description

    Inputs needed: [url, headline, subhead, body,...]
    """
    req = text[part]
    res = { 'ruleCode': 'Rule Code', 'ruleResult': '', 'resultDesc': '' }

    if req: #condition to pass
        res['ruleResult'] = 'PASS'
    else: #condition to fail
        res['ruleResult'] = 'FAIL'
        res['resultDesc'] = 'Some explanation why'

    return res        



def head_01(text,part):
    """
    Head-01: Headlines should not exceeed 70 characters

    Inputs needed: headline 
    """
    req = text[part]
    res = { 'ruleCode': 'Head-01', 'ruleResult': '', 'resultDesc': '' }

    if len(req) < 70:
        res['ruleResult'] = 'PASS'
    else:
        res['ruleResult'] = 'FAIL'
        res['resultDesc'] = 'Headlines should not exceeed 70 characters'

    return res

def head_06(text,part):
    """
    Head-06: Headlines should not have long words

    Inputs needed: headline
    """
    req = text[part]
    res = { 'ruleCode': 'Head-06', 'ruleResult': '', 'resultDesc': '' }

    wordlist = req.split(' ')

    res['ruleResult'] = 'PASS'
    for i in wordlist:
        if len(i) > 10:
            res['ruleResult'] = 'FAIL'
            res['resultDesc'] = 'One of the words in the headline is too long'

    return res

def head_09(text,part):
    """
    Head-09

    Inputs needed: headline
    """
    req = text[part]
    res = { 'ruleCode': 'Head-09', 'ruleResult': '', 'resultDesc': '' }

    res['ruleResult'] = 'PASS'
    for i in req:
        if i == "\"":
            res['ruleResult'] = 'FAIL'
            res['resultDesc'] = 'Use single quotes and not double quotes'

    return res

def head_10(text,part):
    """
    Head-10

    Inputs needed: headline
    """
    req = text[part]
    res = { 'ruleCode': 'Head-10', 'ruleResult': '', 'resultDesc': '' }

    wordlist = req.split(" ")
    colons = [i for i,n in enumerate(wordlist) if ":" in n]
    hyphens = [i for i,n in enumerate(wordlist) if "-" in n]
    checkNames = pos_tag([wordlist[j+1] for j in colons+hyphens])

    res['ruleResult'] = 'PASS'
    for i in checkNames:
        if i[1] == 'NNP':
            res['ruleResult'] = 'FAIL'
            res['resultDesc'] = 'Use an en-dash and not a hyphen or double quote when indicating a source'

    return res



