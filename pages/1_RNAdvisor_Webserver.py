from typing import List

import streamlit as st
import os
import pandas as pd

from streamlit_molstar.auto import st_molstar_auto

from src_st.utils.align_helper import align_structures

from src_st.utils.utils_st import get_upload

from src_st.utils.utils_st import get_multiple_uploads
from src_st.viz.angles_helper import AnglesHelper
from src_st.viz.angles_per_model import AnglesPerModel

from src_st.viz.bar_helper import BarHelper
from src_st.viz.bar_helper_scoring import BarHelperScoring

from src_st.viz.polar_helper import PolarHelper

from src_st.viz.time_plot import TimePlot

from src_st.enums.enums import ALL_METRICS, CASP_PATH, CASP_CHALLENGES, RNA_PUZZLES_CHALLENGES

from src_st.enums.enums import QUICK_METRICS, TEXT_BY_FIGURES

from src_st.utils.rnadvisor_helper import run_rnadvisor

from src_st.enums.enums import ALL_SCORING_FUNCTIONS, QUICK_SCORING_FUNCTIONS


import numpy as np

def get_active_session():
    return np.random.randint(0, 100000)

def get_all_paths(session_number):
    prefix = os.path.join("data", "user", f"tmp_{session_number}")
    os.makedirs(prefix, exist_ok=True)
    for folder in ["aligned", "native", "preds", "output", "logs", "time"]:
        os.makedirs(os.path.join(prefix, folder), exist_ok=True)
    aligned_path = os.path.join(prefix, "aligned", "aligned.pdb")
    pred_dir = os.path.join(prefix, "preds")
    log_path = os.path.join(prefix, "logs", "log.csv")
    time_path = os.path.join(prefix, "time", "time.csv")
    out_path = os.path.join(prefix, "output", "out.csv")
    return aligned_path, pred_dir, log_path, time_path, out_path, prefix

def update_keys(n_keys: List):
    for n_key in n_keys:
        update_key(n_key)

def update_key(n_key):
    st.session_state[n_key] = not(st.session_state.get(n_key, False))

def on_change_native():
    update_key("native_to_show")

def on_change_preds():
    update_key("preds_to_show")


st.set_page_config(layout="wide",)
st.session_state["session_number"] = st.session_state.get("session_number", get_active_session())
aligned_path, pred_dir, log_path, time_path, out_path, prefix = get_all_paths(st.session_state.session_number)

print(f"Session number: {st.session_state['session_number']}")
KEYS_TO_ADD = ["native_to_show", "preds_to_show", "show_align", "show_results", ]
for key_to_add in KEYS_TO_ADD:
    if key_to_add not in st.session_state:
        st.session_state[key_to_add] = st.session_state.get(key_to_add, False)
st.session_state["method"] = st.session_state.get("method", "Metrics")
st.session_state["native_path"] = st.session_state.get("native_path", None)
st.session_state["pred_paths"] = st.session_state.get("pred_paths", None)
st.session_state["example_challenge"] = st.session_state.get("example_challenge", None)

def update_example():
    challenge, rna = st.session_state["example_challenge"]
    if rna is None:
        st.session_state.native_path = None
        st.session_state.pred_paths = None
        return None
    if challenge is not None:
        st.session_state.native_path = None
        st.session_state.pred_paths = None
        if st.session_state.method == "Metrics":
            native_dir = os.path.join("data", challenge, "NATIVE")
            c_native = os.path.join(native_dir, rna+".pdb")
            native_path = os.path.join(prefix,"native", rna+".pdb")
            os.system(f"cp -r {c_native} {native_path}")
            st.session_state.native_path = native_path
        else:
            st.session_state.native_path = None
        os.makedirs(pred_dir, exist_ok=True)
        true_pred_dir = os.path.join("data", challenge, "PREDS", rna)
        models = [name for name in os.listdir(true_pred_dir) if name.endswith(".pdb")]
        c_preds = [os.path.join(true_pred_dir, model) for model in models]
        os.system(f"rm -r {pred_dir}/*")
        new_command = "cp -r " + " ".join(c_preds) + f" {pred_dir}"
        os.system(new_command)
        st.session_state.pred_paths = [os.path.join(pred_dir, name) for name in os.listdir(pred_dir) if name.endswith(".pdb")]

def get_metric_examples():
    st.session_state["example_challenge"] = "CASP_RNA", "R1107"
    st.session_state["method"] = "Metrics"
    update_example()

def get_scoring_examples():
    st.session_state["example_challenge"] = "RNA_PUZZLES", "rp03"
    st.session_state["method"] = "Scoring functions"
    update_example()


def get_update_casp():
    st.session_state["example_challenge"] = "CASP_RNA", st.session_state["casp_choice"]
    st.session_state["rna_choice"] = None
    update_example()

def get_update_rna_puzzles():
    st.session_state["example_challenge"] = "RNA_PUZZLES", st.session_state["rna_choice"]
    st.session_state["casp_choice"] = None
    update_example()

