import transformers
import torch
from transformers import AutoModel, AutoTokenizer
import numpy as np
import pandas as pd
from typing import Optional, Dict
import os
from src_st.tb_helper.tb_mcq import TBMCQ

tb_mcq = TBMCQ()
tb_mcq.compute_tb_mcq("tests/R1107.pdb")