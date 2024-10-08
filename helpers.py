import re

def get_context(text, start, end, context_size=2, context_unit='words'):
    """
    Helper function to extract context around a match, with context_size
    specified in terms of characters, words, or sentences.

    :param text: The full text to extract context from.
    :param start: Start position of the match.
    :param end: End position of the match.
    :param context_size: Size of the context to extract.
    :param context_unit: Unit of the context size ('chars', 'words', or 'sentences').
    :return: Context string surrounding the match.
    """
    # Extract context by character length
    if context_unit == 'chars':
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        context = text[context_start:context_end]

    # Extract context by word count
    elif context_unit == 'words':
        words = re.findall(r'\S+', text)  # Split the text into words
        start_word_idx = len(re.findall(r'\S+', text[:start]))
        end_word_idx = len(re.findall(r'\S+', text[:end]))

        context_start_idx = max(0, start_word_idx - context_size)
        context_end_idx = min(len(words), end_word_idx + context_size)

        context = ' '.join(words[context_start_idx:context_end_idx])

    # Extract context by sentence count
    elif context_unit == 'sentences':
        # Split text into sentences (simple assumption: sentences end with punctuation followed by space)
        sentences = re.split(r'(?<=[.!?])\s+(?=\S)', text)

        # Approximate the start and end positions of the sentences based on character indices
        cumulative_char_count = 0
        start_sentence_idx, end_sentence_idx = 0, 0
        for i, sentence in enumerate(sentences):
            sentence_len = len(sentence)
            if cumulative_char_count <= start <= cumulative_char_count + sentence_len:
                start_sentence_idx = i
            if cumulative_char_count <= end <= cumulative_char_count + sentence_len:
                end_sentence_idx = i
                break
            cumulative_char_count += sentence_len + 1  # Add 1 for space after the sentence
        context_start_idx = max(0, start_sentence_idx - context_size)
        context_end_idx = min(len(sentences), end_sentence_idx + context_size)
        context = ' '.join(sentences[context_start_idx:context_end_idx])

    else:
        raise ValueError("Invalid context_unit. Use 'chars', 'words', or 'sentences'.")
    return context.strip()