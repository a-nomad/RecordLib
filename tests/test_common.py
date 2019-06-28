from RecordLib.common import *
from dataclasses import asdict
from datetime import date, timedelta
import pytest

def test_person():
    per = Person("John", "Smeth", date(2010, 1, 1))
    assert per.first_name == "John"
    assert per.last_name == "Smeth"

def test_person_age():
    per = Person("John", "Smeth", date(2000, 1, 1))
    assert per.age() > 17

def test_person_todict():
    per = Person("John", "Smeth", date(2010, 1, 1))
    assert asdict(per) == {
        "first_name": "John",
        "last_name": "Smeth",
        "date_of_birth": date(2010, 1, 1)
    }

def test_sentence():
    st = Sentence(
        sentence_date=date(2010, 1, 1),
        sentence_type="Probation",
        sentence_period="90 days",
        sentence_length=SentenceLength(
            min_time=("90","Day"),
            max_time=("90","Day")
        )
    )
    assert st.sentence_complete_date() == date(2010, 1, 1) + timedelta(days=90)

def test_calculate_days():
    assert SentenceLength.calculate_days("40", "Day(s)").days == 40
    assert SentenceLength.calculate_days("3 ", "Month(s)").days == 91
    assert SentenceLength.calculate_days(" 1", "Year(s)").days == 365
    assert SentenceLength.calculate_days(" Other", "Values") is None

def test_SentenceLength():
    lng = SentenceLength(
        min_time=("30", " Day(s)"),
        max_time=("1", "Year(s)")
    )
    assert lng.max_time.days==365
    assert lng.min_time.days==30

def test_charge():
    char = Charge(
        offense="Eating w/ mouth open",
        grade="M2",
        statute="24 &sect; 102",
        disposition="Guilty Plea",
        sentences=[])
    assert char.offense == "Eating w/ mouth open"
    assert char.grade == "M2"
    assert char.disposition == "Guilty Plea"
