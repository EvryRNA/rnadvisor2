import streamlit as st
from src_st.viz.bar_helper import BarHelper
from src_st.viz.angles_helper import AnglesHelper
from src_st.viz.bar_helper_scoring import BarHelperScoring
from src_st.viz.angles_per_model import AnglesPerModel
from src_st.viz.polar_helper import PolarHelper
from src_st.viz.time_plot import TimePlot
import pandas as pd
import os

def read_csv(df):
    df.index = df.index.map(lambda x: x.replace("normalized_", ""))
    st.dataframe(df)


def help_page():
    prefix = "data/example"
    all_paths = [os.path.join(prefix, name+".csv") for name in ["out_metrics", "out_sf", "out_tb_mcq_sf", "out_tb_mcq_per_angle_sf",
                                               "time_metrics", "time_sf"]]
    df_metrics, df_sf = pd.read_csv(all_paths[0], index_col=0), pd.read_csv(all_paths[1], index_col=0)
    st.set_page_config(
        layout="wide",
    )
    st.markdown(
        """
        ### Help
        If you have any questions or need help with the *RNAdvisor* tool, please contact us at 
        [guillaume.postic@universite-paris-saclay.fr](guillaume.postic@universite-paris-saclay.fr) or [fariza.tahi@univ-evry.fr](fariza.tahi@univ-evry.fr).
        """
    )
    st.markdown("---")
    st.markdown("""
    
        ## How to use RNAdvisor 2
        
        RNAdvisor 2 is an updated version of the [RNAdvisor](https://github.com/EvryRNA/rnadvisor) tool with an interface available.
        The tool is designed to compute the quality of RNA 3D structures. It computes a variety of metrics and scoring functions.
        
        There are two main modes available: the **metric** mode and the **scoring function** mode:
        
        - The **metric** mode computes a variety of metrics for the input structures compared to a true reference structure.
        - The **scoring function** mode computes the RNA structural quality without the need for a reference structure.
        
        ### Inputs
        
        The user can choose to select one reference structure and multiple predicted structures. 
        The reference structure is the native structure of the RNA molecule. 
        The predicted structures are the molecules to evaluate the quality of.
        The user can input either a `.pdb` file or a `.cif` file. """)
    st.image("img/help/main_website_0.png")
    st.markdown("""
        Then, the user has to select the mode to use: **metric** or **scoring function**.
        """)
    st.image("img/help/metrics_selection.png")
    st.markdown("""
        It can then submit the input to the tool, and the results will be displayed. """)
    st.image("img/help/submission.png")
    st.markdown("""
        The user can reset the current state to do other computations with the clear button.""")
    st.image("img/help/clear.png")
    st.markdown("""---""")
    st.markdown("""
        ## Metrics computation
        In the **metric** mode, the user can select around ten metrics. 
        Default metrics are selected for their quick computation and efficiency.""")
    st.image("img/help/quick_metrics.png")
    st.markdown("""
      The user can select among other available metrics. 
    """)
    st.image("img/help/all_metrics.png")
    st.markdown("""
        The user can then select the hyperparameters for different metrics. 
        - **Normalize**: whether to normalize the structures or not, using the normalisation by [RNA-tools](https://github.com/mmagnus/rna-tools). 
        - **LCS-TA**: the threshold to use for the Longest Common Subsequence (LCS) algorithm. Choice is between 10, 15, 20 and 25° for the MCQ threshold. 
        - **MCQ**: the mode to use for the computation of the MCQ. Choice is between 
        `Strict` (no computation if any violation is found), `Relaxed` (computation only on non violation parts) and `All` 
        (computation regardless any violation).""")
    st.image("img/help/hp.png")
    st.markdown("""
        ### Outputs and visualisation
        Once the user has selected the metrics and hyperparameters, the tool will compute the metrics for each predicted structure.
        Different visualisations are available. 
        - **Output dataframe**: the user can download the dataframe with the computed metrics for each predicted structure. A button is available to download the dataframe on the upper right.""")
    st.image("img/help/df.png")
    st.markdown("""An example is shown below: """)
    read_csv(df_metrics)
    st.markdown("""
        - **Bar plot**: normalised scores for each metric considered. 
            The higher the score, the better the model. The scores are normalised to be between 0 and 1, where 1 is the best 
            and 0 the worst. The decreasing scores are reversed to be increasing. 
            The goal is to give a quick overview of which method seems the best in terms of the selected metrics.""")
    st.image("img/help/bar_plot_metrics.png")
    st.markdown("""An example of the plot is shown below:""")
    st.plotly_chart(BarHelper.get_viz(all_paths[0]))
    st.markdown("""
        - **Polar plot**: INF metrics for three types of interactions: Watson-Crick, Non-Watson-Crick and Stacking interactions.
      """)
    st.image("img/help/polar_plot_metrics.png")
    st.markdown("""An example of the plot is shown below:""")
    st.plotly_chart(PolarHelper.get_viz(all_paths[0]))
    st.markdown("""
        - **Time plot**: time taken to compute the score for all the models.""")
    st.image("img/help/time_plot_metrics.png")
    st.markdown("""An example of the plot is shown below:""")
    st.plotly_chart(TimePlot.get_viz(all_paths[-2]))
    st.markdown("""---""")
    st.markdown("""
        ## Scoring functions computation
        In the **scoring function** mode, the user can select among six existing scoring functions. 
    """)
    st.image("img/help/scoring_functions.png")
    st.markdown("""
        Once the scoring functions are selected, the user can submit the input to the tool.
        
        ### Outputs and visualisation
        Once the user has selected the metrics and hyperparameters, the tool will compute the different scoring functions.
        Different visualisations are available. 
        - **Output dataframe**: the user can download the dataframe with the computed scoring functions for each predicted structure.""")
    st.image("img/help/df_sf.png")
    st.markdown("""An example of the plot is shown below:""")
    read_csv(df_sf)
    st.markdown("""
        - **Bar plot**: normalised scores for each metric considered. 
            The higher the score, the better the model. The scores are normalised to be between 0 and 1, where 1 is the best 
            and 0 the worst. The decreasing scores are reversed to be increasing. 
            The goal is to give a quick overview of which method seems the best in terms of the selected scoring functions.""")
    st.image("img/help/bar_plot_sf.png")
    st.markdown("""An example of the plot is shown below:""")
    st.plotly_chart(BarHelperScoring.get_viz(all_paths[1]))
    st.markdown("""
        - **TB-MCQ per position**: this plot shows the TB-MCQ (scoring function that reproduces the MCQ metric) value for each 
        position of the sequence for each model. It reproduces MCQ visualisations (inspired by [RNAtango](https://rnatango.cs.put.poznan.pl/)),
        with an estimation of the MCQ but without any reference structure.""")
    st.image("img/help/tb_mcq_position.png")
    st.markdown("""An example of the plot is shown below:""")
    st.plotly_chart(AnglesHelper.get_viz(all_paths[2]))
    st.markdown("""
        - **TB-MCQ per angle**: this plot shows the TB-MCQ value for each angle for each model. The lower the MCQ value, the better the model.
        """)
    st.image("img/help/tb_mcq_angle.png")
    st.markdown("""An example of the plot is shown below:""")
    st.plotly_chart(AnglesPerModel.get_viz(all_paths[3]))
    st.markdown("""
        - **Time plot**: time taken to compute the score for all the models.""")
    st.image("img/help/time_plot_sf.png")
    st.markdown("""An example of the plot is shown below:""")
    st.plotly_chart(TimePlot.get_viz(all_paths[-1]))
    st.markdown("""---""")
    st.markdown("""
        ## Loaded examples
        
        Different examples are available for the user: **metrics**, **scoring functions** and specific examples from 
        [RNA-Puzzles](https://www.rnapuzzles.org/) and [CASP-RNA](https://predictioncenter.org/index.cgi). 
        Predicted structures are from our [work](https://www.biorxiv.org/content/10.1101/2024.06.13.598780v2), where a dozens of 
        predictive models are available for each RNA structure of either RNA-Puzzles or CASP-RNA. """)
    st.image("img/help/examples.png")
    st.markdown("""
        - **Metrics**: the user can select the **Metrics** example where one reference structure and multiple predicted structures are available.
        - **Scoring functions**: the user can select the **Scoring functions** example where one reference structure and multiple predicted structures are available.
        - **RNA-Puzzles**: the user can select the **RNA-Puzzles** example where one reference structure and multiple predicted structures are available. 
        """)
    st.image("img/help/rna_puzzles.png")
    st.markdown("""
        - **CASP-RNA**: the user can select the **CASP-RNA** example where one reference structure and multiple predicted structures are available.
    """)
    st.image("img/help/casp_rna.png")
    st.markdown("""---""")
    st.markdown("""
    
    ## Local installation
    
    The tool is available on [GitHub](https://github.com/EvryRNA/rnadvisor2) and can be installed locally. 
    A docker image is also available to build locally the webserver.
    
    You can also directly use the [RNAdvisor](https://github.com/EvryRNA/rnadvisor) tool with command line.""")

help_page()