import os
import glob
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load spaCy English model (download if needed: python -m spacy download en_core_web_md)
nlp = spacy.load("en_core_web_md")

# Seed terms by category
seed_terms = {
    "Weapons and projectiles": [
        "bullet", "knife", "gunpowder", "pistol", "dagger", "cartridge", "blade"
    ],
    "Substances and poisons": [
        "poison", "arsenic", "cyanide", "opium", "belladona", "alcohol", "tonic"
    ],
    "Physical evidence": [
        "residual", "trace", "fiber", "evidence", "handwriting", "ink", "ash", "tobacco", "thread"
    ],
    "Crime scene objects": [
        "furniture", "envelope", "letter", "document"
    ],
    "Clothing and personal items": [
        "hat", "glove", "cane", "handkerchief", "shoe", "sole", "boot"
    ],
    "Injuries and body parts": [
        "blood", "biological", "hair", "secretion", "artery", "vein", "bone"
    ],
    "Locations and environments": [
        "morgue"
    ],
    "Detection and investigation terms": [
        "footprint", "pen", "witness", "judge"
    ],
    "Victorian slang and social context": []
}

# Directory with your _clean.txt files
input_dir = "./wordLists"  # Change this path
file_pattern = os.path.join(input_dir, "*relevant_terms.txt")

# Read all text files
documents = []
for file in glob.glob(file_pattern):
    with open(file, "r", encoding="utf-8") as f:
        documents.append(f.read())

# Flatten documents into terms (they are already cleaned and lowercase)
all_text = " ".join(documents)
terms = list(set(all_text.split()))

# Prepare seed vectors for similarity
category_vectors = {cat: nlp(" ".join(words)) for cat, words in seed_terms.items() if words}

# Check which terms are seeds
all_seed_terms = set([t for sublist in seed_terms.values() for t in sublist])

results = []

for term in terms:
    doc_term = nlp(term)

    # Compute similarity to each category
    best_cat = None
    best_score = 0.0
    for category, cat_vector in category_vectors.items():
        sim = doc_term.similarity(cat_vector)
        if sim > best_score:
            best_score = sim
            best_cat = category

    # Check if OOV (not in spaCy vocab)
    oov = not doc_term.has_vector

    results.append({
        "term": term,
        "suggested_category": best_cat if best_cat else "General use",
        "similarity_score": round(best_score, 4),
        "is_seed": term in all_seed_terms,
        "oov": oov
    })

# Save to CSV
df = pd.DataFrame(results)
df.sort_values(by="term", ascending=False, inplace=True)
df.to_csv("auto_assessment.csv", index=False)

print("✅ Done! Results saved to auto_assessment.csv")
print(df.head(20))
