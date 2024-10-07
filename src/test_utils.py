import unittest

from markdown_utils import (
    extract_title,
)  # Replace 'your_module_name' with the actual module name


class TestExtractTitle(unittest.TestCase):

    def test_basic_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_spaces(self):
        self.assertEqual(extract_title("#   Spaced Out   "), "Spaced Out")

    def test_no_header(self):
        with self.assertRaises(Exception):
            extract_title("Not a header")

    def test_empty_string(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_multiple_words(self):
        self.assertEqual(extract_title("# Multiple Word Title"), "Multiple Word Title")


if __name__ == "__main__":
    unittest.main()
