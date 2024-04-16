# Preprocessing Features

In this module, we convert the SQLite output of the EM data into individual `parquet` files for image data, mitochondria (mito) mask data, lamellar mask data, and tubular mask data using [CytoTable](https://github.com/cytomining/CytoTable).
Next, we used [pycytominer](https://github.com/cytomining/pycytominer) to process each `parquet` file, where CellProfiler features are normalized using standard scalar and applied feature selection to remove redundant features. 

## Perform preprocessing

To perform the preprocessing notebooks, run the below code:

```bash
cd 2.preprocess_features
source preprocess_data.sh
```
