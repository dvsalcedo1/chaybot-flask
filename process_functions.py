from helpers import get_context
from nltk.tag import pos_tag
import spacy
import re

nlp = spacy.load('en_core_web_lg')

## Headline
def head_01(text):
    '''Headlines should not exceeed 70 characters'''
    if len(text) > 70:
        return [text]
    else:
        return []

def head_06(text, **kwargs):
    '''Headlines shouldn’t have long words (more than 12 characters)'''

    return [word for word in text.split() if len(word) > 12]

def head_09(text, **kwargs):
    '''Headlines should have single quotes and not double quotes'''
    offending_strings = []
    matches = list(re.finditer(r'"(.*?)"', text))

    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def head_10(text, **kwargs):
    '''Headlines should use en dash and not hyphen or colon when indicating source'''

    offending_strings = []
    matches = list(re.finditer(r'-|:', text))  # Checking for hyphen (-) or colon (:)
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def head_11(text, **kwargs):
    '''Headlines should use digits and not spelled out numbers except for zero'''
    offending_strings = []
    number_pattern = r'\b(one|two|three|four|five|six|seven|eight|nine|ten)\b'
    matches = list(re.finditer(number_pattern, text, re.IGNORECASE))
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def head_12(text, **kwargs):
    '''Headline word after colon should be capitalized'''
    offending_strings = []
    matches = list(re.finditer(r':\s[a-z]', text))  # Check if the first letter after colon is lowercase
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

## Subhead
def subhead_01(text, **kwargs):
    '''Subhead should not exceed 200 characters'''
    if len(text) > 200:
        return [text[:200] + '...']
    return []

def subhead_06(text, **kwargs):
    '''Subhead should have single quotes and not double quotes'''
    offending_strings = []
    matches = list(re.finditer(r'"(.*?)"', text))
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

## Dateline
def dateline_03(text, **kwargs):
    '''Metro Manila Dateline should use MANILA, PHILIPPINES'''
    if 'Manila, Philippines' in text:
        return ['Manila, Philippines']
    return []

## Breaker
# def breaker_01(text, **kwargs):
#     '''Breakers should be in H5 format'''
#     #N/A
#     return []

def breaker_02(text, **kwargs):
    '''Breakers should not exceed 4 words'''
    words = text.split()
    if len(words) > 4:
        return [text]
    return []

def breaker_05(text, **kwargs):
    '''Breakers use single quotes, not double quotes or italics'''
    offending_strings = []
    matches = list(re.finditer(r'["“”]', text))  # Matches both straight and curly quotes
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings


## URL
def url_01(text, **kwargs):
    '''URLs should have 11 words max'''
    if len(text.split()) > 11:
        return [text]
    return []

def url_04(text, **kwargs):
    '''URLs should not have punctuations'''
    offending_strings = []
    if re.search(r'[.,!?]', text):  # Check for any punctuation marks
        offending_strings.append(text)
    
    return offending_strings

def url_06(text, **kwargs):
    '''URLs should not begin with a number'''
    if re.match(r'^\d', text):
        return [text]
    return []


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

def politicolegal_07(text, **kwargs):
    '''It’s "right against self-incrimination", not "right to self-incrimination"'''
    if 'right to self-incrimination' in text:
        offending_strings = [get_context(text, text.index('right to self-incrimination'), 
                                          text.index('right to self-incrimination') + 26, **kwargs)]
        return offending_strings
    return []

