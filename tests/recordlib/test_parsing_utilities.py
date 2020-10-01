import logging
from RecordLib.sourcerecords.parsingutilities import word_starting_near, map_line

logger = logging.getLogger(__name__)


def test_word_starting_near():
    line = "   The word      is pizza"
    assert (word_starting_near(4, line)) == "The word"
    assert (word_starting_near(18, line)) == "is pizza"


def test_map_line():
    col_dict = {
        "A": 0,
        "B": 20,
    }
    line = "Joe                 Smith"
    assert map_line(line, col_dict) == {
        "A": "Joe",
        "B": "Smith",
    }
