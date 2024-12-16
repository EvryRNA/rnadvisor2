import os

from src_st.utils.align_helper import align_structures

native_structure = "data/CASP_RNA/NATIVE/R1107.pdb"
prefix = os.path.join("data", "CASP_RNA", "PREDS")
pred_structures = [
    os.path.join(prefix, "R1107", rna)
    for rna in ["3drna_r1107_1.pdb", "best_R1107_1.pdb", "rhofold_r1107.pdb"]
]

out = align_structures(native_structure, pred_structures, "test_alignment.pdb")
