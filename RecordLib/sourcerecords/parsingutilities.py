from typing import Union, BinaryIO, Optional, Tuple, List
import os
import re
import tempfile
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


def get_text_from_pdf(pdf: Union[BinaryIO, str]) -> str:
    """
    Function which extracts the text from a pdf document.
    Args:
        pdf:  Either a file object or the location of a pdf document.
        tempdir:  Place to store intermediate files.


    Returns:
        The extracted text of the pdf.
    """
    with tempfile.TemporaryDirectory() as out_dir:
        if hasattr(pdf, "read"):
            # the pdf attribute is a file object,
            # and we need to write it out, for pdftotext to use it.
            pdf_path = os.path.join(out_dir, "tmp.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf.read())
        else:
            pdf_path = pdf
        # TODO - remove the option of making tempdir anything other than a tempfile.
        #        Only doing it this way to avoid breaking old tests that send tempdir.
        # out_path = os.path.join(tempdir, "tmp.txt")
        out_path = os.path.join(out_dir, "tmp.txt")
        os.system(f'pdftotext -layout -enc "UTF-8" { pdf_path } { out_path }')
        try:
            with open(os.path.join(out_dir, "tmp.txt"), "r", encoding="utf8") as f:
                text = f.read()
                return text
        except IOError as e:
            logger.error("Cannot extract pdf text..")
            return ""


def date_or_none(date_text: str, fmtstr: str = r"%m/%d/%Y") -> datetime:
    """
    Return date or None given a string.
    """
    try:
        return datetime.strptime(date_text.strip(), fmtstr).date()
    except (ValueError, AttributeError):
        return None


def money_or_none(money_str: str) -> Optional[float]:
    try:
        return float(money_str.strip().replace(",", ""))
    except:
        return None


def word_starting_near(val: int, line: str, leading=1, trailing=1) -> Optional[str]:
    """
    Return the words starting near the index `val` in `line`. 
    There's a tolerance for error from `-leading` to `trailing`.

    Args:
        val(int): Integer of the column we're looking to fine the value of.
        line(str): The line of columnar text we're deconstructing
        leading(int): If columns don't quite line up, how many spaces before val are we willing to look? 
        trailing(int): If cols don't line up, how many spaces after val will we look for some text?

    Returns:
        Words in the right part of the line, or None.

    Example:
        line = "   The word      is pizza"
        assert(word_starting_near(4,line)) == "The word"
        assert(word_starting_near(18,line)) == "is pizza"
    """
    word_pattern = re.compile(r"^\s{0," + str(trailing) + r"}(\S+\s{0,2})*")
    start_with_index = val - leading if val > leading else 0
    match = word_pattern.search(line[start_with_index:])
    if match is None:
        return None
    else:
        return match.group(0).strip()


def map_line(line: str, col_dict: dict) -> dict:
    """
    Map a line of columnar data to the columns described in col_dict.

    Example: 
    col_dict = {
        'A': {'idx': 0, 'fmt': None},
        'B': {'idx': 20, 'fmt': int}
    }
    line = "Joe                 4"
    map_line(line, col_dict) == {
        'A': 'Joe',
        'B': 4,
    }
    """

    mapped = dict()
    for key, val in col_dict.items():
        extracted_value = word_starting_near(val["idx"], line)
        if val["fmt"]:
            try:
                extracted_value = val["fmt"](extracted_value)
            except:
                pass
        mapped[key] = extracted_value

    return mapped


def find_index_for_pattern(pattern, txt) -> Optional[int]:
    """
    Return the position in `txt` of the pattern `pattern`,
    or None if the pattern isn't found.
    """
    patt = re.compile(pattern)
    try:
        return next(patt.finditer(txt)).start()
    except StopIteration:
        return None


def find_pattern(label, pattern, txt, flags=None) -> Tuple[str, List[str]]:
    """
    Find a pattern in the text `txt`. If its not present, return an error message 
    describing the missing value with `label`. 
    """
    if flags is not None:
        search = re.search(pattern, txt, flags)
    else:
        search = re.search(pattern, txt)
    if search is not None:
        return search, []
    else:
        return None, [f"Could not find {label}"]

