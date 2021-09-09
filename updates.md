# Project Updates

### Update 16/06/2021
#### Library update
With respect to the model added in the previous week to Pykeen (DistMult + text literals), we added to Pykeen two other multimodal models:
1. `ComplExText`: a model based on **ComplEx** which uses information from textual labels to train knowledge graph embeddings via a linear transformation between the entity representation and the text representation,
2. `DistMult_gate_text`: a **DistMult** model which uses information coming both from numeric and textual literals in order to train knowledge graph embeddings via a *gated recurrent unit* (GRU) that combines the three vectors (textual, numeric and structural) as described in ([Kristiadi, 2018](https://arxiv.org/abs/1802.00934)).
However, in order to implement these models, we switched from working with the latest version of Pykeen (now v1.5.0) to its previous release [v-1.4.0](https://github.com/pykeen/pykeen/releases/tag/v1.4.0): we preferred this version for the clarity of code and for having less modularity (easier to add features).<br/>
We tested all the models inside the Pykeen v1.4.0 suite and they all work. 

#### Dataset update
Another dataset was created in order to train Knowledge Graph Embeddings with numeric literals as well as text.
The dataset is called `OC-170K` and is different from the previous one for two aspects:
1. numeric triples are stored in a separate file and numbers are not considered as structural entities,
2. now authors are linked in the kg with the property `oco:hasNext`.
Statistics are available in the `OC-170K` folder and a picture of the data model is available on `docs`.

#### Experiments in authors clustering
We started our first experiments in authors disambiguation by clustering embeddings extracted from a KGE model trained on `OC-197K`.
The KGE model was trained on sparse data so it did not have great performances when tested. However, it was possible to test the practicability of clustering the embeddings related to a specific author name (i.e. all authors named "M Bonitz") to disambiguate them. <br/>
In order to do so, we applied different distance measures between the embeddings (e.g. euclidean distance or cosine similarity) and we applied hierarchical agglomerative clustering by selecting different distance thresholds. In our little experiment, a thresold of 1.4 allowed to distinguish between two different authors having the same name. A notebook containing the toy example is available in `notebooks/author_disambiguation.ipynb`.

#### Efficiency of Multimodal Models on OC-170K
We conducted several trials with the three Multimodal Models in our Pykeen extension on the dataset `OC-170K`.<br/>
The parameters with which we trained the models were:
- evaluator: RankBased
- loss: BCEWithLogits
- embedding dimension: 300
- input dropout: 0.31970168873359067
- number of negatives per position: 1
- learning rate: 0.0015736407249343375
- batch size: 3032
- epochs: 1000
These hyper-parameters were obtained after carrying hyper-parameter optimization on `DistMult_gate_text` for 12 hours. Moreover, early stopping was adopted in the pipeline to prevent overfitting. The configuration files used in the pykeen pipeline are available in the `trials-OC-170K` folder.<br/>
We conducted five experiments for each model in order to understand the degree of consistency in the results. For each model we looked at Hits@10 and we computed average and standard deviation across five trials.
The results are:
- DistMultText: 0.566 (avg)
- DistMult_gate_text: 0.582 (avg)
- ComplExText: *not available still*.
The results are stored in CSV format on `trials-OC-170K/results.csv`.

#### Current issues
In this section we note down the issues that we still have to face:
- This procedure involves the manual selection of many parameters, from model hyper-parameters to distance measures and thresholds in clustering.
- We should consider agents instead of roles (see OpenCitations Data Model).
- the current dataset doesn't allow to test a systematic author name disambiguation process since author's ORCIDs are not stored.
- There might be other entities in the Knowledge Graph which were excluded in the embedding modelling process (e.g. `pro:publisher`, `cito:Citation`, `biro:BibliographicReference`).
- still we haven't addressed the issue of multiple textual labels attached to the same entity (e.f. `foaf:familyName` and `foaf:givenName`).
- we haven't tackled the question of blocking.


### Update 7/06/2021
#### Dataset update
We noticed that the previous datasets suffered from severe bugs, among which:
1. publishers and works were not disambiguated,
2. the preprocessing algorithm produced many duplicate triples,
3. literal triples were included in the train, test and validation datasets.
We corrected these errors and we updated the dataset according to a revised data model. This dataset is called `OC-197K` and it contains 197,366 triples, among which 87,511 are triples containing textual literals (e.g. titles of works, authors' names). The data model is available in the `docs` folder.
#### Library update
Our decision to rely on the project [LiteralE](https://github.com/SmartDataAnalytics/LiteralE) was changed due to the following reasons:
1. the project is no more mantained,
2. there was no sufficient documentation,
3. the project did not allow for many functionalities that we need (e.g. hyper-parameter optimization).
Thus, what we did was to shift to a more mantained library called [pykeen](https://github.com/pykeen/pykeen), a Python package designed to train and evaluate knowledge graph embedding models (incorporating multi-modal information). This library already supports an implementation of the `DistMultLiteral` model which support numeric information from KGs. <br/>
In the folder `pykeen-AND` of this repo we put some extension files for the release `1.4.1-dev` of pykeen in order to allow to train knowledge graph embeddings by using also textual literals info. As in the current state of the repository, we were able to implement a model called **DistMultText** which encodes textual labels of entities (e.g. titles and names) into embeddings by means of **allenai-specter** a BERT language model pre-trained on scholarly literature. For further information please take a look at the `README.md` file in the `pykeen-AND` folder.
#### Notebooks
We introduced the publication of the colab notebooks used to run our experiments. This was mainly done for two reasons:
1. provide a reproducible workflow of our experimental procedures,
2. show how to correctly install and run our extension of the library,
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
