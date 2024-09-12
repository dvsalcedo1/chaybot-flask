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