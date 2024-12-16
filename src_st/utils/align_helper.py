import subprocess
import os
from typing import List
from Bio import PDB
from Bio.PDB import PDBIO


COMMAND = "lib/zhanggroup/USalign -mol RNA $REFERENCE $PRED -o tmp/struct1"


def align_structures(
    reference_struct: str, prediction_structs: List[str], out_path: str
):
    """
    Align multiple predicted structures to the reference structure, adding each prediction as a new chain.

    Args:
        :param reference_struct: The reference structure to superimpose.
        :param prediction_structs: A list of predicted models to superimpose to the reference.
        :param out_path: Where to save the superimposed structures.
    """
    if not all(
        struct.endswith(".pdb") for struct in [reference_struct] + prediction_structs
    ):
        return None
    # Initialize with reference structure
    pdb1 = PDB.PDBParser().get_structure("reference", reference_struct)
    for prediction_struct in prediction_structs:
        command = COMMAND.replace("$REFERENCE", reference_struct).replace(
            "$PRED", prediction_struct
        )
        try:
            output = subprocess.check_output(
                command, shell=True, stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            print(f"Error in superimposing {reference_struct} and {prediction_struct}")
            continue
        # Merge prediction as a new chain
        try:
            merge_structure_with_new_chain(pdb1, "tmp/struct1.pdb")
        except (
            PDB.PDBExceptions.PDBIOException,
            ValueError,
            PDB.PDBExceptions.PDBConstructionException,
            FileNotFoundError,
        ):
            print(f"Error in merging {reference_struct} and {prediction_struct}")
            continue
        # Clean up intermediate file
        os.system("rm tmp/struct1.pdb")
    # Save the final structure with all chains
    io = PDBIO()
    io.set_structure(pdb1)
    io.save(out_path)
    os.system("rm tmp/*.pml")  # Clean up temporary PyMOL script files


def get_last_chain(chains: List[PDB.Chain.Chain]) -> str:
    """
    Return the next chain ID.
    """
    ids = [chain.id for chain in chains]
    orders = [ord(id) for id in ids]
    max_order = max(orders)
    return chr(max_order + 1).upper()


def merge_structure_with_new_chain(reference_structure, struct2_path: str):
    """Merge struct2 as a new chain in the reference structure."""
    pdb2 = PDB.PDBParser().get_structure("pdb2", struct2_path)
    chains = list(pdb2.get_chains())
    new_id = get_last_chain(list(reference_structure[0].get_chains()))
    chains[0].id = new_id
    chains[0].detach_parent()
    reference_structure[0].add(chains[0])


if __name__ == "__main__":
    native_structure = "data/CASP_RNA/NATIVE/R1107.pdb"
    pred_structures = [
        f"data/CASP_RNA/PREDS/R1107/best_R1107_{i}.pdb" for i in range(1, 6)
    ]
    out_path = "test_multiple_alignment.pdb"
    align_structures(native_structure, pred_structures, out_path)
