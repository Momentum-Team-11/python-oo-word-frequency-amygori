import string

STOP_WORDS = [
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "i",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "were",
    "will",
    "with",
]


class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def read_contents(self):
        """
        This should read all the contents of the file
        and return them as one string.
        """
        with open(self.filename) as file:
            text_string = file.read()

        return text_string


class WordList:
    def __init__(self, text_string):
        self.list = []
        self.text = text_string
        self.longest_word_length = 0

    def extract_words(self):
        """
        This should get all words from the text. This method
        is responsible for lowercasing all words and stripping
        them of punctuation.
        """
        self.list = self.text.lower().strip().split()
        transformed_words = []
        for word in self.list:
            if word not in STOP_WORDS:
                transformed_words.append(word.strip(string.punctuation))
        self.list = transformed_words

    def set_longest_word_length(self, word):
        if len(word) > self.longest_word_length:
            self.longest_word_length = len(word)

    def get_freqs(self):
        """
        Returns a data structure of word frequencies that
        FreqPrinter can handle. Expected to be run after
        extract_words and remove_stop_words. The data structure
        could be a dictionary or another type of object.
        """
        word_count = {}
        for word in self.list:
            self.set_longest_word_length(word)
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1

        return word_count


class FreqPrinter:
    """Handles a dictionary of word frequencies"""

    def __init__(self, freqs, longest_word_length):
        self.freqs = freqs
        self.left_margin = longest_word_length + 1

    def use_count_as_key(self, items):
        """
        Provide a key for the sorted function so that words can be sorted by count.
        """
        return items[1]

    def print_freqs(self):
        """
         Prints out a frequency chart of the top 10 items
         in our frequencies data structure.

         Example:
           her | 33   *********************************
         which | 12   ************
           all | 12   ************
          they | 7    *******
         their | 7    *******
           she | 7    *******
          them | 6    ******
          such | 6    ******
        rights | 6    ******
         right | 6    ******
        """
        sorted_words = sorted(
            self.freqs.items(), key=self.use_count_as_key, reverse=True
        )

        for word, count in sorted_words:
            print(
                f"{word.rjust(self.left_margin)}",
                " | ",
                str(count).ljust(4),
                ("*" * count),
            )


if __name__ == "__main__":
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Get the word frequency in a text file."
    )
    parser.add_argument("file", help="file to read")
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        reader = FileReader(file)
        word_list = WordList(reader.read_contents())
        word_list.extract_words()

        printer = FreqPrinter(word_list.get_freqs(), word_list.longest_word_length)
        printer.print_freqs()
    else:
        print(f"{file} does not exist!")
        sys.exit(1)
