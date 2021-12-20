class TestPhraseValidation:
    def test_phrase(self):
        phrase = input("Set a phrase: ")
        expected_result = 15
        assert len(phrase) < expected_result, f"Phrase length is longer than {expected_result}"
