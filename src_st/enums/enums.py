ALL_METRICS = [
    "RMSD",
    "P-VALUE",
    "INF",
    "DI",
    "MCQ",
    "CAD",
    "BARNABA",
    "CLASH",
    "GDT-TS",
    "lDDT",
    "QS-SCORE",
    "LCS-TA",
    "TM-score",
]
QUICK_METRICS = ["RMSD", "P-VALUE", "INF", "DI", "BARNABA", "GDT-TS", "TM-score"]
ALL_SCORING_FUNCTIONS = ["BARNABA", "DFIRE", "rsRNASP", "RASP", "TB-MCQ", "CGRNASP"]
QUICK_SCORING_FUNCTIONS = ["DFIRE", "RASP", "TB-MCQ"]
SUB_METRICS = [
    "RMSD",
    "P-VALUE",
    "εRMSD",
    "TM-score",
    "GDT-TS",
    "INF-ALL",
    "CAD",
    "lDDT",
    "MCQ",
]

# Higher is better
ASC_METRICS = [
    "INF-ALL",
    "TM-score",
    "GDT-TS",
    "lDDT",
    "INF-WC",
    "INF-NWC",
    "INF-STACK",
    "CAD",
    "GDT-TS",
]
# Lower is better
DESC_METRICS = ["RMSD", "P-VALUE", "DI", "εRMSD", "MCQ"]
COLORS_MAPPING = {
    "RMSD": "#e10000",
    "INF-ALL": "#656567",
    "CAD": "#ee7f00",
    "TM-score": "#8b1b58",
    "GDT-TS": "#76885B",
    "lDDT": "#31b2cb",
    "P-VALUE": "#B67352",
    "εRMSD": "#FFD23F",
    "MCQ": "#005793",
    "INF-STACK": "#ef8927",
    "INF-WC": "#83b8d6",
    "INF-NWC": "#621038",
}
OLD_TO_NEW = {
    "BARNABA-eRMSD": "εRMSD",
    "BARNABA-eSCORE": "εSCORE",
}
METRICS_TO_HIDE = [
    "INF-STACK",
    "INF-WC",
    "INF-NWC",
    "BARNABA-RMSD",
    "GDT-TS@2",
    "GDT-TS@4",
    "GDT-TS@8",
    "GDT-TS@1",
    "BARNABA-eSCORE",
    "DI",
    "CLASH",
]
NEGATIVE_ENERGY = ["εSCORE"]
SUB_SCORING = [
    "DFIRE",
    "RASP-ENERGY",
    "RASP-NB-CONTACTS",
    "RASP-NORMALIZED-ENERGY",
    "rsRNASP",
    "εSCORE",
    "TB-MCQ",
    "CGRNASP",
]
COLORS_MAPPING_SCORING = {
    "RASP-ENERGY": "#6499E9",
    "εSCORE": "#B5CB99",
    "DFIRE": "#EF6262",
    "rsRNASP": "#F3AA60",
    "RASP-NB-CONTACTS": "#A0E9FF",
    "RASP-NORMALIZED-ENERGY": "#17A5A5",
    "TB-MCQ": "#F3AA60",
    "CGRNASP": "#F3AA60",
}

import os

ALIGNED_PATH = os.path.join("data", "tmp", "aligned.pdb")
OUT_PATH = os.path.join("data", "output", "tmp_out.csv")
TIME_PATH, LOG_PATH = os.path.join("data", "output", "time.csv"), os.path.join(
    "data", "output", "log.csv"
)
PRED_DIR = os.path.join("data", "tmp", "preds")
NATIVE_PATH, PRED_PATHS = None, None
CASP_PATH, RNA_PUZZLES_PATH = os.path.join("data", "CASP_RNA", "NATIVE"), os.path.join(
    "data", "RNA_PUZZLES", "NATIVE"
)
CASP_CHALLENGES = [
    "R1107",
    "R1108",
    "R1116",
    "R1117",
    "R1126",
    "R1128",
    "R1149",
    "R1156",
    "R1156",
    "R1189",
    "R1190",
]
RNA_PUZZLES_CHALLENGES = [
    "rp03",
    "rp04",
    "rp05",
    "rp06",
    "rp07",
    "rp08",
    "rp09",
    "rp11",
    "rp12",
    "rp13",
    "rp14_bound",
    "rp14_free",
    "rp16",
    "rp17",
    "rp18",
    "rp21",
    "rp23",
    "rp24",
    "rp25",
    "rp29",
    "rp32",
    "rp34",
]


TEXT_BY_FIGURES = {
    "Bar plot": "Bar plot with the normalised scores for each score considered. The higher the score, the better the model. The scores are normalised to be between 0 and 1, "
    "where 1 is the best and 0 the worst. The decreasing scores are reversed to be increasing.",
    "Polar plot": "Polar plot for the INF metric for each model. "
    "It considers the different type of interactions possible in the RNA structure: stacking, Watson-Crick, non-Watson-Crick.",
    "TB-MCQ per position": "TB-MCQ value for each position of the sequence for each model.",
    "TB-MCQ per angle": "Line polar plot with the TB-MCQ value for each angle for each model. The lower the MCQ value, the better the model.",
    "Time plot": "Time plot for the different metrics/scoring functions used. It shows the time taken to compute the score for all the models.",
    "Results": "Obtained dataframe with the different metrics/scoring functions for each model. Methods are sorted by RMSD.",
}
