# Author Name Disambiguation with Knowledge Graph Embeddings using Literals

This is the repository for the master thesis project on Knowledge Graph Embeddings (KGEs) for Author Name Disambiguation presented by Cristian Santini at [Digital Humanities and Digital Knowledge - University of Bologna](https://corsi.unibo.it/2cycle/DigitalHumanitiesKnowledge), with the collaboration of [Information Service Engineering - FIZ Karlsruhe](https://www.fiz-karlsruhe.de/en/forschung/information-service-engineering), in a.y. 2020/2021.

## Datasets

This repository contains notebooks and scripts used for a research on Author Name Disambiguation using Knowledge Graph Embeddings (KGEs) with literals.
Due to the unavailability of an established benchmark for evaluating our approach, we extracted two Knowledge Graphs (KGs) from the following publicly available resources: 1) a triplestore available on [Zenodo](https://doi.org/10.5281/zenodo.5151264) covering information about the journal [Scientometrics](https://www.springer.com/journal/11192) and modelled according to the [OpenCitations Data Model](https://opencitations.net/model) and 2) a publicly available benchmark for author disambiguation made available [here](https://static.aminer.cn/misc/na-data-kdd18.zip) by [AMiner](https://www.aminer.org/). The Knowledge Graphs extracted are called **OpenCitations-782K** [1] and **AMiner-534K** [2]. The files and statistics of these datasets are publicly available on Zenodo.<br/>
For the evaluation, while for AMiner-534K the set of publications was already manually annotated by a team of experts for name disambiguation, for OC-782K we used the ORCID iDs associated with the authors in the triplestore in order to create an evaluation dataset.

## [PyKEEN](https://github.com/pykeen/pykeen) extension

The `pykeen-extension` directory contains extension files compatible with [PyKEEN (Release: v1.4.0.)](https://github.com/pykeen/pykeen/releases/tag/v1.4.0). In this directory we implemented some extensions of the LiteralE model [5] which allow to train multimodal knowledge graph embeddings by also using textual information contained in entity descriptions. Details about the models and on how to install the extension files are available [here](https://github.com/sntcristian/and-kge/blob/main/pykeen-extension/README.md).<br/>


## Code

Scripts used in our research are available in the `src` directory. The `disambiguation.py` file in the `src/disambiguation` folder contains the functions that we developed for carrying author name disambiguation by using knowledge graph embeddings. More specifically it contains:
- the `do_blocking()` function, which is used to preliminarily group the authors in the KG into different sub-sets by means of their last name and first initial,
- the `cluster_KGEs()` function, which takes as input the output of the `do_blocking` function and disambiguates the authors by means of Knowledge Graph Embeddings and Hierarchical Agglomerative Clustering.
- the evaluation functions that we used in our experiments.
The `src` folder also contains the various scripts used for extracting the scholarly KGs from the original sources and creating an evaluation dataset for AND.<br/>

## Results
### Knowledge Graph Embedding Evaluation

### Author Name Disambiguation

## References

[1] Santini, Cristian, Alam, Mehwish, Gesese, Genet Asefa, Peroni, Silvio, Gangemi, Aldo, & Sack, Harald. (2021). OC-782K: Knowledge Graph of "Scientometrics" modelled according to the OpenCitations Data Model [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5675787

[2] Santini, Cristian, Alam, Mehwish, Gesese. Genet Asefa, Peroni, Silvio, Gangemi, Aldo, & Sack, Harald. (2021). AMiner-534K: Knowledge Graph of AMiner benchmark for Author Name Disambiguation [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5675801


[3] Kristiadi A., Khan M.A., Lukovnikov D., Lehmann J., Fischer A. (2019) Incorporating Literals into Knowledge Graph Embeddings. In: Ghidini C. et al. (eds) The Semantic Web – ISWC 2019. ISWC 2019. Lecture Notes in Computer Science, vol 11778. Springer, Cham. [https://doi.org/10.1007/978-3-030-30793-6_20](https://doi.org/10.1007/978-3-030-30793-6_20).

## Acknowledgments

The software and data here available are the result of a master thesis collaboration between the [FICLIT department](https://ficlit.unibo.it/it) of the University of Bologna and the research department [FIZ - Information Service Engineering (ISE)](https://www.fiz-karlsruhe.de/index.php/en/forschung/information-service-engineering) of the Karlsruhe Institute of Technology (KIT). The thesis has been supervised by Prof. Aldo Gangemi and Prof. Silvio Peroni from the University of Bologna, and Prof. Harald Sack, Dr. Mehwish Alam and Genet Asefa Gesese from FIZ-ISE.		

