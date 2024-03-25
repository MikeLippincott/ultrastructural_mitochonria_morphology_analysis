#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pathlib

import pandas as pd

# In[2]:


path_to_data = pathlib.Path("../../data/images").resolve(strict=True)


# In[3]:


# get all files in the data directory
files = path_to_data.glob("*")


# In[4]:


metadata_dict = {
    "condition": [],
    "cell_number": [],
    "mitochondria_number": [],
    "file_type": [],
    "file_name": [],
    "file_path": [],
}


# In[5]:


for file in files:
    metadata_dict["condition"].append(file.stem.split("_")[0])
    metadata_dict["cell_number"].append(file.stem.split("_")[2])
    metadata_dict["mitochondria_number"].append(file.stem.split("_")[3])
    metadata_dict["file_type"].append(file.stem.split("_")[4])
    metadata_dict["file_name"].append(file.stem)
    metadata_dict["file_path"].append(file)


# In[6]:


# make a dataframe from the dictionary
metadata_df = pd.DataFrame(metadata_dict)
print(metadata_df.shape)
metadata_df.head()


# In[7]:


# save the metadata to a csv file
metadata_df.to_csv("../../data/metadata.csv", index=False)
