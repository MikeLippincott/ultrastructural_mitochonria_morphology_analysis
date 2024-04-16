#!/usr/bin/env python
# coding: utf-8

# # Convert SQLite file output from CellProfiler into separate parquet files per mask/object using Cytotable

# ## Import libraries

# In[1]:


import logging
import pathlib

import pandas as pd
from parsl.config import Config
from parsl.executors import HighThroughputExecutor

# cytotable will merge objects from SQLite file into single cells and save as parquet file
from cytotable import convert

# pcytominer annotate will get the metadata from the image_df to apply to the other object dfs
from pycytominer import annotate

# Set the logging level to a higher level to avoid outputting unnecessary errors from config file in convert function
logging.getLogger().setLevel(logging.ERROR)


# ## Set paths and variables

# In[2]:


# type of file output from CytoTable (currently only parquet)
dest_datatype = "parquet"

# set main output dir for all parquet files
output_dir = pathlib.Path("./profiles")
output_dir.mkdir(exist_ok=True)

# directory where SQLite file is located
sqlite_dir = pathlib.Path("../1.cellprofiler_analysis/analysis_output/")

# Set converted parquet path for files
parquet_path = pathlib.Path(f"{output_dir}/converted_profiles")


# ## Run cytotable convert to output nuclei and image features separately for all plates

# In[3]:


# merge single cells and output as parquet file
convert(
    source_path=str(sqlite_dir),
    dest_path=str(parquet_path),
    dest_datatype=dest_datatype,
    metadata=["image"],
    compartments=["mito", "lamellar", "tubular"],
    identifying_columns=["ImageNumber"],
    join=False,
    parsl_config=Config(
        executors=[HighThroughputExecutor()],
    ),
    chunk_size=10000,
)

print("Conversion finished for EM data")


# ## Move parquet files out of folders with the same name for easier access in downstream analysis

# In[4]:


# Edit the structure of the output to remove the extra nested folders in each plate folder
for parent_dir in output_dir.iterdir():
    if parent_dir.is_dir():
        for subdir in parent_dir.iterdir():
            if subdir.is_dir():
                for file_path in subdir.glob("*.parquet"):
                    new_path = parent_dir / file_path.name
                    file_path.rename(new_path)
                # Remove the subfolder with the same name as the parquet file
                subdir.rmdir()

print("Parquet files moved down in the nest and folders removed.")


# ## Remove unwanted image + metadata columns and merge relevant metadata into each mask/object file from the image file

# In[5]:


# path to unwanted image cols text file
unwanted_list_path = pathlib.Path("./unwanted_image_cols.txt")
# Load the list of columns to remove from the text file
with open(unwanted_list_path, "r") as file:
    columns_to_remove = [line.strip() for line in file]


# In[6]:


# Read in each file as data frame
image_df = pd.read_parquet(pathlib.Path(f"{parquet_path}/per_image.parquet"))
mito_df = pd.read_parquet(pathlib.Path(f"{parquet_path}/per_mito.parquet"))
lamellar_df = pd.read_parquet(pathlib.Path(f"{parquet_path}/per_lamellar.parquet"))
tubular_df = pd.read_parquet(pathlib.Path(f"{parquet_path}/per_tubular.parquet"))

print(
    "Starting to edit image and object data frames for EM data",
)

# Drop the specified columns from image_df (ignore error if a column isn't there)
image_df = image_df.drop(columns=columns_to_remove)

# Identify metadata columns for mask data frame
metadata_cols = [
    col
    for col in image_df.columns
    if col.startswith("Image_Metadata") or col == "Metadata_ImageNumber"
]

# Change prefix and remove "Image_" portion from metadata columns
new_metadata_cols = [col.replace("Image_", "") for col in metadata_cols]
image_df = image_df.rename(columns=dict(zip(metadata_cols, new_metadata_cols)))

mito_df = annotate(
    profiles=mito_df,
    platemap=image_df[new_metadata_cols],
    join_on=["Metadata_ImageNumber", "Metadata_ImageNumber"],
)
lamellar_df = annotate(
    profiles=lamellar_df,
    platemap=image_df[new_metadata_cols],
    join_on=["Metadata_ImageNumber", "Metadata_ImageNumber"],
)
tubular_df = annotate(
    profiles=tubular_df,
    platemap=image_df[new_metadata_cols],
    join_on=["Metadata_ImageNumber", "Metadata_ImageNumber"],
)

# Update object number column in the object data frames and add Metadata_ prefix
for df in [mito_df, lamellar_df, tubular_df]:
    for col in df.columns:
        if col.endswith("_Number_Object_Number"):
            new_col_name = f"Metadata_{col}"
            df.rename(columns={col: new_col_name}, inplace=True)

# Save data frames to the same path
image_df.to_parquet(f"{parquet_path}/per_image.parquet", index=False)
mito_df.to_parquet(f"{parquet_path}/per_mito.parquet", index=False)
lamellar_df.to_parquet(f"{parquet_path}/per_lamellar.parquet", index=False)
tubular_df.to_parquet(f"{parquet_path}/per_tubular.parquet", index=False)

# Output shapes and one data frame to assess all looks correct
print("Shape of image data frame", image_df.shape)
print("Shape of mito data frame", mito_df.shape)
print("Shape of lamellar data frame", lamellar_df.shape)
print("Shape of tubular data frame", tubular_df.shape)
lamellar_df.head()

