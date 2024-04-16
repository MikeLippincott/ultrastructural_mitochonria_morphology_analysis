#!/bin/bash

# initialize the correct shell for your machine to allow conda to work (see README for note on shell names)
conda init bash
# activate the main conda environment
conda activate image_profiling_em_data

# convert all notebooks to python files into the scripts folder
jupyter nbconvert --to python --output-dir=scripts/ *.ipynb

# run the python scripts in order (convert with CytoTable then normalize+feature select with pycytominer)
python scripts/0.convert_cytotable.py
python scripts/1.norm_fs_pycytominer.py
