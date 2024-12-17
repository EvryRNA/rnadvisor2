from typing import List, Tuple
import os
import pandas as pd

from src_st.tb_helper.extractor.extractor_helper import ExtractorHelper
from src_st.tb_helper.metrics.mcq import MCQ
from src_st.tb_helper.rna_torsionbert_helper import RNATorsionBERTHelper


class TBMCQ:
    def compute_tb_mcq(self, in_pdb: str) -> float:
        """
        Compute the TB-MCQ scoring function from a .pdb file
        It computes the angles with a custom Python script, and compute the MAE with the angles
            predictions from RNA-Torsion-BERT
        :param in_pdb: path to a .pdb file
        :return: the TB-MCQ score
        """
        experimental_angles = ExtractorHelper().extract_all(in_pdb)
        sequence = "".join(experimental_angles["sequence"].values)
        torsionBERT_helper = RNATorsionBERTHelper()
        torsionBERT_output = torsionBERT_helper.predict(sequence)
        mcq = MCQ().compute_mcq(experimental_angles, torsionBERT_output)
        return mcq

    @staticmethod
    def compute_tb_mcq_per_sequence(in_pdb: str) -> Tuple[str, List[float]]:
        """
        Compute the TB-MCQ scoring function from a .pdb file per sequence
        :param in_pdb: path to a .pdb file
        :return: the sequence and the TB-MCQ score per sequence
        """
        experimental_angles = ExtractorHelper().extract_all(in_pdb)
        sequence = "".join(experimental_angles["sequence"].values)
        torsionBERT_helper = RNATorsionBERTHelper()
        torsionBERT_output = torsionBERT_helper.predict(sequence)
        mcq_per_seq = MCQ().compute_mcq_per_sequence(
            experimental_angles, torsionBERT_output
        )
        return sequence, mcq_per_seq

    @staticmethod
    def compute_tb_mcq_per_sequences(list_pdbs: List[str]):
        """
        Compute the TB-MCQ per sequence for the list of PDB files.
        """
        out_seq, out_mcq = [], []
        for in_pdb in list_pdbs:
            seq, mcq_per_seq = TBMCQ.compute_tb_mcq_per_sequence(in_pdb)
            out_seq.append(seq)
            out_mcq.append(mcq_per_seq)
        return out_seq, out_mcq

    @staticmethod
    def get_tb_mcq_all(list_pdbs: List[str]):
        """
        Return the TB MCQ per position and per angle
        :return:
        """
        out_seq, out_mcq_per_pos, out_mcq_per_angle = [], [], {}
        out_mcq_per_pos_pt = []
        torsionBERT_helper = RNATorsionBERTHelper()
        mcq_helper = MCQ()
        for in_pdb in list_pdbs:
            experimental_angles = ExtractorHelper().extract_all(in_pdb)
            sequence = "".join(experimental_angles["sequence"].values)
            torsionBERT_output = torsionBERT_helper.predict(sequence)
            mcq_per_seq = mcq_helper.compute_mcq_per_sequence(
                experimental_angles, torsionBERT_output
            )
            mcq_per_seq_pt = mcq_helper.compute_mcq_per_sequence(
                experimental_angles, torsionBERT_output, torsion="PSEUDO"
            )
            mcq_per_angle = mcq_helper.compute_mcq_per_angle(
                experimental_angles, torsionBERT_output
            )
            mcq_per_angle_pt = mcq_helper.compute_mcq_per_angle(
                experimental_angles, torsionBERT_output, torsion="PSEUDO"
            )
            out_seq.append(sequence)
            out_mcq_per_pos.append(mcq_per_seq)
            out_mcq_per_pos_pt.append(mcq_per_seq_pt)
            for angle, value in {**mcq_per_angle, **mcq_per_angle_pt}.items():
                out_mcq_per_angle[angle] = out_mcq_per_angle.get(angle, []) + [value]
        names = [os.path.basename(name) for name in list_pdbs]
        seq = list(sequence[:-2])
        out = {name: mcq[:len(seq)] for name, mcq in zip(names, out_mcq_per_pos)}
        df = pd.DataFrame({"Sequence": seq, **out})
        df_angle = pd.DataFrame(out_mcq_per_angle, index=names)
        return df, df_angle


if __name__ == "__main__":
    prefix = "data/CASP_RNA/PREDS/R1107"
    list_pdbs = [
        os.path.join(prefix, name)
        for name in [
            "3drna_r1107_1.pdb",
            "alphafold3_R1107_1.pdb",
            "best_R1107_1.pdb",
            "rhofold_r1107.pdb",
        ]
    ]
    # mcq_seq = TBMCQ.compute_tb_mcq_per_sequences(list_pdbs)
    TBMCQ.get_tb_mcq_all(list_pdbs)
