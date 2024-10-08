from process_functions import *

rules = {
    'head_01': {'function': head_01, 'parts': ['headline'], 'ruleDesc': 'Headlines should not exceeed 70 characters', },
    'name_01': {'function': name_01, 'parts': ['headline', 'body'], 'ruleDesc': 'Put periods in honorifics and suffixes, Mr Mrs Dr Jr Sr'},
    'name_02': {'function': name_02, 'parts': ['headline', 'body'], 'ruleDesc': 'Put periods in middle initials'},
    'name_03': {'function': name_03, 'parts': ['headline', 'body'], 'ruleDesc': 'Sr. And Jr. should not have a comma separating it from the surname'},
    'name_04': {'function': name_04, 'parts': ['headline', 'body'], 'ruleDesc': 'Don’t put periods in names like TJ, AJ, JC, etc.'},
    'name_05': {'function': name_05, 'parts': ['headline', 'body'], 'ruleDesc': 'Names with de, dela, de la, del, de los, delos should not be capitalized if the first name is mentioned'},
}

def agg_details(input_content):
    details = []
    for rulename in rules.keys():
        fulltext = ' '.join(input_content[i] for i in rules[rulename]['parts'])
        result = rules[rulename]['function'](fulltext)
        
        details.append({
            'ruleCode': rulename,
            'ruleResult': 'FAIL' if len(result) > 0 else 'PASS',
            'resultDesc': rules[rulename]['ruleDesc'],
            'offendingStrings': result
        })
    return details