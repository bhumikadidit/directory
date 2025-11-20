import unittest
import os
import pandas as pd
from merge.main import CleanAndMerge  

class TestCleanAndMergePipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Define file paths relative to this test file
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        cls.dict_file = os.path.join(base_dir, 'data', 'raw', 'correct_districts.txt')
        cls.kpi1_path = os.path.join(base_dir, 'data', 'raw', 'kpi_1.csv')
        cls.kpi2_path = os.path.join(base_dir, 'data', 'raw', 'kpi_2.csv')

        cls.cleaner = CleanAndMerge(dict_file=cls.dict_file)

    def test_process_files_runs_without_error(self):
        # Run the pipeline to clean and merge the files
        df1_cleaned, df2_cleaned, merged_df = self.cleaner.process_files(self.kpi1_path, self.kpi2_path)

        # Check that outputs are DataFrames
        self.assertIsInstance(df1_cleaned, pd.DataFrame)
        self.assertIsInstance(df2_cleaned, pd.DataFrame)
        self.assertIsInstance(merged_df, pd.DataFrame)

        # Check essential 'District' column exists
        self.assertIn('District', df1_cleaned.columns)
        self.assertIn('District', df2_cleaned.columns)
        self.assertIn('District', merged_df.columns)

    def test_correction_logic(self):
        # test known typo correction with spaces removed
        self.assertEqual(self.cleaner.correction('dhanusa'), 'dhanusha')
        self.assertEqual(self.cleaner.correction('kavrepalanchowk'), 'kavrepalanchowk')
    
        # optional: normalize spaced input before correction
        spaced_input = 'kavre palanchowk'.replace(' ', '')
        self.assertEqual(self.cleaner.correction(spaced_input), 'kavrepalanchowk')
        # correct district unaltered
        self.assertEqual(self.cleaner.correction('kathmandu'), 'kathmandu')
        
if __name__ == '__main__':
    unittest.main()
