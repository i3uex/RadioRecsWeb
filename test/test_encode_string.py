from unittest import TestCase

from engine import encode_string


class TestEncodeString(TestCase):
    def test_encode_string(self):
        self.assertEqual(encode_string("Word"), "word", "Encoded string is not lower-cased")
        self.assertEqual(encode_string("Word Word"), "word_word", "Spaces were not replaced in encoded string")
