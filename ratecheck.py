import os
import csv
import re

origin_dir = "origin"
algorithm_dir = "algorithm"
output_csv = "comparison_results.csv"

results = []

for filename in os.listdir(origin_dir):
    origin_path = os.path.join(origin_dir, filename)
    algorithm_path = os.path.join(algorithm_dir, filename)

    if os.path.isfile(origin_path) and os.path.isfile(algorithm_path):
        with open(origin_path, 'r', encoding='utf-8') as origin_file, \
             open(algorithm_path, 'r', encoding='utf-8') as algorithm_file:
            print(f"Processing {filename}...")
            origin_content = origin_file.read()
            algorithm_content = algorithm_file.read()
        
            origin_sentences = re.split(r'[.!?\n]', origin_content)
            algorithm_sentences = re.split(r'[.!?\n]', algorithm_content)

            origin_sentences = [re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z가-힣\s]', '', sentence)).strip() for sentence in origin_sentences if sentence.strip()]
            algorithm_sentences = [re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z가-힣\s]', '', sentence)).strip() for sentence in algorithm_sentences if sentence.strip()]
        
            origin_sentences = [sentence for sentence in origin_sentences if sentence]
            algorithm_sentences = [sentence for sentence in algorithm_sentences if sentence]

            unmatched_sentences = []
            match_ratio = 0.0
            for sentence in origin_sentences:
                sentence = sentence.strip()
                if sentence and any(sentence in algo_sentence for algo_sentence in algorithm_sentences):
                    match_ratio += 1
                else:
                    unmatched_sentences.append(sentence)

            if origin_sentences:
                match_ratio /= len(origin_sentences)

            extra_algorithm_sentences = [
                sentence for sentence in algorithm_sentences 
                if not any(sentence in origin_sentence for origin_sentence in origin_sentences)
            ]
            extra_count = len(extra_algorithm_sentences)

            results.append([filename, len(origin_sentences), len(algorithm_sentences), match_ratio, "; ".join(unmatched_sentences), extra_count])

with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Filename", "Number of origin setences", "Number of extracted setences", "Match Ratio", "Unmatched Sentences", "Extra Count"])
    writer.writerows(results)

print(f"Comparison results saved to {output_csv}")