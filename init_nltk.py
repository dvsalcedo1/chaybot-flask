import nltk
import subprocess

nltk.download('averaged_perceptron_tagger_eng')
subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_lg'], check=True)