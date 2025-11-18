import unittest
import pandas as pd
from collections import Counter
from merge.main import CleanandMerge

class TestCleanandMerge(unittest.TestCase):
    def setUp(self):
        # Provide minimal sample district data for dictionary
        self.sample_districts = 'dhanusha\nkathmandu\nkavrepalanchowk'
        
        # Instead of using default file, initiate with sample text
        self.cleaner = CleanandMerge(dict_file=None)
        self.cleaner.WORDS = Counter(self.cleaner.words(self.sample_districts))
        self.cleaner.N = sum(self.cleaner.WORDS.values())

        # Sample data simulating your CSV content
        self.df1 = pd.DataFrame({
            'District': ['dhanusa', 'kathmandu', 'kavre palanchowk'],
            'KPI_1': [0.85, 0.8, 0.75]
        })

        self.df2 = pd.DataFrame({
            'District': ['dhanusha', 'kathmandu', 'kavrepalanchowk'],
            'KPI_2': [0.6, 0.35, 0.65]
        })

    def test_clean_correction(self):
        corrected_df1 = self.cleaner.clean_csv(self.df1)
        self.assertIn('dhanusha', corrected_df1['District'].values)

    def test_merge_rows(self):
        df1_cleaned, df2_cleaned, merged = self.cleaner.process_and_merge(self.df1, self.df2)
        self.assertTrue('dhanusha' in merged['District'].values)
        self.assertFalse('dhanusa' in merged['District'].values)
        self.assertEqual(len(merged['District'].unique()), 3)

if __name__ == '__main__':
    unittest.main()
