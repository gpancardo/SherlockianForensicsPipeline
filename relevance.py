import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import itertools

# Load spaCy
nlp = spacy.load("en_core_web_md")

DATA_DIR = "books"

# Seeds
seed_terms = ["bullet", "poison", "arsenic", "footprint", "residual", "blood", "knife", "gunpowder", "biological", "trace", "fiber", "judge", "evidence", "handwriting", "pen", "ink", "witness", "pistol", "dagger", "cartridge","blade","cyanide","opium","belladona","alcohol","tonic", "ash", "tobacco", "hair", "secretion", "morgue", "artery", "vein", "bone", "furniture", "envelope", "letter", "document","hat", "glove", "cane", "handkerchief", "shoe", "sole", "boot", "thread"]

# Texts
texts = []
for fname in os.listdir(DATA_DIR):
    if fname.endswith("_clean.txt"):
        with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
            texts.append(f.read())

# Get nouns
def extract_nouns(text):
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

noun_texts = [" ".join(extract_nouns(text)) for text in texts]

# n-gram generation
def generate_ngrams(text, n=3):
    tokens = text.split()
    ngrams = []
    for i in range(1, n+1):
        ngrams.extend(['_'.join(tokens[j:j+i]) for j in range(len(tokens)-i+1)])
    return ngrams

all_ngrams = []
for doc in noun_texts:
    all_ngrams.append(" ".join(generate_ngrams(doc, n=3)))

#TF-IDF calculation
vectorizer = TfidfVectorizer(min_df=2) 
X = vectorizer.fit_transform(all_ngrams)
terms = vectorizer.get_feature_names_out()
scores = X.sum(axis=0).A1
tfidf_scores = dict(zip(terms, scores))

# Top 1000 TF-IDF
top_terms = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:300]

# Find similar words for each seed term
def expand_with_similarity(seed_terms, candidate_terms, top_k=30):
    expansions = set()
    for seed in seed_terms:
        if seed in nlp.vocab:
            seed_vec = nlp(seed).vector
            sims = []
            for term in candidate_terms:
                term_vec = nlp(term.replace("_", " ")).vector
                if term_vec.any():
                    sim = nlp(seed).similarity(nlp(term.replace("_", " ")))
                    sims.append((term, sim))
            sims.sort(key=lambda x: x[1], reverse=True)
            expansions.update([t for t, _ in sims[:top_k]])
    return list(expansions)

expanded_terms = expand_with_similarity(seed_terms, terms)

final_terms = set([t for t, _ in top_terms]) | set(expanded_terms)

with open("relevant_terms.txt", "w", encoding="utf-8") as f:
    for term in sorted(final_terms):
        f.write(term + "\n")

print(f"Se extrajeron {len(final_terms)} términos relevantes.")
