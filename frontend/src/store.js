import { createStore } from "redux";

const initialState = {
  formData: {
    hcp_name: "",
    date: "",
    time: "",
    sentiment: "",
    materials: "",
    topics: ""
  }
};

function reducer(state = initialState, action) {
  switch (action.type) {
    case "UPDATE_FORM":
      return {
        ...state,
        formData: {
          ...state.formData,
          ...action.payload
        }
      };
    default:
      return state;
  }
}

const store = createStore(reducer);

export default store;