import axios from 'axios';

// Without declaring a BASE_URL, axios just calls to its own domain.
//const API_BASE_URL = 'http://localhost';

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

const client = axios.create({
        //baseURL: API_BASE_URL,
        headers: {
                'Content-Type': 'application/json',
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
        files.forEach((file) => data.append('files', file))

        return client.post(
                "/record/upload/", data, 
                {headers: {'Content-Type': 'multipart/form-data'}});
}

/**
 * POST a CRecord to the server and retrieve an analysis.
 */
export function analyzeCRecord(data) {
        data.person = data.defendant
        delete data.defendant
        return client.post(
                "/record/analyze/",
                data
        )
}


export function fetchPetitions(petitions, attorney) {
        petitions.forEach(p => p.attorney = attorney)
        return client.post(
                "/record/petitions/",
                {petitions: petitions}
        )
}

export function login(username, password) {
        const data = new FormData()
        data.append('username', username)
        data.append('password', password)
        client.post(
                "/accounts/login/",
                data,
                {headers: {'Content-Type': 'multipart/form-data'}},
        ).then(response => {
                window.location = "/"
                console.log(response)
        })
}