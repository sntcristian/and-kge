<h1>Pykeen-AND</h1>
This folder contains some extension files of [pykeen v.1.4.1-dev](https://github.com/pykeen/pykeen).
# To start
In order to install to run the extension files of pykeen: <br/>
1. Clone the latest release of pykeen, by means of:

```
$ git clone https://github.com/pykeen/pykeen.git
```
2. Go inside the `pykeen/src/models/` folder and overwrite the `multimodal` directory with the one contained in this folder.
3. Go in `pykeen/src` and overwrite the `triples` folder with the `triples` directory of this folder.
4. Once you have overwritten the original files in the pykeen repository, open your command line inside your pykeen folder and install the dependencies by using:

```
$ cd pykeen
$ pip install -e .
```
5. In order to use our models which support text literals, make sure to also have installed the `sentence-transformers` library.

```
!pip install sentence-transformers
```
# Modifications:
In this modified version of [pykeen v.1.4.1-dev](https://github.com/pykeen/pykeen), we introduced a new model, `DistMultText`, which allows to train knowledge graph embeddings by making entity representations interact with embeddings derived from corresponding labels via a linear transformation. This model was firstly introduced in ([Kristiadi, 2018](https://arxiv.org/abs/1802.00934)). Source code of the model [here]().<br/>
In order to implement our model we introduced the class `TriplesTextualLiteralsFactory` which models textual labels associated to entities by means of **allenai-specter** a BERT language model pre-trained on scholarly literature. You can see the implementation of this class [here]().

# Credits
This is an extension of [pykeen v.1.4.1-dev](https://github.com/pykeen/pykeen).<br/>
The implementation of the model `DistMultText` and the preprocessing class `TriplesTextualLiteralsFactory` was inspired by a previous implementation of the LiteralE model in [https://github.com/SmartDataAnalytics/LiteralE](https://github.com/SmartDataAnalytics/LiteralE).

# References

Kristiadi A., Khan M.A., Lukovnikov D., Lehmann J., Fischer A. (2019) Incorporating Literals into Knowledge Graph Embeddings. In: Ghidini C. et al. (eds) The Semantic Web – ISWC 2019. ISWC 2019. Lecture Notes in Computer Science, vol 11778. Springer, Cham. [https://doi.org/10.1007/978-3-030-30793-6_20](https://doi.org/10.1007/978-3-030-30793-6_20).