def clean_files():
    all_keys = ["native_to_show", "preds_to_show", "show_align", "show_results"]
    for c_key in all_keys:
        st.session_state[c_key] = False
    st.session_state.native_path = None
    st.session_state.pred_paths = None
    st.session_state.example_challenge = None
    os.system(f"rm -r {pred_dir}/* {aligned_path} {log_path} {time_path} {out_path}")


def add_side_bar_examples():
    st.sidebar.write("# Load examples")
    st.sidebar.write("## Small examples")
    left_col, right_col = st.sidebar.columns(2)
    # Add Button
    metrics_btn = left_col.button(label="Metrics",
              on_click=get_metric_examples)
    scoring_btn = right_col.button(label="Scoring functions",
              on_click=get_scoring_examples)
    st.sidebar.write("## CASP-RNA")
    option = st.sidebar.selectbox(
        "Challenge",
        tuple(CASP_CHALLENGES),
        index=None,
        on_change= get_update_casp,
        key="casp_choice"
    )
    st.sidebar.write("# RNA-Puzzles")
    option = st.sidebar.selectbox(
        "Challenge",
        tuple(RNA_PUZZLES_CHALLENGES),
        index=None,
        on_change=get_update_rna_puzzles,
        key="rna_choice"
    )
    return None

add_side_bar_examples()

def return_gif_native_figures():
    left_col_native, right_col_preds = st.columns(2)
    left_col_native.image("img/gif/native_rp14b.gif")
    right_col_preds.image("img/gif/pred_rp14b.gif")

def get_uploads():
    native_path, pred_paths = st.session_state.native_path, st.session_state.pred_paths
    left_col, right_col = st.columns(2)
    left_col.write("### Native structure")
    right_col.write("### Predicted structures")
    left_col, right_col = st.columns(2)
    left_col.write("You can upload the native/reference structure.")
    right_col.write("You can upload the predicted structures.")
    if st.session_state.method == "Metrics":
        native_upload = left_col.file_uploader(
            "Upload Native structure (PDB or mmCIF Format)", accept_multiple_files=False,
            type=["pdb"], key="native", on_change=on_change_native,
        )
    else:
        native_upload = None
    pred_upload = right_col.file_uploader(
        "Upload predicted structure (PDB or mmCIF Format)", accept_multiple_files=True,
        type=["pdb"],
        key="preds", on_change=on_change_preds,
    )
    if native_upload:
        native_path = get_upload(native_upload, session_number=st.session_state.session_number)
    if pred_upload:
        pred_paths = get_multiple_uploads(pred_upload, session_number=st.session_state.session_number)
    left_col_struct, right_col_struct = st.columns(2)
    st.session_state.native_path = native_path
    st.session_state.pred_paths = pred_paths
    if native_path is not None and st.session_state.method == "Metrics":
        with left_col_struct:
            st_molstar_auto([st.session_state.native_path], key=f"structure_native_{st.session_state.native_path}")
    if pred_paths is not None:
        with right_col_struct:
            st_molstar_auto(st.session_state.pred_paths, key=f"structure_preds_{st.session_state.pred_paths}")

def get_metrics_scoring():
    metrics, scoring_functions = [], None
    st.markdown("### Quality assessment method")
    col1, col2, col3 = st.columns([5,6,5])
    method = col2.segmented_control(
        "",
        options=["Metrics", "Scoring functions"],
        selection_mode="single",
        key="method"
    )
    col1, col2, col3 = st.columns([3,6,3])
    if st.session_state.method == "Metrics":
        metrics = col2.multiselect(
            "Select Metrics to compute",
            ALL_METRICS,
            default=QUICK_METRICS,
            help="Select the metrics to compute.",
        )
    elif st.session_state.method == "Scoring functions":
        scoring_functions = col2.multiselect(
            "Select Scoring functions to compute",
            ALL_SCORING_FUNCTIONS,
            default=QUICK_SCORING_FUNCTIONS,
            help="Select the scoring function to compute.",
        )
        st.session_state["show_results"] = False
        st.session_state["native_path"] = None
    with st.expander("Optional parameters", expanded=False):
        normalisation = st.checkbox(
            "Normalize",
            help="Normalize the data to have a better visualisation.",
            key="normalize",
            value=True,
        )
        if st.session_state.method == "Metrics":
            st.write("LCS-TA threshold")
            col1, col2, col3 = st.columns([3, 6, 3])
            threshold = col2.slider(
                "Threshold",
                min_value=10,
                max_value=25,
                value=10,
                step=5,
                help="MCQ Threshold for the LCS-TA metric.",
                key="threshold",
            )
            st.write("MCQ method")
            col1, col2, col3 = st.columns([3, 6, 3])
            mcq_method = col2.selectbox(
                "MCQ method",
                ["Strict", "Moderate", "All"],
                help="MCQ method to use. Strict: no comparison if any violation is found. "
                     "Moderate: comparison without violations. "
                     "All: comparison regardless of the violations.",
                key="mcq_method",
                index=2,
            )
    return metrics, scoring_functions, normalisation


