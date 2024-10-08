from process_functions import *

rules = {
    'head_01': {'function': head_01, 'parts': ['headline'], 'ruleDesc': 'Headlines should not exceeed 70 characters', },
    'name_01': {'function': name_01, 'parts': ['headline', 'body'], 'ruleDesc': 'Put periods in honorifics and suffixes, Mr Mrs Dr Jr Sr'},
    'name_02': {'function': name_02, 'parts': ['headline', 'body'], 'ruleDesc': 'Put periods in middle initials'},
    'name_03': {'function': name_03, 'parts': ['headline', 'body'], 'ruleDesc': 'Sr. And Jr. should not have a comma separating it from the surname'},
    'name_04': {'function': name_04, 'parts': ['headline', 'body'], 'ruleDesc': 'Don’t put periods in names like TJ, AJ, JC, etc.'},
    'name_05': {'function': name_05, 'parts': ['headline', 'body'], 'ruleDesc': 'Names with de, dela, de la, del, de los, delos should not be capitalized if the first name is mentioned'},
    'position_05': {'function': position_05, 'parts': ['headline', 'body'], 'ruleDesc': 'Use lowercase for opposition senator and opposition lawmaker, whether with a name or not.'},
    'position_09': {'function': position_09, 'parts': ['headline', 'body'], 'ruleDesc': 'There is no hyphen in vice president, vice governor, vice mayor, etc.'},
    'position_10': {'function': position_10, 'parts': ['headline', 'body'], 'ruleDesc': 'Use foreign secretary, not foreign affairs secretary'},
    'position_12': {'function': position_12, 'parts': ['headline', 'body'], 'ruleDesc': 'When using then-(position), there should be a hyphen. Lowercase for the position.'},
    'position_21': {'function': position_21, 'parts': ['headline', 'body'], 'ruleDesc': 'The Pope and the Dalai Lama are always capitalized.'},
    'agency_03': {'function': agency_03, 'parts': ['body'], 'ruleDesc': 'If the full name and the acronym will be used in the same sentence, don’t put the acronym in parentheses next to the first mention.'},
    'agency_05': {'function': agency_05, 'parts': ['body'], 'ruleDesc': 'No need to put the acronyms in parentheses for the United Nations and the European Union.'},
    'agency_09': {'function': agency_09, 'parts': ['body'], 'ruleDesc': 'Senate and House of Representatives should always be capitalized'},
    'agency_12': {'function': agency_12, 'parts': ['body'], 'ruleDesc': 'Use non-government organization, not non-governmental'},
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