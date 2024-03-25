#!/usr/bin/env python
# coding: utf-8

# This notebook extracts metadata from the dataset file and creates a metadata csv file.

# In[1]:


import pathlib

import pandas as pd

# In[2]:


# create and error
def create_error(file: str):
    """
    Raises an error if the proper substring is not found in the image file name

    Parameters
    ----------
    file : str
        string of the file path to the image

    Raises
    ------
    ValueError
        Raises an error if the proper substring is not found in the image file name
    """
    raise ValueError(f"Unknown image category type: {file.stem.split('_')[5]}")


# In[3]:


path_to_data = pathlib.Path("../../data/raw_images").resolve(strict=True)


# In[4]:


# get all files in the data directory
all_image_files = path_to_data.glob("*.tiff")


# In[5]:


metadata_dict = {
    "condition": [],
    "cell_id": [],
    "mitochondria_id": [],
    "image_label": [],
    "image_category_type": [],
    "file_name": [],
    "file_path": [],
}


# In[6]:


for file in all_image_files:
    metadata_dict["condition"].append(file.stem.split("_")[1])
    metadata_dict["cell_id"].append(file.stem.split("_")[3])
    metadata_dict["mitochondria_id"].append(file.stem.split("_")[4])
    metadata_dict["image_label"].append(file.stem.split("_")[5])
    if file.stem.split("_")[5] == "tubular":
        metadata_dict["image_category_type"].append("tubular_cristae_mask")
    elif file.stem.split("_")[5] == "ori":
        metadata_dict["image_category_type"].append("original_EM_image")
    elif file.stem.split("_")[5] == "mito":
        metadata_dict["image_category_type"].append("mitochondria_mask")
    elif file.stem.split("_")[5] == "lamellar":
        metadata_dict["image_category_type"].append("lamellar_cristae_mask")
    else:
        create_error(file)
    metadata_dict["file_name"].append(file.stem)
    metadata_dict["file_path"].append(file)
print(
    file.stem.split("_")[0],
    file.stem.split("_")[1],
    file.stem.split("_")[2],
    file.stem.split("_")[3],
    file.stem.split("_")[4],
    file.stem.split("_")[5],
)


# In[7]:


# make a dataframe from the dictionary
metadata_df = pd.DataFrame(metadata_dict)
# drop the image label column
metadata_df = metadata_df.drop(columns=["image_label"])
# make columns the correct data type
metadata_df["condition"] = metadata_df["condition"].astype("category")
metadata_df["cell_id"] = metadata_df["cell_id"].astype("int")
metadata_df["mitochondria_id"] = metadata_df["mitochondria_id"].astype("int")
metadata_df["image_category_type"] = metadata_df["image_category_type"].astype(
    "category"
)
metadata_df["file_name"] = metadata_df["file_name"].astype("str")
metadata_df["file_path"] = metadata_df["file_path"].astype("str")
print(metadata_df.shape)
metadata_df.head()


# In[8]:


# save the metadata to a csv file
metadata_df.to_csv("../../data/metadata.csv", index=False)
