import spacy
from pathlib import Path
from collections import Counter

# Load English spaCy
nlp = spacy.load("en_core_web_sm")

def extract_oov_words(folder_path, max_freq=7):
    oov_counter = Counter()
    
    # Go through clean files
    for file in Path(folder_path).glob("*_clean.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
        doc = nlp(text)
        
        for token in doc:
            if token.is_alpha and not token.is_stop and token.is_oov:
                oov_counter[token.text] += 1
    
    # Filter by low frequency
    filtered_oov = [word for word, freq in oov_counter.items() if freq <= max_freq]
    
    return sorted(filtered_oov)

# Run
folder_path = "books" 
oov_terms = extract_oov_words(folder_path, max_freq=10)

with open("rareOovTerms.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(oov_terms))

print(f"Low frequency (≤7) words: {len(oov_terms)}")