def politicolegal_15(text, **kwargs):
    '''Show cause order, temporary restraining order, writ of amparo, writ of habeas corpus, writ of kalikasan, affidavit and similar should be lowercase'''
    legal_terms = ['Show Cause Order', 'Temporary Restraining Order', 'Writ of Amparo', 'Writ of Habeas Corpus', 
                   'Writ of Kalikasan', 'Affidavit']
    offending_strings = []
    for term in legal_terms:
        if term in text:
            match = re.search(term, text)
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def disasters_02(text, **kwargs):
    '''Various weather systems are lowercase'''
    weather_systems = ['Tropical Cyclone', 'Low Pressure Area', 'Intertropical Convergence Zone', 
                       'Southwest Monsoon', 'Northeast Monsoon', 'Tail-end of a Frontal System', 'Easterlies']
    offending_strings = []
    for term in weather_systems:
        if term in text:
            match = re.search(term, text)
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def disasters_07(text, **kwargs):
    '''Use earthquake (not quake) in headlines and URLs. Quake is acceptable in the body'''
    offending_strings = []
    if 'quake' in text:
        match = re.search('quake', text)
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def disasters_09(text, **kwargs):
    '''For volcanoes, spell out "Mount" and not "Mt."'''
    offending_strings = []
    if 'Mt.' in text:
        match = re.search('Mt\.', text)
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def health_01(text, **kwargs):
    '''A pandemic is global. Just say pandemic, not "global pandemic"'''
    offending_strings = []
    if 'global pandemic' in text:
        match = re.search('global pandemic', text)
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def health_02(text, **kwargs):
    '''Coronavirus is acceptable on first mention. Add "the" before coronavirus'''
    offending_strings = []
    if 'coronavirus' in text and not 'the coronavirus' in text:
        match = re.search('coronavirus', text)
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def health_03(text, **kwargs):
    '''Use "COVID-19", not "Covid-19", "COVID", or "Covid"'''
    offending_strings = []
    covid_variants = ['Covid-19', 'COVID', 'Covid']
    for variant in covid_variants:
        if variant in text:
            match = re.search(variant, text)
            start, end = match.start(), match.end()
            offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def race_02(text, **kwargs):
    '''The plural form of Lumad is still Lumad, not Lumads'''
    if 'Lumads' in text:
        match = re.search('Lumads', text)
        start, end = match.start(), match.end()
        return [get_context(text, start, end, **kwargs)]
    return []

def race_04(text, **kwargs):
    '''Capitalize "Black" when referring to race'''
    offending_strings = []
    matches = list(re.finditer(r'\bblack\b', text, re.IGNORECASE))
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def gender_02(text, **kwargs):
    '''It’s trans man/trans woman, not transman/transwoman'''
    offending_strings = []
    matches = list(re.finditer(r'transman|transwoman', text, re.IGNORECASE))
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def gender_03(text, **kwargs):
    '''"Transgender" is an adjective, do not use it as a noun'''
    offending_strings = []
    matches = list(re.finditer(r'\btransgender\b(?!\s(man|woman))', text, re.IGNORECASE))
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def gender_04(text, **kwargs):
    '''Use "they/them/their" instead of "he/she" or "him/her"'''
    offending_strings = []
    matches = list(re.finditer(r'he\/she|him\/her', text, re.IGNORECASE))
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def photos_01(text, **kwargs):
    '''Each photo caption begins with a title in all caps, no more than two words, followed by a period'''
    # N/A - This would likely require more contextual info about the image and caption structure
    return []

def photos_02(text, **kwargs):
    '''Photo caption should only be one sentence'''
    if len(text.split('.')) > 1:
        return [text]
    return []

def photos_05(text, **kwargs):
    '''Photo caption should use single and not double quotes'''
    offending_strings = []
    matches = list(re.finditer(r'"(.*?)"', text))
    
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    
    return offending_strings

def photos_06(text, **kwargs):
    '''Photo caption date format should be Month Day, Year'''
    offending_strings = []
    matches = list(re.finditer(r'\b\d{4}-\d{2}-\d{2}\b', text))  # Matches "YYYY-MM-DD" format
    for match in matches:
        start, end = match.start(), match.end()
        offending_strings.append(get_context(text, start, end, **kwargs))
    return offending_strings

def photos_08(text, **kwargs):
    '''Photo credits should not contain "Photo by"'''
    if 'Photo by' in text:
        return [text]
    return []

def photos_12(text, **kwargs):
    '''Reuters photos should use Name/Reuters or Original Source/Reuters'''
    # N/A
    return []

def photos_15(text, **kwargs):
    '''If the photo is a screenshot from a video, put "Rappler video screenshot"'''
    if 'screengrab' in text:
        match = re.search('screengrab', text)
        start, end = match.start(), match.end()
        return [get_context(text, start, end, **kwargs)]
    return []

def photos_16(text, **kwargs):
    '''When in doubt about the source of a photo or unsure who to credit, do not use'''
    # N/A - This would depend on external info
    return []

def hyperlinks_01(text, **kwargs):
    '''Put hyperlinks in stories whenever applicable, aim for at least 3 or more'''
    hyperlinks = re.findall(r'(https?://[^\s]+)', text)  # Finds URLs
    if len(hyperlinks) < 3:
        return [text]
    return []

