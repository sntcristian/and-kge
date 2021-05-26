# Project Updates

### Update 21/05/2021
- Report on literature review, data analysis, data modelling and first model architecture: [slides](https://docs.google.com/presentation/d/12JzKb53fGLuNAyHXao7tzu0kn5Cor8FKPT_bW7_U2Js/edit?usp=sharing)
### Update 26/05/2021
#### OC-55K
- I updated the `OC-33K` dataset by adding publication data in `xsd:gYear` format for each article. I obtained a new dataset of 55k triples called `OC-55K`. A schema of the data model is available in the `docs` folder.
- The dataset was stored in TSV format and is available in the `OC-55K` folder as `kg.txt`
- The dataset statistics are available in a file called `kg_statistics.json`.
- `kg.txt` was split into three distinct file for model training: `train.txt`, `test.txt` and `valid.txt`. The percentage of the split were 80%/10%/10%.
- the test set was derived by randomly splitting the file. Instead, we made sure that `valid.txt` does not contain unseen entities and relationships by using the `train_test_split_no_unseen` function from **ampligraph**. For further details on how the dataset was obtained check `obtain_OC_55K.py`.
#### Forked repository from [SmartDataAnalytics/LiteralE](https://github.com/SmartDataAnalytics/LiteralE)
- I stored in the Github repository a forked version of a repository of the model LiteralE, which models textual and numerical information from Knowledge Graphs. The files are available in the `LiteralE` folder.
- The `LiteralE` folder does not contain the original source code but a derived version. I basically changed the `preprocessing/batching.py` file in the spodernet module due to a `ValueError` on my data. 
- To understand how to import data and run experiments look up the `README.md` file inside the folder.
#### Results from DistMult with textual and numerical literals (100 epochs)
- I trained the `DistMult_text` model available in [LiteralE](https://github.com/SmartDataAnalytics/LiteralE) on `OC-55K`.
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
- I trained the `ComplEx_gate` model available in [LiteralE](https://github.com/SmartDataAnalytics/LiteralE) on `OC-55K`.
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
- Both in validation and testing the models have poorer performances in tail prediction rather than head prediction
- DistMult, with same parameters, performs better than ComplEx.
- By increasing learning rate (fro 0.001 to 0.01) the model performances did not increase.
- Two ways of preventing the models from underfitting might be to train them for more epochs or feed them with more (structural) data (e.g. by adding coauthorship links between authors).
