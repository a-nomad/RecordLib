import React, { useEffect } from "react";
import { connect } from "react-redux";

import Attorney from "frontend/src/components/Attorney";
import EditAttorney from "frontend/src/components/EditAttorney";
import {
  editAttorney,
  toggleEditingAttorney,
  updateAttorney,
} from "frontend/src/actions";
import { fetchUserProfile } from "frontend/src/actions/user";
/**
 * Connected component for a Attorney, which can be in edit mode.
 * The editing prop determines the mode.
 * Props which are properties of the attorney are passed to a child
 * presentational component, which is either Attorney or EditAttorney.
 * Theses components also receive a dispatching function, which is used by the
 * EditAttorney component to send changes to the redux store.
 */
function AttorneyHolder(props) {
  const { attorney, user, fetchUserProfile, updateAttorney } = props;

  const populateAttorney = (user) => {
    console.log("populating attorney with:");
    const defaultAtty = {
      address: {
        line_one: user.default_atty_address_line_one,
        city_state_zip: user.default_atty_address_line_two,
      },
      full_name: user.default_atty_name,
      organization: user.default_atty_organization,
      organization_phone: user.default_atty_phone,
      bar_id: user.default_bar_id,
    };
    console.log(defaultAtty);
    updateAttorney(defaultAtty);
  };

  useEffect(() => {
    fetchUserProfile();
  }, []);

  useEffect(() => {
    if (!attorney.hasBeenEdited) {
      populateAttorney(user);
    }
  }, [user]);

  return (
    <div className="attorneyHolder">
      {!props.attorney.editing ? (
        <Attorney
          modifer={props.modifier}
          toggleEditing={props.toggleEditing}
          {...props.attorney}
        />
      ) : (
        <EditAttorney
          modifier={props.modifier}
          toggleEditing={props.toggleEditing}
          {...props.attorney}
        />
      )}
    </div>
  );
}

function mapStateToProps(state) {
  return { attorney: state.attorney, user: state.user };
}

/**
 * The modifier function takes a key,value pair
 * and associates the value with that key in the Attorney
 * object being edited.  It is used by the EditAttorney component.
 */
function mapDispatchToProps(dispatch, ownProps) {
  return {
    modifier: (key, value) => {
      dispatch(editAttorney(key, value));
    },
    toggleEditing: () => dispatch(toggleEditingAttorney()),
    fetchUserProfile: () => dispatch(fetchUserProfile()),
    updateAttorney: (update) => dispatch(updateAttorney(update)),
  };
}

const AttorneyHolderWrapper = connect(
  mapStateToProps,
  mapDispatchToProps
)(AttorneyHolder);
export default AttorneyHolderWrapper;
