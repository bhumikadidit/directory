import pandas as pd
import re
from collections import Counter

class CleanAndMerge:
    def __init__(self, dict_file='../data/raw/correct_districts.txt'):
        """Initialize with a dictionary file for corrections."""
        try:
            with open(dict_file, 'r', encoding='utf-8') as f:
                big_text = f.read()
            self.WORDS = Counter(self.words(big_text))
            self.N = sum(self.WORDS.values())
            if self.N == 0:
                raise ValueError("Dictionary file is empty or has no valid words.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Dictionary file '{dict_file}' not found.")

    def words(self, text):
        """Extract words from text."""
        return re.findall(r'\w+', text.lower())

    def P(self, word):
        """Probability of a word."""
        return self.WORDS.get(word, 0) / self.N if self.N > 0 else 0

    def edits1(self, word):
        """Generate 1-edit candidates."""
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits if b for c in letters]
        inserts = [a + c + b for a, b in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def known(self, words):
        """Filter known words."""
        return set(w for w in words if w in self.WORDS)

    def candidates(self, word):
        """Generate correction candidates."""
        return self.known([word]) or self.known(self.edits1(word)) or [word]

    def correction(self, word):
        """Correct a word."""
        cands = self.candidates(word)
        return max(cands, key=self.P) if cands else word

    def clean_dataframe(self, df):
        """Clean a DataFrame by correcting the 'District' column."""
        df['District'] = df['District'].apply(
            lambda x: self.correction(str(x).lower()) if pd.notna(x) else x
        )
        return df

    def process_files(self, kpi_1_path, kpi_2_path):
        """Process files: clean each and return cleaned DataFrames and merged DF"""
        df1 = pd.read_csv(kpi_1_path)
        df2 = pd.read_csv(kpi_2_path)
        df1_clean = self.clean_dataframe(df1)
        df2_clean = self.clean_dataframe(df2)

        merged = pd.merge(df1_clean, df2_clean, on='District', how='outer')

        return df1_clean, df2_clean, merged

if __name__ == '__main__':
    
    dict_file = '../data/raw/correct_districts.txt'
    kpi1_path = '../data/raw/kpi_1.csv'
    kpi2_path = '../data/raw/kpi_2.csv'
    
    cleaner = CleanAndMerge(dict_file)

    with open(dict_file, 'r', encoding='utf-8') as f:
        dict_text = f.read()

    df1 = pd.read_csv(kpi1_path)
    df2 = pd.read_csv(kpi2_path)

    cleaner = CleanAndMerge(dict_text)
    df1_cleaned, df2_cleaned, merged_df = cleaner.process_files(df1, df2)

    df1_cleaned.to_csv('../data/temp/kpi_1_cleaned.csv', index=False)
    df2_cleaned.to_csv('../data/temp/kpi_2_cleaned.csv', index=False)
    merged_df.to_csv('../data/processed/merged_kpi.csv', index=False)

    print("Data cleaning and merging completed.")
