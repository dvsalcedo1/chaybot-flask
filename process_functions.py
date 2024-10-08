from helpers import get_context
from nltk.tag import pos_tag
import spacy
import re

nlp = spacy.load('en_core_web_lg')

### Headline
def head_01(text):
    '''Headlines should not exceeed 70 characters'''
    if len(text) > 70:
        return [text]
    else:
        return []

def head_06(text,part):
    """
    Head-06: Headlines should not have long words

    Inputs needed: headline
    """
    req = text[part]
    res = { 'ruleCode': 'Head-06', 'ruleResult': '', 'resultDesc': '' }

    # wordlist = req.split(' ')

    # res['ruleResult'] = 'PASS'
    # for i in wordlist:
    #     if len(i) > 10:
    #         res['ruleResult'] = 'FAIL'
    #         res['resultDesc'] = 'One of the words in the headline is too long'

    return res

def head_09(text,part):
    """
    Head-09: Headlines should have single quotes and not double quotes

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
    Head-10: Headlines should use en dash and not hyphen or colon when indicating source

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
    Head-11: Headlines should use digits and not spelled out numbers except for zero

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
    Head-12: Headline word after colon should be capitalized

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

### Subhead
def subhead_01(text,part):
    """
    Subhead-01: Subhead should not exceed 200 characters

    Inputs needed: subhead 
    """
    req = text[part]
    res = { 'ruleCode': 'Subhead-01', 'ruleResult': '', 'resultDesc': '' }

    if len(req) < 200:
        res['ruleResult'] = 'PASS'
    else:
        res['ruleResult'] = 'FAIL'
        res['resultDesc'] = 'Subhead should not exceed 200 characters'

    return res

def subhead_06(text,part):
    """
    Subhead-06: Subhead should have single quotes and not double quotes

    Inputs needed: subhead
    """
    req = text[part]
    res = { 'ruleCode': 'Subhead-06', 'ruleResult': '', 'resultDesc': '' }

    res['ruleResult'] = 'PASS'
    for i in req:
        if i == "\"":
            res['ruleResult'] = 'FAIL'
            res['resultDesc'] = 'Subhead should have single quotes and not double quotes'

### Dateline
def dateline_03(text,part):
    """
    Metro Manila dateline should use MANILA, PHILIPPINES

    Inputs needed: body
    """
    req = text[part]
    res = { 'ruleCode': 'Dateline-03', 'ruleResult': '', 'resultDesc': '' }

    dateline = ""
    res['ruleResult'] = 'PASS'
    if ("—" in req):
        dateline = req.split("—")[0][:-1]
        if len(dateline) < 100:
            if "metro manila" in dateline.lower():
                res['ruleResult'] = 'FAIL'
                res['resultDesc'] = 'Metro Manila dateline should use MANILA, PHILIPPINES'
        else:
            res['resultDesc'] = 'There was no dateline detected' 
    else:
        res['resultDesc'] = 'There was no dateline detected' # return pass if there is no dateline

    return res

### URL
def url_01(text,part):
    """
    URLs should have 11 words max

    Inputs needed: body
    """
    req = text[part]
    res = { 'ruleCode': 'Url-01', 'ruleResult': '', 'resultDesc': '' }

    url = req.split("/")[-2]
    res['ruleResult'] = 'PASS'
    if len(url.split("-")) > 11:
        res['ruleResult'] = 'FAIL'
        res['resultDesc'] = 'URLs should have 11 words max'

    return res

def url_04(text,part):
    """
    URLs should not have punctuations

    Inputs needed: body
    """
    req = text[part]
    res = { 'ruleCode': 'Url-04', 'ruleResult': '', 'resultDesc': '' }

    url = req.split("/")[-2]
    res['ruleResult'] = 'PASS'
    for i in url.split("-"):
        if not i.isalnum():
            res['ruleResult'] = 'FAIL'
            res['resultDesc'] = 'URLs should not have punctuations'

    return res

def url_06(text,part):
    """
    URLs should not begin with a number

    Inputs needed: body
    """
    req = text[part]
    res = { 'ruleCode': 'Url-06', 'ruleResult': '', 'resultDesc': '' }

    url = req.split("/")[-2]
    res['ruleResult'] = 'PASS'
    if url.split("-")[0].isdigit():
        res['ruleResult'] = 'FAIL'
        res['resultDesc'] = 'URLs should not begin with a number'

    return res

## Name
def name_01(text, **kwargs):
  '''Put periods in common honorifics and suffixes'''
  honorifics = ['Mr', 'Mrs', 'Dr', 'Ms', 'Prof', 'Mx']
  suffixes = ['Jr', 'Sr']

  offending_strings = []
  honorifics_pattern = r'\b(' + '|'.join(honorifics) + r')\b(?!\.)'
  suffix_pattern = r'\b(' + '|'.join(suffixes) + r')\b(?!\.)'

  # Combine patterns into one for efficiency
  combined_pattern = f'({honorifics_pattern})|({suffix_pattern})'

  # Find all potential matches
  matches = list(re.finditer(combined_pattern, text))

  contexts = []
  for match in matches:
      start, end = match.start(), match.end()
      offending_strings.append(get_context(text, start, end, **kwargs))
  return offending_strings

def name_02(text, **kwargs):
  '''Put periods in middle initials'''
  offending_strings = []
  middle_initial_pattern = r'[A-Z][a-z]+\s([A-Z])\s(?!\.)[A-Z][a-z]'
  # Find all potential matches
  matches = list(re.finditer(middle_initial_pattern, text))

  contexts = []
  for match in matches:
      start, end = match.start(), match.end()
      context = get_context(text, start, end, **kwargs)

      # Run NER on the context
      doc = nlp(context)

      # Check if there is a proper noun (PERSON entity) in the context
      has_proper_noun = any(ent.label_ == 'PERSON' and match.group(0) in ent.text for ent in doc.ents)

      if has_proper_noun:
          contexts.append(context)
  return contexts

def name_03(text, **kwargs):
    '''Sr. And Jr. should not have a comma separating it from the surname'''
    offending_strings = []
    pattern = r'\b\w+,\s+(Jr\.|Sr\.)\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def name_04(text, **kwargs):
    '''Don’t put periods in names like TJ, AJ, JC, etc.'''
    offending_strings = []
    pattern = r'\b([A-Z])\.([A-Z])\.\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def name_05(text, **kwargs):
    '''Names with de, dela, de la, del, de los, delos should not be capitalized if the first name is mentioned'''
    offending_strings = []
    particles = ['De', 'Dela', 'De la', 'Del', 'De los', 'Delos']
    pattern = r'\b[A-Z][a-z]+\s+(' + '|'.join(particles) + r')\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

## Position
def position_05(text, **kwargs):
    '''Use lowercase for opposition senator and opposition lawmaker, whether with a name or not.'''
    offending_strings = []
    pattern = r'\bOpposition\s+(Senator|Lawmaker)\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def position_09(text, **kwargs):
    '''There is no hyphen in vice president, vice governor, vice mayor, etc.'''
    offending_strings = []
    positions = ['president', 'governor', 'mayor']
    pattern = r'\bvice-(' + '|'.join(positions) + r')\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def position_10(text, **kwargs):
    '''Use foreign secretary, not foreign affairs secretary'''
    offending_strings = []
    pattern = r'\bforeign affairs secretary\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def position_12(text, **kwargs):
    '''When using then-(position), there should be a hyphen. Lowercase for the position.'''
    offending_strings = []
    positions = ['president', 'governor', 'mayor', 'senator', 'secretary', 'minister', 'prime minister', 'chancellor', 'ambassador', 'congressman', 'congresswoman', 'representative']
    pattern_no_hyphen = r'\bthen\s+(' + '|'.join(positions) + r')\b'
    matches_no_hyphen = list(re.finditer(pattern_no_hyphen, text, re.IGNORECASE))
    for match in matches_no_hyphen:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    pattern_capital_position = r'\bthen-(' + '|'.join([p.capitalize() for p in positions]) + r')\b'
    matches_capital = list(re.finditer(pattern_capital_position, text))
    for match in matches_capital:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def position_21(text, **kwargs):
    '''The Pope and the Dalai Lama are always capitalized.'''
    offending_strings = []
    pattern = r'\b(pope|dalai lama)\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        matched_text = match.group(0)
        if matched_text.islower():
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

## Agency
def agency_03(text, context_unit='sentences', context_size=1):
    '''If the full name and the acronym will be used in the same sentence, don’t put the acronym in parentheses next to the first mention.'''
    offending_strings = []
    pattern = r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)+)\s+\(([A-Z]{2,})\)'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, context_unit='sentences', context_size=1))
    return offending_strings

def agency_05(text, **kwargs):
    '''No need to put the acronyms in parentheses for the United Nations and the European Union.'''
    offending_strings = []
    pattern = r'\b(United Nations|European Union)\s+\((UN|EU)\)'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def agency_09(text, **kwargs):
    '''Senate and House of Representatives should always be capitalized'''
    offending_strings = []
    pattern = r'\b(senate|house of representatives)\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        if match.group(0).islower():
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def agency_12(text, **kwargs):
    '''Use non-government organization, not non-governmental'''
    offending_strings = []
    pattern = r'\bnon-governmental organization\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

## Place
# def place_02(text, **kwargs):
#     '''URL should not contain CamSur or Gensan, it should be completely spelled out in the slug. They are acceptable everywhere else'''
#     offending_strings = []
#     pattern = r'https?://[^\s]+'
#     matches = list(re.finditer(pattern, text))
#     for match in matches:
#         url = match.group(0)
#         if 'CamSur' in url or 'Gensan' in url:
#             start, end = match.start(), match.end()
#             offending_strings.append(get_context(text, start, end, **kwargs))
#     return offending_strings

def place_06(text, **kwargs):
    '''Spell out st., rd., ave., and blvd (street, avenue, road, boulevard)'''
    offending_strings = []
    abbreviations = ['st\.', 'rd\.', 'ave\.', 'blvd\.']
    pattern = r'\b(' + '|'.join(abbreviations) + r')\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

## Dates
def dates_01(text, **kwargs):
    '''Spell out days and months'''
    offending_strings = []
    abbreviations = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
                     'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug',
                     'Sep', 'Oct', 'Nov', 'Dec']
    pattern = r'\b(' + '|'.join(abbreviations) + r')\.?\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        if match.group(0) in abbreviations:
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_02(text, **kwargs):
    '''Day format on first mention: day of week, comma, month & Day'''
    offending_strings = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    day_pattern = r'\b(' + '|'.join(days) + r')\b'
    month_pattern = r'\b(' + '|'.join(months) + r')\b'
    correct_pattern = day_pattern + r',\s+' + month_pattern + r'\s+\d{1,2}\b'
    incorrect_pattern = day_pattern + r'\s+' + month_pattern + r'\s+\d{1,2}\b'
    matches = list(re.finditer(incorrect_pattern, text))
    for match in matches:
        if not re.match(correct_pattern, match.group(0)):
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_03(text, **kwargs):
    '''Never use yesterday, today, tomorrow, last week, last month, last year, next week, next month, next year'''
    offending_strings = []
    phrases = ['yesterday', 'today', 'tomorrow', 'last week', 'last month',
               'last year', 'next week', 'next month', 'next year']
    pattern = r'\b(' + '|'.join(phrases) + r')\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_04(text, **kwargs):
    '''Date format is Month Day, Year'''
    offending_strings = []
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    month_pattern = r'\b(' + '|'.join(months) + r')\b'
    correct_pattern = month_pattern + r'\s+\d{1,2},\s+\d{4}'
    incorrect_pattern = month_pattern + r'\s+\d{1,2}\s+\d{4}'
    matches = list(re.finditer(incorrect_pattern, text))
    for match in matches:
        if not re.match(correct_pattern, match.group(0)):
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_05(text, **kwargs):
    '''Use "in month year"'''
    offending_strings = []
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    month_pattern = r'\b(' + '|'.join(months) + r')\b'
    pattern = r'(?<!\bin\s)(' + month_pattern + r'\s+\d{4})\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(1), match.end(1)
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_06(text, **kwargs):
    '''When referring to decades, use yyyy-s'''
    offending_strings = []
    pattern = r'\b(\d{2}\'?s|\d{4}\'?s)\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        decade = match.group(0)
        if not re.match(r'\d{4}s', decade):
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_07(text, **kwargs):
    '''nth year anniversary is wrong'''
    offending_strings = []
    pattern = r'\b\d+(st|nd|rd|th)?\s+year anniversary\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_08(text, **kwargs):
    '''for am/pm, don't use periods'''
    offending_strings = []
    pattern = r'\b\d{1,2}(:\d{2})?\s*(a\.m\.|p\.m\.)\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_09(text, **kwargs):
    '''If at top of the hour, no need to use :00'''
    offending_strings = []
    pattern = r'\b\d{1,2}:00\s*(am|pm)\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def dates_10(text, **kwargs):
    '''don't include 12 if using noon or midnight'''
    offending_strings = []
    pattern = r'\b12\s+(noon|midnight)\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

## Numbers
def numbers_01(text, **kwargs):
    '''The general rule for exact numbers is to spell out zero to nine and use digits for 10 onwards'''
    offending_strings = []

    # Find numbers less than 10 written as digits (should be spelled out)
    pattern_digits = r'\b[0-9]\b'
    matches_digits = list(re.finditer(pattern_digits, text))

    # Find numbers 10 and above written as words (should be in digits)
    numbers_10_19 = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
                     'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    scales = ['hundred', 'thousand', 'million', 'billion', 'trillion']
    number_words = numbers_10_19 + tens + scales
    pattern_words = r'\b(' + '|'.join(number_words) + r')\b'
    matches_words = list(re.finditer(pattern_words, text, re.IGNORECASE))

    # Combine all matches
    matches = matches_digits + matches_words

    for match in matches:
        start, end = match.start(), match.end()
        context = get_context(text, start, end, **kwargs)
        context_start = start - (start - context.find(match.group(0)))

        # Run spaCy NLP on the context
        doc = nlp(context)

        # Find the token in the doc that matches the offending string
        match_in_context_start = start - (start - context_start)
        token = None
        for t in doc:
            if t.idx == match_in_context_start:
                token = t
                break
        if not token:
            continue  # Skip if token not found

        # Exclude false positives
        # Exclude dates and times
        if token.ent_type_ in ['DATE', 'TIME']:
            continue
        # Exclude ages (e.g., '26 year old', '5-year-old')
        next_tokens = doc[token.i+1:token.i+3] if token.i+1 < len(doc) else []
        next_text = ' '.join([t.text for t in next_tokens])
        if re.match(r'(year|years)(-| )old', next_text):
            continue
        # Exclude ordinals (e.g., '26th anniversary')
        if token.text.lower().endswith(('st', 'nd', 'rd', 'th')):
            continue
        # Exclude measurements (e.g., '5 km', '10 km/h')
        next_token = doc[token.i+1] if token.i+1 < len(doc) else None
        if next_token and next_token.ent_type_ == 'QUANTITY':
            continue
        if next_token and next_token.text.lower() in ['km', 'km/h', 'kg', 'm', 'cm', 'mph', '°c', '°f']:
            continue
        # Exclude 'a million', 'one million'
        prev_token = doc[token.i-1] if token.i > 0 else None
        if prev_token and prev_token.text.lower() in ['a', 'one'] and token.text.lower() in scales:
            continue
        # Exclude if part of a larger number phrase (e.g., 'twenty million', 'one hundred')
        if (prev_token and prev_token.like_num) or (next_token and next_token.like_num):
            continue
        # Exclude if the token is part of a date format (e.g., 'January 3, 2000')
        if token.ent_type_ == 'CARDINAL' and any(ent.label_ == 'DATE' for ent in doc.ents if token in ent):
            continue

        # If none of the exclusions apply, add to offending strings
        offending_strings.append(context)
    return offending_strings

def numbers_02(text, **kwargs):
    '''When describing age, use the format x-year-old but only if it is an adjective'''
    offending_strings = []
    pattern = r'\b(\d+)\s+year\s+old\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        # Check if 'year old' is used as an adjective
        doc = nlp(text[match.start():match.end()])
        if any(tok.dep_ == 'amod' for tok in doc):
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_03(text, **kwargs):
    '''If using digits in a phrase, use only digits and not spelled out numbers'''
    offending_strings = []
    pattern = r'\b(\d+)\s+([A-Za-z]+)\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        num_word = match.group(2)
        if num_word.lower() in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']:
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_04(text, **kwargs):
    '''If a sentence begins with a number, spell it out, unless it is a year'''
    offending_strings = []
    sentences = list(nlp(text).sents)
    for sent in sentences:
        first_token = sent[0]
        if first_token.like_num and len(first_token.text) > 2:
            continue  # Likely a year
        elif first_token.text.isdigit():
            start, end = first_token.idx, first_token.idx + len(first_token)
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_05(text, **kwargs):
    '''When describing number ranges, use "to" and not hyphen'''
    offending_strings = []
    pattern = r'\b\d+\s*-\s*\d+\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_06(text, **kwargs):
    '''Spell out first to ninth unless it is describing a congressional district, court, division, or military unit'''
    offending_strings = []
    ordinals = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th']
    pattern = r'\b(' + '|'.join(ordinals) + r')\b'
    exclusions = ['district', 'court', 'division', 'unit']
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        end = match.end()
        following_text = text[end:end+20].lower()
        if not any(word in following_text for word in exclusions):
            start = match.start()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_07(text, **kwargs):
    '''For top <number>, the word top is lowercase.'''
    offending_strings = []
    pattern = r'\bTop\s+\d+\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.start()+3
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_08(text, **kwargs):
    '''Using No. X should always be capitalized'''
    offending_strings = []
    pattern = r'\bno\.\s*\d+\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        if match.group(0).startswith('no.'):
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_09(text, **kwargs):
    '''Never use XX-k to refer to thousands'''
    offending_strings = []
    pattern = r'\b\d{1,2}k\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_10(text, **kwargs):
    '''Use % and not percent, also separated by a space'''
    offending_strings = []
    pattern = r'\b\d+(\.\d+)?\s*percent\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    # Check for missing space before %
    pattern_no_space = r'\b\d+(\.\d+)?%(?!\S)'
    matches_no_space = list(re.finditer(pattern_no_space, text))
    for match in matches_no_space:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_11(text, **kwargs):
    '''No need for .0 in percentages'''
    offending_strings = []
    pattern = r'\b\d+\.0\s*%\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_12(text, **kwargs):
    '''Spell out fractions'''
    offending_strings = []
    pattern = r'\b\d+/\d+\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        fraction = match.group(0)
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_13(text, **kwargs):
    '''Use P instead of Php, without space, $ and not USD'''
    offending_strings = []
    pattern_php = r'\bPhp\s*\d+(\.\d+)?\b'
    matches_php = list(re.finditer(pattern_php, text, re.IGNORECASE))
    for match in matches_php:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    pattern_usd = r'\bUSD\s*\d+(\.\d+)?\b'
    matches_usd = list(re.finditer(pattern_usd, text, re.IGNORECASE))
    for match in matches_usd:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_14(text, **kwargs):
    '''multimillion, multibillion has no hyphen'''
    offending_strings = []
    pattern = r'\bmulti-(million|billion)\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_15(text, **kwargs):
    '''Use km/h not kph'''
    offending_strings = []
    pattern = r'\bkph\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_16(text, **kwargs):
    '''Use kWh not kwh'''
    offending_strings = []
    pattern = r'\bkwh\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        if match.group(0) == 'kwh':
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_17(text, **kwargs):
    '''For internet speeds, put a space between the number and the unit of measurement'''
    offending_strings = []
    units = ['Mbps', 'Gbps', 'Kbps']
    pattern = r'\b\d+(Mbps|Gbps|Kbps)\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_18(text, **kwargs):
    '''For temperatures, go straight to °C and °F.'''
    offending_strings = []
    pattern = r'\b\d+\s*(degrees?\s*(Celsius|Fahrenheit)|°\s*[CF])\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        if '°' not in match.group(0):
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def numbers_19(text, **kwargs):
    '''Use Roman numerals for World War I and World War II.'''
    offending_strings = []
    pattern = r'\bWorld War\s+(1|2|One|Two)\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        numeral = match.group(1)
        if numeral.lower() in ['1', 'one', '2', 'two']:
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

## Grammar
def grammar_01(text, **kwargs):
    '''Use "results in", not "results to"'''
    offending_strings = []
    pattern = r'\bresults\s+to\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def grammar_02(text, **kwargs):
    '''Don't use "for" after seek/sought'''
    offending_strings = []
    pattern = r'\b(seek|sought)\s+for\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def grammar_03(text, **kwargs):
    '''Don't use "as" after called/dubbed'''
    offending_strings = []
    pattern = r'\b(called|dubbed)\s+as\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def grammar_04(text, **kwargs):
    '''"On the other hand" should have "on the one hand" in the same paragraph'''
    offending_strings = []
    paragraphs = text.split('\n\n')
    for para in paragraphs:
        if re.search(r'\bon the other hand\b', para, re.IGNORECASE):
            if not re.search(r'\bon the one hand\b', para, re.IGNORECASE):
                match = re.search(r'\bon the other hand\b', para, re.IGNORECASE)
                start = text.find(para) + match.start()
                end = start + len(match.group(0))
                offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

## Punctuation
def punctuation_01(text, **kwargs):
    '''Use the Oxford or serial comma'''
    offending_strings = []
    pattern = r'(\b\w+\b,\s+\b\w+\b\s+and\s+\b\w+\b)'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        if ',' not in match.group(1).rsplit(',', 1)[-1]:
            start, end = match.start(1), match.end(1)
            offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def punctuation_02(text, **kwargs):
    '''Capitalization after a colon'''
    offending_strings = []
    pattern = r':\s+[A-Z]'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        # Check if previous word is not a proper noun
        prev_char = text[match.start()-1]
        if prev_char != '.':
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start+2, end, **kwargs))
    return offending_strings

def punctuation_03(text, **kwargs):
    '''Use en dash (–) with spaces, not em dash (—)'''
    offending_strings = []
    pattern = r'\s*—\s*'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    # Also check for en dash without spaces
    pattern_no_space = r'\S–\S'
    matches_no_space = list(re.finditer(pattern_no_space, text))
    for match in matches_no_space:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def punctuation_04(text, **kwargs):
    '''When words end with s, use just an apostrophe for the possessive form'''
    offending_strings = []
    pattern = r'\b\w+s\'s\b'
    matches = list(re.finditer(pattern, text))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

## Politicolegal
def politicolegal_01(text, **kwargs):
    '''It’s charged with, not charged of'''
    offending_strings = []
    pattern = r'\bcharged\s+of\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def politicolegal_02(text, **kwargs):
    '''It’s indicted for, not indicted of'''
    offending_strings = []
    pattern = r'\bindicted\s+of\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def politicolegal_03(text, **kwargs):
    '''It’s plead guilty to, not plead guilty of'''
    offending_strings = []
    pattern = r'\bplead(ed)?\s+guilty\s+of\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def politicolegal_04(text, **kwargs):
    '''It’s convicted of and acquitted of, not for'''
    offending_strings = []
    pattern = r'\b(convicted|acquitted)\s+for\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

# rules = {
#   # 'place_02': {'ruleDesc': 'URL should not contain CamSur or Gensan, it should be completely spelled out in the slug. They are acceptable everywhere else', 'function': place_02},

#   'numbers_01': {'ruleDesc': 'The general rule for exact numbers is to spell out zero to nine and use digits for 10 onwards', 'function': numbers_01},
#   'numbers_02': {'ruleDesc': 'When describing age, use the format x-year-old but only if it is an adjective', 'function': numbers_02},
#   'numbers_03': {'ruleDesc': 'if using digits in a phrase, use only digits and not spelled out numbers', 'function': numbers_03},
#   'numbers_04': {'ruleDesc': 'If a sentence begins with a number, spell it out, unless it is a year', 'function': numbers_04},
#   'numbers_05': {'ruleDesc': 'When describing number ranges, use "to" and not hyphen', 'function': numbers_05},
#   'numbers_06': {'ruleDesc': 'Spell out first to ninth unless it is describing a congressional district, court, division, or military unit', 'function': numbers_06},
#   'numbers_07': {'ruleDesc': 'For top <number>, the word top is lowercase.', 'function': numbers_07},
#   'numbers_08': {'ruleDesc': 'using No. X should always be capitalized', 'function': numbers_08},
#   'numbers_09': {'ruleDesc': 'Never use XX-k to refer to thousands', 'function': numbers_09},
#   'numbers_10': {'ruleDesc': 'Use % and not percent, also separated by a space', 'function': numbers_10},
#   'numbers_11': {'ruleDesc': 'No need for .0 in percentages', 'function': numbers_11},
#   'numbers_12': {'ruleDesc': 'Spell out fractions', 'function': numbers_12},
#   'numbers_13': {'ruleDesc': 'Use P instead of Php, without space, $ and not USD', 'function': numbers_13},
#   'numbers_14': {'ruleDesc': 'multimillion, multibillion has no hyphen', 'function': numbers_14},
#   'numbers_15': {'ruleDesc': 'Use km/h not kph', 'function': numbers_15},
#   'numbers_16': {'ruleDesc': 'Use kWh not kwh', 'function': numbers_16},
#   'numbers_17': {'ruleDesc': 'For internet speeds, put a space between the number and the unit of measurement', 'function': numbers_17},
#   'numbers_18': {'ruleDesc': 'For temperatures, go straight to °C and °F.', 'function': numbers_18},
#   'numbers_19': {'ruleDesc': 'Use Roman numerals for World War I and World War II.', 'function': numbers_19},
#   'grammar_01': {'ruleDesc': 'use results in, not results to', 'function': grammar_01},
#   'grammar_02': {'ruleDesc': 'dont use "for" after seek/sought', 'function': grammar_02},
#   'grammar_03': {'ruleDesc': 'dont use "as" after called/dubbed', 'function': grammar_03},
#   'grammar_04': {'ruleDesc': '"on the other hand" should have "on the one hand" in the same paragraph', 'function': grammar_04},
#   'punctuation_01': {'ruleDesc': 'Use the Oxford or serial comma', 'function': punctuation_01},
#   'punctuation_02': {'ruleDesc': 'Capitalization after a colon:', 'function': punctuation_02},
#   'punctuation_03': {'ruleDesc': 'A dash is used to separate word/s. We commonly use the en dash (–), not the em dash (—), with spaces', 'function': punctuation_03},
#   'punctuation_04': {'ruleDesc': 'When words end with s, use just an apostrophe for the possessive form.', 'function': punctuation_04},
#   'politicolegal_01': {'ruleDesc': 'It’s charged with, not charged of', 'function': politicolegal_01},
#   'politicolegal_02': {'ruleDesc': 'It’s indicted for, not indicted of.', 'function': politicolegal_02},
#   'politicolegal_03': {'ruleDesc': 'It’s plead guilty to, not plead guilty of.', 'function': politicolegal_03},
#   'politicolegal_04': {'ruleDesc': 'It’s convicted of and acquitted of, not for', 'function': politicolegal_04}
#   }

# def fix_format(func, result):
#     '''Reformat output to align with API expectations'''
#     return {'ruleCode': func.__name__, 
#             'ruleResult': 'FAIL' if len(result) else 'PASS', 
#             'resultDesc': rules[func.__name__]['ruleDesc']}
