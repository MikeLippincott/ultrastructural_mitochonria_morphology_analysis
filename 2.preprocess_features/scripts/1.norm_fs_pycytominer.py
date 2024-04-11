#!/usr/bin/env python
# coding: utf-8

# # Perform data preprocessing with pycytominer on each compartment file

# ## Import libraries

# In[1]:


import pathlib

import pandas as pd
from pycytominer import normalize, feature_select
from pycytominer.cyto_utils import infer_cp_features


# ## Set paths and variables

# In[2]:


# operations to perform for feature selection
feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
    "drop_na_columns"
]

# Output directory for processed profiles
output_dir = pathlib.Path("./profiles/processed_profiles")
output_dir.mkdir(parents=True, exist_ok=True)

# Path to CytoTable converted profiles for each object
converted_profiles_dir = pathlib.Path("./profiles/converted_profiles/")

# List all the converted files in the directory
converted_files = [file for file in converted_profiles_dir.iterdir() if file.is_file()]

# Print the converted files that will be processed
for file in converted_files:
    print(file)


# ## Perform preprocessing on single cell features

# In[3]:


for file in converted_files:
    print(f"Performing pycytominer pipeline for {file.stem}")
    output_normalized_file = str(
        pathlib.Path(f"{output_dir}/{file.stem}_normalized.parquet")
    )
    output_feature_select_file = str(
        pathlib.Path(f"{output_dir}/{file.stem}_feature_selected.parquet")
    )

    # Load in file to process
    df = pd.read_parquet(file)

    # Set the compartment name to find in the data frame (must be capitalized)
    compartment_name = file.stem.split("_")[1].capitalize()

    # Find the cp features based on the mask name or image
    cp_features = infer_cp_features(population_df=df, compartments=[compartment_name])

    # Find the metadata features
    meta_features = infer_cp_features(population_df=df, compartments=[compartment_name], metadata=True)

    # Step 2: Normalization
    normalize(
        profiles=df,
        method="standardize",
        features=cp_features,
        meta_features=meta_features,
        output_file=output_normalized_file,
        output_type="parquet",
    )

    # Step 3: Feature selection
    feature_select(
        output_normalized_file,
        operation=feature_select_ops,
        na_cutoff=0,
        features=cp_features,
        output_file=output_feature_select_file,
        output_type="parquet",
    )

    print(
        f"Normalization and feature selection have been performed for {file.stem}"
    )


# ## Check example output file to confirm that the process worked

# In[4]:


# Check output file
test_df = pd.read_parquet(output_feature_select_file)

print(test_df.shape)
test_df.head(2)

