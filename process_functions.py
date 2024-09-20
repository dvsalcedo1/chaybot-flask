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

def head_11(text,part):
    """
    Head-11

    Inputs needed: headline
    """
    req = text[part]
    res = { 'ruleCode': 'Head-11', 'ruleResult': '', 'resultDesc': '' }

    wordlist = req.lower().split(" ")
    numbers = ['one','two','three','four','five','six','seven','eight','nine','ten',
               'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen',
               'twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety']
    
    res['ruleResult'] = 'PASS'
    for i in wordlist:
        if i in numbers:
            res['ruleResult'] = 'FAIL'
            res['resultDesc'] = 'Do not spell out numbers in the title. Use numerical digits instead.'
        if i == '0':
            res['ruleResult'] = 'FAIL'
            res['resultDesc'] += ' Spell out \"zero\" instead of using \"0\"'                        

    return res

def head_12(text,part):
    """
    Head-12

    Inputs needed: headline
    """
    req = text[part]
    res = { 'ruleCode': 'Head-12', 'ruleResult': '', 'resultDesc': '' }

    wordlist = req.split(" ")
    colons = [i for i,n in enumerate(wordlist) if ":" in n]
    checkCapitalization = [wordlist[j+1] for j in colons]

    res['ruleResult'] = 'PASS'
    for i in checkCapitalization:
        if i[0].isalpha() and i[0].islower():
            res['ruleResult'] = 'FAIL'
            res['resultDesc'] = 'Capitalize the next word after every colon'

    return res

