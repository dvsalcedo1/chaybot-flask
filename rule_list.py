from process_functions import *

rules = {
    'head_01': {'ruleDesc': 'Headlines should not exceeed 70 characters', 'function': head_01, 'parts': ['headline']}
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