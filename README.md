# Ultrastructural mitochondria morphology analysis

This repository contains the code used to analyze the ultrastructural morphology of mitochondria in electron microscopy images from [Suga et al. 2023](https://doi.org/10.1371/journal.pbio.3002246).
The main goal of this project is to demonstrate proof-of-concept for extracting high-content morphology measurements from electron microscopy (EM) images of mitochondria.

We will analyze the morphology of mitochondria tubular cristae and laminellar cristae in shRNA knockdowns of control and OPA1 cells.
We are interested in mitochondrial cristae, shape, size and morphology.

## Set up environment

To perform the image analysis and image-based profiling notebooks, please create the conda (or mamba) environment using the [image_profiling_env yaml file](./image_profiling_env.yml).

```bash
conda env create -f image_profiling_env.yml
```
