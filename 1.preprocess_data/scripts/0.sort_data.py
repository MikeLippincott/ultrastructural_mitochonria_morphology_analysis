#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pathlib

# In[2]:


# set path to data
data_path = pathlib.Path("../../data/").resolve(strict=True)
new_data_path = pathlib.Path("../../data/images/").resolve()
# make new data directory if it doesn't exist
new_data_path.mkdir(parents=True, exist_ok=True)


# In[3]:


# get all files in data directory recursively
files = data_path.rglob("*")


# In[4]:


# loop through the files
for file in files:
    if file.is_file():
        if file.suffix == ".tiff":
            new_file_name = (
                str(file.parents[0]).split("data/")[2].replace("/", "_")
                + "_"
                + file.stem
                + ".tiff"
            )
            new_file_path = pathlib.Path(f"{data_path}/images/{new_file_name}")
            print(file, new_file_path)
            # rename file
            file.rename(new_file_path)
