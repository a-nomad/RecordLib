"""
Classes representing expungment or sealing petitions. 

"""
from __future__ import annotations
from RecordLib.crecord import Case
from RecordLib.crecord import Attorney
from RecordLib.crecord import Person
from typing import Optional, List
from docxtpl import DocxTemplate
import io
from datetime import date


class Petition:
    @staticmethod
    def from_dict(self) -> None:
        """ Create a Petition from a dict """
        raise NotImplementedError

    def __init__(
        self,
        attorney: Optional[Attorney] = None,
        client: Optional[Person] = None,
        cases: Optional[List[Case]] = None,
        ifp_message: str = "",
        service_agencies: Optional[List[str]] = None,
        include_crim_hist_report: str = "",
    ) -> None:
        self.petition_type = "Generic Petition"
        self.attorney = attorney
        self.cases = cases or []
        self.client = client
        self.ifp_message = ifp_message
        self.service_agencies = service_agencies or []
        self.include_crim_hist_report = include_crim_hist_report
        self._template = None

    def set_template(self, template_file: io.BytesIO) -> None:
        """ Use set_template to pass a binary object to a Petitions that can then be stored as a docx template.
        """
        self._template = DocxTemplate(template_file)

    def add_case(self, case: Case) -> None:
        self.cases.append(case)

    def get_context(self) -> dict:
        """
        Return a dict to pass to render that describes the info in the petition.
        """
        if len(self.cases) > 0:
            disposition_list = ", ".join(
                [ch.disposition for ch in self.cases[0].charges]
            )
        else:
            disposition_list = ""
        return {
            "date": date.today().strftime(r"%B %d, %Y"),
            "attorney": self.attorney,
            "cases": self.cases,
            "client": self.client,
            "ifp_message": self.ifp_message,
            "service_agencies": self.service_agencies,
            "disposition_list": disposition_list,
        }

    def file_name(self) -> str:
        """
        Return a file name for the rendered petition.
        """
        try:
            docknum = self.cases[0].docket_number
        except:
            docknum = "NoCases"
        return f"{self.petition_type}_{self.client.last_name}_{docknum}.docx"

    def render(self) -> DocxTemplate:
        """
        Return the filled-in template document.
        """
        self._template.render(self.get_context())
        return self._template

    def __repr__(self):
        return f"Petition(Client: {self.client}, Cases: {[c for c in self.cases]}, Atty: {self.attorney})"


class Expungement(Petition):
    # class-level constants for the type of the expungment. FULL/Partial is only relevant to
    # helping the user understand what this expungement is.
    class ExpungementTypes:
        FULL_EXPUNGEMENT = "Full Expungement"
        PARTIAL_EXPUNGEMENT = "Partial Expungement"

    # Class constants for the section of the PA Criminal Procedure rules, pursuant to which this
    # expungement is being filed.
    # 490 is for expunging summary convictions,
    # 790 is for expunging everything else.
    class ExpungementProcedures:
        SUMMARY_EXPUNGEMENT = "§ 490"
        NONSUMMARY_EXPUNGEMENT = "§ 790"

    @staticmethod
    def from_dict(dct: dict) -> Expungement:
        dct.update(
            {
                "attorney": Attorney.from_dict(dct["attorney"])
                if dct.get("attorney")
                else Attorney(),
                "client": Person.from_dict(dct["client"]),
                "cases": [Case.from_dict(c) for c in dct["cases"]],
            }
        )
        return Expungement(**dct)

    def __init__(self, *args, **kwargs):

        if "petition_type" in kwargs.keys():
            kwargs.pop("petition_type")
        if "expungement_type" in kwargs.keys():
            self.expungement_type = kwargs["expungement_type"]
            kwargs.pop("expungement_type")
        else:
            self.expungement_type = ""

        if "procedure" in kwargs.keys():
            self.procedure = kwargs["procedure"]
            kwargs.pop("procedure")
        else:
            self.procedure = ""
        if "expungement_reasons" in kwargs.keys():
            # expungement_reasons is text for at the end of the 'reasons for expungement section of the petittion.
            # It may explain that the petition is for a person over 70 or for summary expungements.
            self.expungement_reasons = kwargs["expungement_reasons"]
            kwargs.pop("expungement_reasons")
        else:
            self.expungement_reasons = ""

        super().__init__(*args, **kwargs)
        self.petition_type = "Expungement"

    def get_context(self):
        """
        Get the dictionary of values we'll pass to the docx template file.

        Add any keys/values that aren't in the parent Petition class.
        """
        ctx = super().get_context()
        ctx.update(
            {
                "petition_type": "Expungement",
                "petition_procedure": self.procedure,
                "expungement_reasons": self.expungement_reasons,
            }
        )
        return ctx

    def __repr__(self):
        return f"{self.petition_type}({self.expungement_type}, Client: {self.client}, Cases: {[c for c in self.cases]}, Atty: {self.attorney})"


class Sealing(Petition):
    def __init__(self, *args, **kwargs):
        if "petition_type" in kwargs.keys():
            kwargs.pop("petition_type")
        super().__init__(*args, **kwargs)
        self.petition_type = "Sealing"

    def __repr__(self):
        return f"{self.petition_type}(Client: {self.client}, Cases: {[c for c in self.cases]}, Atty: {self.attorney})"

    @staticmethod
    def from_dict(dct: dict) -> Sealing:
        """ 
        Create a Sealing Petition from a dict with information about the petition we need to create.
        """
        dct.update(
            {
                "attorney": Attorney.from_dict(dct["attorney"])
                if dct.get("attorney")
                else Attorney(),
                "client": Person.from_dict(dct["client"]),
                "cases": [Case.from_dict(c) for c in dct["cases"]],
            }
        )
        return Sealing(**dct)

