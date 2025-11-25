import unittest
import pandas as pd
# Import the functions we want to test
from garbage_filter import calculate_text_entropy, type_token_ratio, contains_boilerplate

class TestGANISFilters(unittest.TestCase):
    
    def test_entropy_logic(self):
        """Test that complex text has higher entropy than repetitive text."""
        # High entropy: varied characters
        high_ent = calculate_text_entropy("The quick brown fox jumps over the lazy dog and explores the dataset.")
        # Low entropy: repetitive characters
        low_ent = calculate_text_entropy("loading loading loading loading loading")
        
        print(f"\n[Test] High Entropy: {high_ent:.2f} | Low Entropy: {low_ent:.2f}")
        self.assertTrue(high_ent > 4.0, "Complex text entropy should be high (>4.0)")
        self.assertTrue(low_ent < 3.8, "Repetitive text entropy should be low (<3.8)")

    def test_ttr_logic(self):
        """Test Type-Token Ratio (Vocabulary Richness)."""
        # Rich vocabulary
        text_rich = "Generative AI presents novel challenges for academic policy and institutional governance."
        # Poor vocabulary
        text_poor = "AI AI AI AI AI AI AI"
        
        self.assertTrue(type_token_ratio(text_rich) > 0.8, "Rich text should have high TTR")
        self.assertTrue(type_token_ratio(text_poor) < 0.3, "Repetitive text should have low TTR")

    def test_boilerplate_detection(self):
        """Test that boilerplate keywords are flagged correctly."""
        # Mock row representing a dataframe row with boilerplate
        row_garbage = {
            "content_text": "Please enable javascript to view this page.",
            "Title": "Privacy Policy",
            "top_bigrams": "cookie settings",
            "top_trigrams": "terms of use"
        }
        
        # Mock row representing legitimate content
        row_clean = {
            "content_text": "The university is launching a new research grant for LLM studies.",
            "Title": "News Release",
            "top_bigrams": "artificial intelligence",
            "top_trigrams": "generative ai models"
        }

        self.assertTrue(contains_boilerplate(row_garbage), "Should flag 'cookie settings' or 'privacy policy'")
        self.assertFalse(contains_boilerplate(row_clean), "Should NOT flag legitimate research text")

if __name__ == '__main__':
    print("Running GANIS Smoke Tests...")
    unittest.main()