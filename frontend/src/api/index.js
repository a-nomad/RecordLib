import axios from "axios";

// Without declaring a BASE_URL, axios just calls to its own domain.
//const API_BASE_URL = 'http://localhost';

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

/**
 * Utility to remove keys with `null` values from objects sent to the
 * api.
 *
 * So if an object has null keys in the ui, let the server handle defaults,
 * rather than sending null.
 * @param {} object
 */
export function removeNullValues(object) {
  Object.keys(object).forEach((key) => {
    if (!object[key]) {
      delete object[key];
    } else if (typeof object[key] == "object") {
      object[key] = removeNullValues(object[key]);
    }
  });
  return object;
}

const client = axios.create({
  //baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  maxRedirects: 5,
});

/**
 * function to post record files (currently only pdfs) to the server
 * @param  {Object} files - uploaded Summary and docket pdf files
 * @return {Object} a promise
 */
export function uploadRecords(files) {
  const data = new FormData();
  files.forEach((file) => data.append("files", file));

  return client.post("/api/record/sourcerecords/upload/", data, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}

/**
 * POST a CRecord to the server and retrieve an analysis.
 */
export function analyzeCRecord(data) {
  return client.post("/api/record/analysis/", removeNullValues(data));
}

export function fetchPetitions(petitions) {
  // Send a POST to transform a set of petitions into
  // rendered petition files, and return the generated files
  // in a zip file.

  const config = {
    responseType: "blob",
  };

  return client.post(
    "/api/record/petitions/",
    { petitions: petitions.map((p) => removeNullValues(p)) },
    config
  );
}

export function login(username, password) {
  const data = new FormData();
  data.append("username", username);
  data.append("password", password);
  return client
    .post("/api/accounts/login/", data, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((response) => {
      return new Promise((resolve, reject) => {
        if (response.data.includes("didn't match")) {
          return reject("Login failed. Try again.");
        } else {
          return resolve("Login succeeded.");
        }
      });
    });
}

export function logout() {
  client.get("/api/accounts/logout/").then(() => {
    window.location = "/";
  });
}

export function fetchUserProfileData() {
  return client.get("/api/record/profile/"); // TODO thats a bad api endpoint for a user profile.
}
/**
 * PUT current user profile to the server to update it.
 * @param {*} user
 */
export function saveUserProfile(user) {
  console.log("posting profile");
  console.log(user);
  return client.put("/api/record/profile/", user);
}

export function searchUJSByName(first_name, last_name, date_of_birth) {
  return client.post("/api/ujs/search/name/", {
    first_name: first_name,
    last_name: last_name,
    dob: date_of_birth,
  });
}

export function uploadUJSDocs(source_records) {
  return client.post("/api/record/sourcerecords/fetch/", {
    source_records: source_records,
  });
}

export function integrateDocsWithRecord(crecord, sourceRecords) {
  console.log("integrateDocsWithRecord action creator");
  return client.put("/api/record/cases/", {
    crecord: removeNullValues(crecord),
    source_records: removeNullValues(sourceRecords),
  });
}

export function guessGrade(offense, statuteComponents) {
  return client.get("/api/grades/guess/", {
    params: { offense, ...statuteComponents },
  });
}
