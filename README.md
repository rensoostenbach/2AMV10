# Visual Analytics group project - Group 4
## Installation

Create a virtual environment with Python 3.8. This is done via the [2amv10_env.yml](2amv10_env.yml) file.
Use the package manager [conda](https://docs.conda.io/en/latest/) to create the environment.

```bash
conda env create -f 2amv10_env.yml
```

## Usage
Navigate to the folder where this repo is in, and run the following bash code to run the app:

```bash
conda activate 2amv10
python index.py
```

Make sure to have the data in your repo folder as well, since we do not host it on Github. It should be in a map named
"data/raw", and the processed images should be in "data/processed".
