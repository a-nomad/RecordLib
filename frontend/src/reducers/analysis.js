/**
 * Add an Analysis returned from the server to the state.
 *
 * @param {*} state
 * @param {*} action
 */

import { ANALYZE_CRECORD_SUCCEEDED } from "frontend/src/actions/crecord";
import { ANALYZE_CRECORD_SUCCEDED } from "../actions/crecord";

export default function analysisReducer(state = {}, action) {
  switch (action.type) {
    case ANALYZE_CRECORD_SUCCEDED: {
      console.log("Analyzing record succeeded. We got back: ");
      console.log(action.payload);
      return action.payload;
    }
    default:
      return state;
  }
}
