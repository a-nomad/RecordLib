from RecordLib import ruledefs
from RecordLib.common import Sentence, SentenceLength
from datetime import date
import pytest
import types
import copy

def test_rule_expunge_over_70(example_crecord):
    example_crecord.person.date_of_birth = date(1920, 1, 1)
    example_crecord.cases[0].arrest_date = date(1970, 1, 1)
    example_crecord.cases[0].charges[0].sentences = [Sentence(
        sentence_date = date.today(),
        sentence_type = "Confinement",
        sentence_period = "90 days",
        sentence_length = SentenceLength(("90","day"), ("90","day"))
    )]
    modified_record, analysis = ruledefs.expunge_over_70(example_crecord)
    assert analysis["age_over_70_expungements"]["conclusion"] == "No expungements possible"
    assert analysis["age_over_70_expungements"]["conditions"]["years_since_final_release"] == False
    assert len(modified_record.cases) == len(example_crecord.cases)

    example_crecord.cases[0].charges[0].sentences[0] = Sentence(
        sentence_date = date(1980, 1, 1),
        sentence_type = "Confinement",
        sentence_period = "90 days",
        sentence_length = SentenceLength(("90","day"), ("90","day"))
    )
    modified_record, analysis = ruledefs.expunge_over_70(example_crecord)
    assert analysis["age_over_70_expungements"]["conclusion"] == "Expunge cases"
    analysis["age_over_70_expungements"]["conditions"]["years_since_final_release"] == True
    # The modified record has removed the cases this rule wants to expunge.
    assert len(modified_record.cases) < len(example_crecord.cases)


def test_expunge_deceased(example_crecord):
    example_crecord.person.date_of_death = None
    mod_rec, analysis = ruledefs.expunge_deceased(example_crecord)
    assert analysis["deceased_expungements"]["conclusion"] == "No expungements possible"
    assert analysis["deceased_expungements"]["conditions"]["deceased_three_years"] is False

    example_crecord.person.date_of_death = date(2000, 1, 1)
    mod_rec, analysis = ruledefs.expunge_deceased(example_crecord)
    assert analysis["deceased_expungements"]["conclusion"] == "Expunge cases"
    assert analysis["deceased_expungements"]["conditions"]["deceased_three_years"] is True


def test_expunge_summary_convictions(example_crecord, example_charge):
    # Old summary convictions are expungeable
    example_crecord.cases[0].charges[0].grade = "S"
    example_crecord.cases[0].arrest_date = date(2000, 1, 1)
    example_crecord.cases[0].disposition_date = date(2001, 1, 1)
    mod_rec, analysis = ruledefs.expunge_summary_convictions(example_crecord)
    assert analysis["summary_conviction_expungements"]["conclusion"] == "Expunge all cases"

    # no expunged summary convictions if there was a recent arrest.
    example_crecord.cases[0].arrest_date = date(2019, 1, 1)
    mod_rec, analysis = ruledefs.expunge_summary_convictions(example_crecord)
    assert analysis["summary_conviction_expungements"]["conclusion"] == "No expungements possible"

    # Only summary convictions, not other grades, can be expunged.
    new_charge = copy.deepcopy(example_charge)
    new_charge.grade = "M2"
    example_crecord.cases[0].arrest_date = date(2000, 1, 1)
    example_crecord.cases[0].charges.append(new_charge)
    assert len(example_crecord.cases[0].charges) == 2
    mod_rec, analysis = ruledefs.expunge_summary_convictions(example_crecord)
    assert analysis["summary_conviction_expungements"]["conclusion"] == "Expunge 1 charges in 1 cases"
    assert analysis["summary_conviction_expungements"]["expungements"][0]["charge"] == example_charge
