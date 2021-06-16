<h1>Pykeen Multimodal Extension</h1>

This folder contains some extension files of [pykeen (Release: v1.4.0.)](https://github.com/pykeen/pykeen/releases/tag/v1.4.0)

## To start
In order to run the extension files of pykeen download the 1.4.0 release of pykeen, by means of:

```
$ git clone https://github.com/pykeen/pykeen.git
```
Once you have cloned the repository, execute the following steps:
1. Go inside the `pykeen/src/models/` folder and overwrite the `multimodal` directory with the one contained in this folder.
2. Go in `pykeen/src` and overwrite the `triples` folder with the `triples` directory of this folder.
3. Once you have executed these steps, open your command line inside your pykeen folder and install the library by using:

```
$ cd pykeen
$ pip install -e .
```
In order to use our models which support text literals, make sure to also have installed the `sentence-transformers` library.

```
!pip install sentence-transformers
```
## Extensions:
In this modified version of [pykeen v1.4.0](https://github.com/pykeen/pykeen/releases/tag/v1.4.0), we introduced three new models: `DistMultText`, `ComplExText` and `DistMult_gate_text` , all extension of the LiteralE model which allow to train knowledge graph embeddings by means of structural and literal information. The LiteralE model was firstly introduced in ([Kristiadi, 2018](https://arxiv.org/abs/1802.00934)) and a previous implementation of LiteralE, with DistMult and ComplEx as base for the scoring functions, was previously introduced in [https://github.com/SmartDataAnalytics/LiteralE](https://github.com/SmartDataAnalytics/LiteralE).<br/>
In this extension of Pykeen we provided two models, `DistMultText` and `ComplExText`, which use textual literal labels attached to entities to train Knowledge Graph Embeddings by means of a linear transformation which combines the entity representation with the corresponding literal information.<br/>
The third model is `DistMult_gate_text`, an extension of the DistMult model which allows to train knowledge graph embeddings by using both textual and numerical information attached to entities. The way it combines these representations is by using a *gated recurrent unit* (GRU), as described in ([Kristiadi, 2018](https://arxiv.org/abs/1802.00934)).<br/>

In order to implement our models we introduced two classes: `TriplesTextualLiteralsFactory` and `TriplesLiteralsFactory` which models textual labels associated to entities by means of **allenai-specter** a BERT language model pre-trained on scholarly literature. `TriplesLiteralsFactory` returns also a matrix of numerical vectors, provided that they are given as input in TSV or array of triples, as in the Pykeen class `TriplesNumericLiteralsFactory`.

## Credits
This is an extension of [pykeen v.1.4.0](https://github.com/pykeen/pykeen).<br/>
The implementation of the model `DistMultText`, `ComplExText` and `DistMult_gate_text` was inspired by a previous implementation of the LiteralE model in [https://github.com/SmartDataAnalytics/LiteralE](https://github.com/SmartDataAnalytics/LiteralE).

## References

Kristiadi A., Khan M.A., Lukovnikov D., Lehmann J., Fischer A. (2019) Incorporating Literals into Knowledge Graph Embeddings. In: Ghidini C. et al. (eds) The Semantic Web – ISWC 2019. ISWC 2019. Lecture Notes in Computer Science, vol 11778. Springer, Cham. [https://doi.org/10.1007/978-3-030-30793-6_20](https://doi.org/10.1007/978-3-030-30793-6_20).
