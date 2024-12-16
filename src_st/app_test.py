import streamlit as st
from enums.enums import ALL_METRICS
from enums.enums import ALL_SCORING_FUNCTIONS, QUICK_SCORING_FUNCTIONS

from enums.enums import QUICK_METRICS


def get_scoring_examples():
    pass
    return None, pred_paths


def get_metric_examples():
    pass


def update_key(n_key):
    st.session_state[n_key] = not (st.session_state.get(n_key, False))


def add_side_bar_examples():
    st.sidebar.write("# Load examples")
    st.sidebar.write("## Small examples")
    left_col, right_col = st.sidebar.columns(2)
    metrics_btn = left_col.button(label="Metrics", on_click=get_metric_examples)
    scoring_btn = right_col.button(
        label="Scoring functions", on_click=get_scoring_examples
    )
    st.sidebar.write("## CASP-RNA")
    with st.sidebar.expander("Load examples", expanded=False):
        st.write("Load example from CASP-RNA competition")
        option = st.selectbox("Challenge", tuple(["rp01", "rp03"]), index=None)
    st.sidebar.write("# RNA-Puzzles")
    return option


def change_button():
    # print(f"SHOW BEFORE {st.session_state.show_metrics}")
    st.session_state.method = "Metrics"
    # print(f"SHOW AFTER {st.session_state.show_metrics}")


def get_metrics_scoring():
    button = st.button(
        "Test button",
    )
    if button:
        change_button()
    # print(f"SHOW SELECTED {st.session_state.show_metrics}")
    selected = "Metrics" if st.session_state.show_metrics else "Scoring functions"
    print(f"SELECTED : {selected}")
    method = st.segmented_control(
        "Quality assessment method",
        options=["Metrics", "Scoring functions"],
        selection_mode="single",
        default=selected,
        key="method",
    )
    metrics, scoring_functions = [], None
    # left_col, right_col = st.columns(2)
    if st.session_state.method == "Metrics":
        metrics = st.multiselect(
            "Select Metrics to compute",
            ALL_METRICS,
            default=QUICK_METRICS,
            help="Select the metrics to compute.",
        )
    elif st.session_state.method == "Scoring functions":
        scoring_functions = st.multiselect(
            "Select Scoring functions to compute",
            ALL_SCORING_FUNCTIONS,
            default=QUICK_SCORING_FUNCTIONS,
            help="Select the scoring function to compute.",
        )
    with st.expander("Optional parameters", expanded=False):
        normalisation = st.checkbox(
            "Normalize",
            help="Normalize the data to have a better visualisation.",
            key="normalize",
            value=True,
        )
    return metrics, scoring_functions, normalisation


KEYS_TO_ADD = ["show_metrics"]
for key_to_add in KEYS_TO_ADD:
    if key_to_add not in st.session_state:
        st.session_state[key_to_add] = st.session_state.get(key_to_add, True)


# options = add_side_bar_examples()
metrics, scoring_functions, normalisation = get_metrics_scoring()
