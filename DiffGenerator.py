import difflib


DIFF_HTML_NAME = "diff.html"
MATCH_FILE_NAME = "match.txt"
QA_DIFFERENCE_FILE_NAME = "qa_diff.txt"
BASE_DIFFERENCE_FILE_NAME = "base_diff.txt"


class DiffGenerator(object):
    open_files = list()

    READ_MODE, WRITE_MODE = "r", "w"

    EMPTY_STRING = ""

    IDENTICAL_FILE_LINE_PLACEHOLDER = "Line {} is identical : {}"

    def open_file(self, name, mode):
        """ Helper function to keep track of open files.
        """
        file = open(name, mode)
        self.open_files.append(file)
        return file

    def close_files(self):
        """ Helper function to close all open files.
        """
        for each in self.open_files:
            each.close()

    def __init__(self, input_file_one, input_file_two):
        """
            :argument input_file_one: Path of the first file to compare.
            :argument input_file_two: Path of the second file to compare.
        """
        self.base_file_content, self.qa_file_content = \
            self.open_file(input_file_two, self.READ_MODE).readlines(), \
            self.open_file(input_file_one, self.READ_MODE).readlines()
        self.QA_INPUT_FILE_NAME, self.BASE_INPUT_FILE_NAME = input_file_one, input_file_two

        self._compute_longer_shorter()

        self.DIFF_FILE_NAME = "diff.html"
        self.MATCH_FILE_NAME = "match.txt"
        self.QA_DIFFERENCE_FILE_NAME = "qa_diff.txt"
        self.BASE_DIFFERENCE_FILE_NAME = "base_diff.txt"

    def __del__(self):
        self.close_files()

    def _compute_longer_shorter(self):
        """ Helper function to determine which file is longer
        """
        if len(self.base_file_content) > len(self.qa_file_content):
            self.shorter, self.longer = self.qa_file_content, self.base_file_content
            self.shorter_file, self.longer_file = self.open_file(self.QA_INPUT_FILE_NAME, self.READ_MODE), \
                self.open_file(self.BASE_INPUT_FILE_NAME, self.READ_MODE)
            self.base_shorter = False
        else:
            self.shorter, self.longer = self.base_file_content, self.qa_file_content
            self.shorter_file, self.longer_file = self.open_file(self.BASE_INPUT_FILE_NAME, self.READ_MODE), \
                self.open_file(self.QA_INPUT_FILE_NAME, self.READ_MODE)
            self.base_shorter = True

    def generate_txt_diff(self, output_match_file=MATCH_FILE_NAME,
                          output_file_one=QA_DIFFERENCE_FILE_NAME,
                          output_file_two=BASE_DIFFERENCE_FILE_NAME):
        """ Generates the TXT difference of the two files

        :argument output_match_file: Path of the match file to generate.
        :argument output_file_one: Path of the file to contain diff of input_file_one.
        :argument output_file_two: Path of the file to contain diff of input_file_two.

        :return: None
        """

        _match_file = self.open_file(output_match_file, self.WRITE_MODE)
        _diff_one = self.open_file(output_file_one, self.WRITE_MODE)
        _diff_two = self.open_file(output_file_two, self.WRITE_MODE)

        # LOOPING BETWEEN BOTH FILES TILL SHORTER FILE
        for index, line_from_shorter in enumerate(self.shorter):
            line_from_longer = self.longer[index]
            if line_from_shorter == line_from_longer:
                print(self.IDENTICAL_FILE_LINE_PLACEHOLDER.format(index + 1, line_from_shorter),
                      file=_match_file, end=self.EMPTY_STRING)
                print(self.EMPTY_STRING, file=_diff_one)
                print(self.EMPTY_STRING, file=_diff_two)
            else:
                if self.base_shorter:
                    print(line_from_shorter, file=_diff_one, end=self.EMPTY_STRING)
                    print(line_from_longer, file=_diff_two, end=self.EMPTY_STRING)
                else:
                    print(line_from_shorter, file=_diff_two, end=self.EMPTY_STRING)
                    print(line_from_longer, file=_diff_one, end=self.EMPTY_STRING)

        # LOOPING THROUGH REMAINING OF LONGER FILE
        if len(self.shorter) != len(self.longer):
            for remaining in self.longer[len(self.shorter):]:
                print(remaining, file=_diff_two if self.base_shorter else _diff_one,
                      end=self.EMPTY_STRING)

    def generate_html_diff(self, output_html_file=DIFF_HTML_NAME):
        """ Generates the HTML difference of the two files
        :argument output_html_file: Path of the HTML diff file to generate.
        :return: None
        """
        comparison = difflib.HtmlDiff().make_file(self.base_file_content, self.qa_file_content)
        diff_report = self.open_file(output_html_file, self.WRITE_MODE)
        diff_report.write(comparison)


QA_INPUT_FILE_NAME = "qa_input.txt"
BASE_INPUT_FILE_NAME = "base_input.txt"

diff = DiffGenerator(QA_INPUT_FILE_NAME, BASE_INPUT_FILE_NAME)
diff.generate_txt_diff(output_match_file="match.txt", output_file_one="one.txt", output_file_two="two.txt")
diff.generate_html_diff(output_html_file="html.html")
