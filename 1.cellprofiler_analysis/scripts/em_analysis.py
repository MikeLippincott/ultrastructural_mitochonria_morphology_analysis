#!/usr/bin/env python
# coding: utf-8

# # Perform feature extraction for EM data using CellProfiler Parallel

# ## Import libraries

# In[1]:


import pathlib
import pprint

import sys

sys.path.append("../utils")
import cp_parallel


# ## Set paths and variables

# In[2]:


# set the run type for the parallelization
run_name = "analysis"

# set main output dir for all plates
output_dir = pathlib.Path("./analysis_output")
output_dir.mkdir(exist_ok=True)

# directory where images and masks are located within folders
images_dir = pathlib.Path("../0.download_data/data").resolve(strict=True)

# path to pipeline to perform feature extraction
pipeline_path = pathlib.Path("./pipeline/3D_analysis.cppipe")


# ## Create dictionary with all info for data
# 
# The CellProfiler Parallel command expects paths in a dictionary form (made for multiple plates to process).

# In[3]:


# create plate info dictionary with specified plates for the CellProfiler CLI command
plate_info_dictionary = {
    "EM_data": {
        "path_to_images": images_dir,
        "path_to_output": output_dir,
        "path_to_pipeline": pipeline_path
    }
}

# view the dictionary to assess that all info is added correctly
pprint.pprint(plate_info_dictionary, indent=4)


# ## Run analysis pipeline on each plate in parallel
# 
# This cell is not finished to completion due to how long it would take. It is ran in the python file instead.

# In[4]:


cp_parallel.run_cellprofiler_parallel(
    plate_info_dictionary=plate_info_dictionary, run_name=run_name
)

