# Project Updates


### Update 7/06/2021
#### Dataset update
We noticed that the previous datasets suffered from severe bugs, among which:
1. Publishers and works were not disambiguated,
2. The preprocessing algorithm produced many duplicate triples,
3. literal triples were included in the train, test and validation datasets.
We corrected these errors and we updated the dataset according to a revised data model. This dataset is called `OC-197K` and it contains 197,366 triples, among which 87,511 are triples containing textual literals (e.g. titles of works, authors' names). The data model is available in the `docs` folder.
#### Library update
Our decision to rely on the project [LiteralE](https://github.com/SmartDataAnalytics/LiteralE) was changed due to the following reasons:
1. the project is no more mantained,
2. there was no sufficient documentation,
3. the project did not allow for many functionalities that we need (e.g. hyper-parameter optimization).
Thus, what we did was to shift to a more mantained library called [pykeen](https://github.com/pykeen/pykeen) a Python package designed to train and evaluate knowledge graph embedding models (incorporating multi-modal information). This library already support an implementation of the `DistMultLiteral` model which support numeric information from KGs. <br/>
The forked version contained in the folder `pykeen-AND` of this repo contains the release `1.4.1-dev` of pykeen modified in order to allow to train knowledge graph embeddings by using also textual literals info. As in the current state of the repository, we were able to implement a model called **DistMultText** which encodes textual labels of entities (e.g. titles and names) into embeddings by means of **allenai-specter** a BERT language model pre-trained on scholarly literature. For further information please take a look at the `README.md` file in the `pykeen-AND` folder.
#### Notebooks
We introduced the publication of the colab notebooks used to run our experiments. This was mainly done for two reasons:
1. provide a reproducible workflow of our experimental procedures,
2. show how to correctly install and run our modified version of library,
3. show how to correctly run our models inside the pykeen framework.
You can find the colab notebooks in the `notebooks` folder.

### Update 26/05/2021
#### OC-55K
- We updated the `OC-33K` dataset by adding publication data in `xsd:gYear` format for each article. We obtained a new dataset of 55k triples called `OC-55K`. A schema of the data model is available in the `docs` folder.
- The dataset was stored in TSV format and is available in the `OC-55K` folder as `kg.txt`
- The dataset statistics are available in a file called `kg_statistics.json`.
- `kg.txt` was split into three distinct file for model training: `train.txt`, `test.txt` and `valid.txt`. The percentage of the split were 80%/10%/10%.
- the test set was derived by randomly splitting the file. Instead, we made sure that `valid.txt` does not contain unseen entities and relationships by using the `train_test_split_no_unseen` function from **ampligraph**. For further details on how the dataset was obtained check `obtain_OC_55K.py`.
#### Forked repository from [SmartDataAnalytics/LiteralE](https://github.com/SmartDataAnalytics/LiteralE)
- We stored in the Github repository a forked version of a repository of the model LiteralE, which models textual and numerical information from Knowledge Graphs. The files are available in the `LiteralE` folder.
- The `LiteralE` folder does not contain the original source code but a derived version. We basically changed the `preprocessing/batching.py` file in the spodernet module due to a `ValueError` on my data. 
- To understand how to import data and run experiments look up the `README.md` file inside the folder.
#### Results from DistMult with textual and numerical literals (100 epochs)
- We trained the `DistMult_text` model available in [LiteralE](https://github.com/SmartDataAnalytics/LiteralE) on `OC-55K`.
- Hyperparameters were `input_drop 0.2`, `embedding_dim 100`, `batch_size 128`, `epochs 100`, `lr 0.01`.
- Final results on the test set were: <br/>
  **Hits@1:** 0.03,
  **Hits@3:** 0.06,
  **Hits@5:** 0.08,
  **Hits@8:** 0.1,
  **Hits@10:** 0.116,
  **Mean Rank:** 4507,
  **Mean Reciprocal Rank:** 0.06. <br/>
#### Results from ComplEx with numerical literals (100 epochs)
- We trained the `ComplEx_gate` model available in [LiteralE](https://github.com/SmartDataAnalytics/LiteralE) on `OC-55K`.
- Hyperparameters were the same as in DistMult.
- Final results on the test set were: <br/>
**Hits@1:** 0.027,
**Hits@3:** 0.05,
**Hits@5:** 0.06,
**Hits@8:** 0.07,
**Hits@10:** 0.08,
**Mean Rank:** 8407,
**Mean Reciprocal Rank:** 0.04.
#### Discussions on preliminary results
- The models trained for 100 epochs have bad performances.
- Both in validation and testing the models have poorer performances in tail prediction rather than head prediction.
- DistMult, with same parameters, performs better than ComplEx.
- By increasing learning rate (fro 0.001 to 0.01) the model performances did not increase.
- Two ways of preventing the models from underfitting might be to train them for more epochs or feed them with more (structural) data (e.g. by adding coauthorship links between authors).
#### Results from DistMult with textual and numerical literals (500 epochs)
- We trained the `DistMult_text` model available in [LiteralE](https://github.com/SmartDataAnalytics/LiteralE) on `OC-55K`.
- Hyperparameters were `input_drop 0.2`, `embedding_dim 100`, `batch_size 128`, `epochs 500`, `lr 0.01`.
- Final results on the test set were: <br/>
  **Hits@1:** 0.04,
  **Hits@3:** 0.07,
  **Hits@5:** 0.09,
  **Hits@8:** 0.11,
  **Hits@10:** 0.119,
  **Mean Rank:** 4737,
  **Mean Reciprocal Rank:** 0.11. <br/>
- By increasing the epochs the performances increased, but not significantly.
- Still, the model was not able to reduce the difference between the prediction scores of head and tail entities.
- The model's performances reached their peak around epoch 400 and then started to fluctuate and decrease.

### Update 21/05/2021
- Report on literature review, data analysis, data modelling and first model architecture: [slides](https://docs.google.com/presentation/d/12JzKb53fGLuNAyHXao7tzu0kn5Cor8FKPT_bW7_U2Js/edit?usp=sharing)