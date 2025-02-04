from typing import List, Dict

import streamlit as st
import pandas as pd

from src_st.tb_helper.tb_mcq import TBMCQ
import os

from src_st.utils.utils import convert_cif_to_pdb
from src.rnadvisor_cli import ScoreCLI

os.environ["TOKENIZERS_PARALLELISM"] = "false"

rnadvisor_args = {
    "pred_path": None,
    "native_path": None,
    "result_path": None,
    "all_scores": None,
    "time_path": None,
    "log_path": None,
}


@st.cache_data
def run_rnadvisor(
    native_path,
    pred_path,
    out_path,
    metrics,
    scoring_functions,
    time_path,
    log_path,
    hp_params,
):
    str_metrics = ",".join(metrics) if len(metrics) > 0 else ""
    to_compute_tb = (
        "TB-MCQ" in scoring_functions if scoring_functions is not None else False
    )
    if scoring_functions is not None:
        scoring_functions = [
            score_fn for score_fn in scoring_functions if score_fn not in metrics
        ]
        str_metrics += "," + ",".join(scoring_functions)
        str_metrics = str_metrics.replace("TB-MCQ", "")  # TB-MCQ is computed separately
    if native_path is None and pred_path is not None:
        native_path = os.path.join(pred_path, os.listdir(pred_path)[0])
    rnadvisor_args["pred_path"] = pred_path
    rnadvisor_args["native_path"] = native_path
    rnadvisor_args["result_path"] = out_path
    rnadvisor_args["all_scores"] = ScoreCLI.convert_cli_scores(str_metrics)
    rnadvisor_args["time_path"] = time_path
    rnadvisor_args["log_path"] = log_path
    rnadvisor_args["hp_params"] = hp_params
    score_cli = ScoreCLI(**rnadvisor_args)
    score_cli.compute_scores()
    if to_compute_tb:
        out_path_mcq = out_path.replace(".csv", "_tb_mcq.csv")
        compute_tb_mcq_per_sequence(pred_path, out_path_mcq, time_path)
    clean_df(out_path, scoring_functions)


def clean_df(in_df: str, scoring_functions: List):
    """
    Clean the dataframe by removing unwanted names and columns
    """
    df = pd.read_csv(in_df, index_col=0)
    df.index = df.index.map(lambda x: x.replace("normalized_", ""))
    if scoring_functions is not None:
        try:
            df = df.drop(["BARNABA-RMSD", "BARNABA-eRMSD"], axis=1)
        except KeyError:
            pass
    df.to_csv(in_df)


def convert_preds_cif_to_pdb(pred_paths: List[str]) -> List[str]:
    """
    Convert .cif to .pdb
    :param pred_paths:
    :return:
    """
    new_preds = []
    for pred in pred_paths:
        if pred.endswith(".cif"):
            new_path = pred.replace(".cif", "pdb")
            convert_cif_to_pdb(pred, new_path)
        else:
            new_path = pred
        new_preds.append(new_path)
    return new_preds


def add_tb_mcq_to_df(tb_mcq: Dict, in_path: str):
    """
    Add the TB-MCQ to the dataframe
    """
    df = pd.read_csv(in_path, index_col=0)
    df_tb = pd.DataFrame({"TB-MCQ": tb_mcq.values()}, index=tb_mcq.keys())
    # Clean names
    if "normalized_" in df.index[0]:
        df_tb.index = df_tb.index.map(lambda x: f"normalized_{x}")
    new_df = pd.concat([df, df_tb], axis=1)
    new_df.to_csv(in_path)


def compute_tb_mcq_per_sequence(pred_path: str, out_path: str, time_path):
    """
    Compute the TB-MCQ per sequence
    :param pred_path: path to a predicted structure
    :param out_path: path where to save the predicted error
    :param time_path: path where to save the time
    """
    if os.path.isdir(pred_path):
        pred_files = [
            os.path.join(pred_path, name)
            for name in os.listdir(pred_path)
            if name.endswith(".pdb") or name.endswith(".cif")
        ]
    elif os.path.isfile(pred_path):
        pred_files = pred_path
    pred_files = convert_preds_cif_to_pdb(pred_files)
    df, df_angle, tb_mcq, c_time = TBMCQ.get_tb_mcq_all(pred_files)
    df.to_csv(out_path, index=False)
    df_angle.to_csv(out_path.replace(".csv", "_per_angle.csv"))
    add_tb_mcq_to_df(tb_mcq, out_path.replace("_tb_mcq", ""))
    add_tb_mcq_to_df(c_time, time_path)
