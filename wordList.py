import csv

# Paths to input files
rare_oov_path = 'rareOovTerms.txt'
relevant_terms_path = 'relevant_terms.txt'
output_csv_path = 'merged_terms.csv'

# Read words from both files
def read_terms(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

terms = []
terms += read_terms(rare_oov_path)
terms += read_terms(relevant_terms_path)

# Write to CSV with specified columns
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['ID', 'TERM', 'DEFINITION', 'CATEGORY', 'TOTAL_FREQUENCY', 'BOOKS'])
    writer.writeheader()
    for idx, term in enumerate(terms, start=1):
        writer.writerow({
            'ID': idx,
            'TERM': term,
            'DEFINITION': '',
            'CATEGORY': '',
            'TOTAL_FREQUENCY': '',
            'BOOKS': ''
        })