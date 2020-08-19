import {
  FETCH_USER_PROFILE_SUCCEEDED,
  UPDATE_USER_PROFILE,
} from "../actions/user";

const initialState = {
  username: document.getElementById("username").textContent,
};

export default function userReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_USER_PROFILE_SUCCEEDED:
      const newState = Object.assign(
        {},
        state,
        { ...action.payload.user },
        { ...action.payload.profile }
      );
      return newState;
    case UPDATE_USER_PROFILE: {
      return Object.assign({}, state, action.payload);
    }
    default: {
      return state;
    }
  }
}
