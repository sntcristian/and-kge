# LiteralE
Knowledge Graph Embeddings learned from the structure and literals of knowledge graphs.<br/>
ArXiv link for the paper: [Incorporating Literals into Knowledge Graph Embeddings](https://arxiv.org/abs/1802.00934)

### Credits

This work was forked from https://github.com/SmartDataAnalytics/LiteralE.

### Getting Started

**Notes:** Python 3.6+ is required.

LiteralE only support computation on GPU (CUDA). The original code was tested with Nvidia Titan Xp (12GB) and RTX 2080Ti (11GB). 6 or 8GB of memory should also be enough though we couldn't test them.

1. Install PyTorch. We have verified that version 1.2.0 works.
2. Install other requirements: `pip install -r requirements.txt`
3. Install spacy model: `python -m spacy download en && python -m spacy download en_core_web_md`

### Adding external datasets

1. Add your dataset folder in the `data` folder and make sure your dataset split files have name `train.txt`, `valid.txt` and `test.txt`. Make sure that triples with numerical and textual literals are split in two separate files in a folder called `literals` in your dataset folder and call the files respectively `numerical_literals.txt` and `textual_literals.txt`. Then, run `python wrangle_KG.py FOLDER_NAME`.
2. Preprocess datasets (do these steps for each dataset in `data`):
    1. `python main_literal.py dataset FOLDER_NAME epochs 0 process True`
    2. Numerical literals: `python preprocess_num_lit.py --dataset FOLDER_NAME`
    3. Text literals: `python preprocess_txt_lit.py --dataset FOLDER_NAME`

### Running the models

To run the models execute the following command:<br/>
`python main_literal.py dataset FOLDER_NAME model MODEL_NAME input_drop INPUT_DROPOUT embedding_dim EMBEDDING_SIZE batch_size BATCH_SIZE epochs EPOCHS_NUM lr LEARNING_RATE process True`

### Changes made to original code

This repository reuses code from https://github.com/SmartDataAnalytics/LiteralE.<br/>
We modified the file `spodernet/preprocessing/batching.py` since a ValueError was occuring with the original code.<br/>
This repository also includes **bashmagic** module.
