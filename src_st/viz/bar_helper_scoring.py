import os
from typing import List

import numpy as np

from src_st.enums.enums import NEGATIVE_ENERGY, SUB_SCORING, COLORS_MAPPING_SCORING
from src_st.viz.bar_helper import BarHelper
import plotly.express as px
from src_st.utils.utils import update_bar_plot
from sklearn.preprocessing import MinMaxScaler


class BarHelperScoring(BarHelper):
    def __init__(self, *args, **kwargs):
        super(BarHelperScoring, self).__init__(*args, **kwargs)

    def normalize_metrics(self, df, desc_metrics: List = NEGATIVE_ENERGY):
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
        df = df.rename(columns={"Metric": "Scoring function"})
        df = df[df["Scoring function"].isin(SUB_SCORING)]
        df = (
            df[["Scoring function", "Model", "Value", "Value (normalised)"]]
            .groupby(["Model", "Scoring function"])
            .mean()
            .reset_index()
        )
        fig = px.bar(
            df,
            y="Model",
            x="Value (normalised)",
            color="Scoring function",
            color_discrete_map=COLORS_MAPPING_SCORING,
            orientation="h",
            category_orders={
                "Metric": list(COLORS_MAPPING_SCORING.keys()),
            },
            labels={"Metric (value)": "Normalized scoring function"},
            hover_data=["Value"],
        )
        fig = update_bar_plot(fig)
        return fig

    @staticmethod
    def get_viz(in_path):
        bar_helper = BarHelperScoring(in_path)
        return bar_helper.viz()


if __name__ == "__main__":
    in_path = os.path.join("data", "user", "tmp_23373", "output", "out.csv")
    bar_helper = BarHelperScoring(in_path)
    bar_helper.viz()
