import React from "react";
import Paper from "@material-ui/core/Paper";
import Container from "@material-ui/core/Container";
import Typ from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Link from "@material-ui/core/Link";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3),
    "& p": {
      paddingTop: theme.spacing(3),
      paddingBottom: theme.spacing(5),
    },
  },
}));

const HelpPage = () => {
  const classes = useStyles();

  return (
    <Container>
      <Paper className={classes.root}>
        <Typ variant="h3">Help with Clean Slate Buddy</Typ>
        <Typ variant="body1">
          You can use Clean Slate Buddy for a few different workflows for
          analyzing or clearing records of arrests and convictions in
          Pennsylvania.
        </Typ>
        <Typ variant="h4">Drafting Petitions by Hand</Typ>
        <Typ variant="body1">To draft petitions by hand, you will</Typ>
        <ol>
          <li>
            Enter information about your client on the{" "}
            <Link target="_blank" href="/applicant">
              Applicant
            </Link>{" "}
            page. This information identifies the person you are drafting
            petitions for.
          </li>
          <li>
            Check the information on the <Link href="/attorney"> Attorney</Link>{" "}
            page is correct (this form defaults to information in your{" "}
            <Link href="/profile">user profile</Link>). The information on this
            form identifies the attorney responsible for the petitions you are
            generating.
          </li>
          <li>
            Enter information about cases you are sealing or expunging on the{" "}
            <Link href="/cases">Cases</Link> page. First enter the Docket
            Number, click "Add Case", and fill in the form that appears. Use the
            "Add Charge" button to add charges to the case.
          </li>
          <li>
            Create your petitions on the{" "}
            <Link href="/petitions">Petitions</Link> page.
          </li>{" "}
          Click the "New Petition" button and fill out missing information. Use
          the "Cases" dropdown to select the cases you'll include in each
          petition.
          <li>
            Finally, click "Process Petition Package" at the top of the page to
            download docx files of your petitions.
          </li>
        </ol>

        <Typ variant="h4">
          Drafting Petitions with an automated record search and a automated
          legal analysis
        </Typ>

        <Typ variant="body1">
          We can search the public UJS for a person's public records. Then we
          can use that information to automatically screen their record for
          expungeable and sealable charges.
        </Typ>
        <ol>
          <li>
            Enter information about your client on the{" "}
            <Link target="_blank" href="/applicant">
              Applicant
            </Link>{" "}
            page. This information identifies the person you are drafting
            petitions for.
          </li>
          <li>
            Click the "Search UJS" button to start a search for public records.
          </li>
          <li>
            Select the dockets and summary files you'd like to use for the
            analysis.
          </li>
          <li>
            Click the "Process Selected and Download Petitions" to use the files
            you've selected to generate petitions entirely automatically.
          </li>
          <li>Make sure you review these auto-drafted petitions!</li>
        </ol>
      </Paper>
    </Container>
  );
};

export default HelpPage;