def get_condition_to_submit(native_path, pred_paths):
    condition = True
    if (st.session_state.method == "Scoring functions" and pred_paths is None):
        st.toast(
            "Could not compute scoring functions because there are no valid predicted structures.",
            icon="🚨")
        condition = False
    elif (st.session_state.method == "Scoring functions" and native_path is not None):
        st.toast(
            "Could not compute scoring functions because there is a native structure uploaded.",
            icon="🚨")
        condition = False
    elif (st.session_state.method == "Metrics" and (native_path is None or pred_paths is None)):
        st.toast(
            "Could not compute metrics because the native or predicted structures are not valid. ",
            icon="🚨")
        condition = False
    st.session_state["show_results"] = condition
    st.session_state["show_align"] = condition
    return condition


def get_submit_button():
    native_path, pred_paths = st.session_state.native_path, st.session_state.pred_paths
    col1, col2, _ = st.columns([1, 1, 5])
    submit = col1.button(label="Submit",
                       on_click=lambda: update_keys(["show_results", "show_align"]))
    if submit:
        clean_button = col2.button("Clear", on_click=lambda: clean_files())
        # Check if the native and predicted structures are uploaded
        condition = get_condition_to_submit(native_path, pred_paths)
        if not condition:
            return None
        with st.spinner("Computing metrics ... (may take up to a minute)"):
            if isinstance(native_path, str) and os.path.exists(native_path) and pred_paths is not None:
                align_structures(native_path, pred_paths, aligned_path)
                st.session_state.show_align = True
            st.session_state.show_results = True
            mcq_method = st.session_state.get("mcq_method", "All")
            mcq_to_params = {"Strict": 0, "Moderate": 1, "All": 2}
            hp_params = {"mcq_threshold": st.session_state.get("threshold", 10),
                         "mcq_mode": mcq_to_params.get(mcq_method)}
            run_rnadvisor(native_path, pred_dir, out_path, metrics, scoring_functions, time_path,
                          log_path, hp_params)
    return submit

st.markdown("## RNAdvisor Webserver")
st.markdown("---")
return_gif_native_figures()


get_uploads()

metrics, scoring_functions, normalisation = get_metrics_scoring()

submit = get_submit_button()

def get_conditions_show_results(native_path, pred_paths):
    if native_path is not None:
        condition_native = os.path.exists(native_path)
    else:
        condition_native = False
    if pred_paths is not None:
        condition_pred = any([os.path.exists(path) for path in pred_paths])
    else:
        condition_pred = False
    return condition_native or condition_pred

def is_only_scoring_functions(native_path, pred_paths):
    condition_pred = pred_paths is not None and any([os.path.exists(path) for path in pred_paths])
    if condition_pred and native_path is None and st.session_state.method == "Scoring functions":
        return True
    return False

condition_to_show = get_conditions_show_results(st.session_state.native_path, st.session_state.pred_paths)
is_only_scoring = is_only_scoring_functions(st.session_state.native_path, st.session_state.pred_paths)

if condition_to_show and st.session_state.show_align and st.session_state.show_results\
        and not is_only_scoring:
    st.write("---")
    st.write("## Aligned structures")
    st.write("Aligned structures using US-Align.")
    st_molstar_auto([aligned_path], key="aligned_structure")

if condition_to_show and st.session_state.show_results:
    try:
        df = pd.read_csv(out_path, index_col=0)
        df.index = df.index.map(lambda x: x.replace("normalized_", ""))
        st.write("## Results")
        st.write(TEXT_BY_FIGURES["Results"])
        st.dataframe(df)
        mapping_titles = {"TB-MCQ per position": "_tb_mcq.csv",
                          "TB-MCQ per angle": "_tb_mcq_per_angle.csv"}
        if is_only_scoring:
            fn_to_show = [BarHelperScoring]
            titles = ["Bar plot"]
            if "TB-MCQ" in df.columns:
                fn_to_show.extend([AnglesHelper, AnglesPerModel])
                titles.extend(["TB-MCQ per position", "TB-MCQ per angle"])
        else:
            fn_to_show = [BarHelper, PolarHelper]
            titles = ["Bar plot", "Polar plot"]
        for index, fn in enumerate(fn_to_show):
            if titles[index] in mapping_titles:
                c_out_path = out_path.replace(".csv", mapping_titles[titles[index]])
            else:
                c_out_path = out_path
            fig = fn.get_viz(c_out_path)
            st.write(f"## {titles[index]}")
            st.write(f"{TEXT_BY_FIGURES[titles[index]]}")
            st.plotly_chart(fig)
        fig_time = TimePlot.get_viz(time_path)
        st.write("## Time plot")
        st.write(f"{TEXT_BY_FIGURES['Time plot']}")
        st.plotly_chart(fig_time)
    except FileNotFoundError:
        st.session_state.show_results = False
