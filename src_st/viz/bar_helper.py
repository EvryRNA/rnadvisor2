import os
from typing import List
import numpy as np

import plotly.express as px

from sklearn.preprocessing import MinMaxScaler

from src_st.enums.enums import COLORS_MAPPING, DESC_METRICS, SUB_METRICS
from src_st.utils.utils import update_bar_plot

from src_st.viz.polar_helper import PolarHelper


class BarHelper:
    def __init__(self, in_path: str):
        self.df = PolarHelper.read_df(in_path)

    def normalize_metrics(self, df, desc_metrics: List = DESC_METRICS):
        metrics = df["Metric"].unique()
        df["Value (normalised)"] = [np.nan] * df.shape[0]
        for metric in metrics:
            mask = df["Metric"] == metric
            metric_values = df.loc[mask, "Value"].values.reshape(-1, 1)
            if metric_values.shape[0] == 0:
                continue
            non_nan_metrics = metric_values[~np.isnan(metric_values)].reshape(-1, 1)
            if len(non_nan_metrics) == 0:
                continue
            scaler = MinMaxScaler().fit(X=non_nan_metrics)
            norm_metric = scaler.transform(X=metric_values).reshape(-1).tolist()
            if metric in desc_metrics:
                norm_metric = [x if np.isnan(x) else 1 - x for x in norm_metric]
            df.loc[mask, "Value (normalised)"] = norm_metric
        return df

    def viz(self):
        """Plot the polar distribution for a dataset."""
        df = self.normalize_metrics(self.df)
        # df = df[~df["Metric"].isin(METRICS_TO_HIDE)]
        df = df[df["Metric"].isin(SUB_METRICS)]
        df = (
            df[["Metric", "Model", "Value", "Value (normalised)"]]
            .groupby(["Model", "Metric"])
            .mean()
            .reset_index()
        )
        fig = px.bar(
            df,
            y="Model",
            x="Value (normalised)",
            color="Metric",
            color_discrete_map=COLORS_MAPPING,
            orientation="h",
            category_orders={
                "Metric": list(COLORS_MAPPING.keys()),
            },
            labels={"Metric (value)": "Normalized metrics"},
            range_x=[0, 9],
            hover_data=["Value"],
        )
        fig = update_bar_plot(fig)
        return fig

    @staticmethod
    def get_viz(in_path):
        bar_helper = BarHelper(in_path)
        return bar_helper.viz()


if __name__ == "__main__":
    in_path = os.path.join("data", "output", "R1107.csv")
    bar_helper = BarHelper(in_path)
    bar_helper.viz()
