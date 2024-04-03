# CellProfiler Analysis

In this module, we run a 3D feature extraction pipeline using CellProfiler.
We extract features from three "compartments":

- Whole mitochondria 
- Lamellar cristae 
- Tubular cristae

We extract these measurements specifically:

- `Image Quality`
- `Granularity`
- `Object Neighbors` - specifically lamellar and tubular neighbors
- `Image Area Occupied`
- `Object Intensity`
- `Object Size Shape`
- `Texture`

Extracted features are outputted as an SQLite file with image and object features as individual tables.

## Run CellProfiler 3D analysis

To run the notebook to perform the 3D analysis in CellProfiler, run the below command.

```bash
# Change to the cellprofiler analysis directory
cd 1.cellprofiler_analysis
# Run the script to perform analysis
source cellprofiler_analysis.sh
```
