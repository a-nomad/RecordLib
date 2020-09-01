import React, { useState } from "react";
import { connect } from "react-redux";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import { searchUJSByName, uploadUJSDocs } from "../actions/ujs";
import { Redirect } from "react-router-dom";

import UJSSearchResultsContainer from "./UJSSearchResult";
import { analyzeCRecord } from "frontend/src/actions/crecord";

function NameSearch(props) {
  const {
    applicant,
    ujsSearchResults,
    searchUJSByName,
    uploadUJSDocs,
    analyzeCRecord,
  } = props;
  const missingSearchFields =
    applicant.first_name === "" || applicant.last_name === "";

  const [redirectTo, setRedirectTo] = useState(null);

  const searchClickHandler = () => {
    searchUJSByName(applicant);
  };

  const uploadUJSDocsClickHandler = (redirect_to) => {
    return () => {
      uploadUJSDocs().then(() => {
        setRedirectTo(redirect_to);
      });
    };
  };

  /**
   * User clicks the button to
   * (1) upload selected search results as Source Records
   * (2) update the crecord
   * (3) analyze the crecord for petitons
   * (4) go to the /petitions page.
   */
  const uploadUJSDocsAndDownloadPetitionsHandler = () => {
    uploadUJSDocs()
      .then(() => {
        console.log("then analyze crecord.");
        return analyzeCRecord();
      })
      .then(() => setRedirectTo("/petitions"))
      .catch((err) => {
        console.log("Error: " + err);
      });
  };

  const anySearchedCasesSelected =
    ujsSearchResults.casesFound.result.length > 0;

  if (redirectTo !== null) {
    return <Redirect to={redirectTo} />;
  }

  return (
    <div>
      <Typography variant="h4">Search UJS</Typography>
      <Grid
        container
        direction="row"
        alignItems="flex-start"
        alignContent="center"
        justify="space-around"
      >
        <Grid item xs={2}>
          <Button
            variant="contained"
            color="primary"
            disabled={missingSearchFields}
            onClick={searchClickHandler}
          >
            {" "}
            Search UJS{" "}
          </Button>
        </Grid>
        <Grid item xs={2}>
          <Button
            variant="contained"
            color="primary"
            disabled={!anySearchedCasesSelected}
            onClick={uploadUJSDocsClickHandler("/sourcerecords")}
          >
            Process selected and review or upload additional.
          </Button>
        </Grid>
        <Grid item xs={2}>
          <Button
            variant="contained"
            color="primary"
            disabled={!anySearchedCasesSelected}
            onClick={uploadUJSDocsClickHandler("/criminalrecord")}
          >
            Process selected and review applicant's full record.
          </Button>
        </Grid>
        <Grid item xs={2}>
          <Button
            variant="contained"
            color="primary"
            disabled={!anySearchedCasesSelected}
            onClick={uploadUJSDocsAndDownloadPetitionsHandler}
          >
            Process selected cases and download petitions.
          </Button>
        </Grid>
      </Grid>
      <Grid
        container
        direction="row"
        alignItems="center"
        alignContent="center"
        justify="space-around"
      >
        {<UJSSearchResultsContainer results={ujsSearchResults} />}
      </Grid>
    </div>
  );
}

function mapStateToProps(state) {
  return {
    applicant: state.applicantInfo.applicant,
    ujsSearchResults: state.ujsSearchResults,
    crecord: state.crecord,
  };
}

function mapDispatchToProps(dispatch, ownprops) {
  return {
    searchUJSByName: (applicant) => {
      return dispatch(
        searchUJSByName(
          applicant.first_name,
          applicant.last_name,
          applicant.date_of_birth
        )
      );
    },
    uploadUJSDocs: () => {
      return dispatch(uploadUJSDocs());
    },
    analyzeCRecord: () => {
      return dispatch(analyzeCRecord());
    },
  };
}

const NameSearchWrapper = connect(
  mapStateToProps,
  mapDispatchToProps
)(NameSearch);

export default NameSearchWrapper;
