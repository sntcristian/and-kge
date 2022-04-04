# Author Name Disambiguation with Knowledge Graph Embeddings using Literals

This is the repository for the master thesis project on Knowledge Graph Embeddings for Author Name Disambiguation presented by Cristian Santini at [Digital Humanities and Digital Knowledge - University of Bologna](https://corsi.unibo.it/2cycle/DigitalHumanitiesKnowledge), with the collaboration of [Information Service Engineering - FIZ Karlsruhe](https://www.fiz-karlsruhe.de/en/forschung/information-service-engineering), in a.y. 2020/2021.

## Datasets

This repository contains notebooks and scripts used for a research on Author Name Disambiguation using Knowledge Graph Embeddings (KGEs) with literals.
Due to the unavailability of an established benchmark for evaluating our approach, we extracted two Knowledge Graphs (KGs) from the following publicly available resources: 1) a triplestore available on Zenodo [1] covering information about the journal [Scientometrics](https://www.springer.com/journal/11192) and modelled according to the [OpenCitations Data Model](https://opencitations.net/model) and 2) a publicly available benchmark for author disambiguation available [at this link](https://static.aminer.cn/misc/na-data-kdd18.zip) by [AMiner](https://www.aminer.org/). <br/>
The Knowledge Graphs extracted are available on Zenodo as [OpenCitations-782K](https://doi.org/10.5281/zenodo.5675787) [2] and [AMiner-534K](https://doi.org/10.5281/zenodo.5675801) [3]. Each dataset is organized as a collection of RDF triples stored in TSV format. Literal triples are stored separately in order to train multimodal Knowledge Graph Embedding models.<br/>
Each dataset contains a JSON file called `and_eval.json` which contains a list of publications in the scholarly KGs labelled for evaluating AND algorithms. For the evaluation, while for AMiner-534K the set of publications was already manually annotated by a team of experts, for OC-782K we used the ORCID iDs associated with the authors in the triplestore in order to create an evaluation dataset.

## [PyKEEN](https://github.com/pykeen/pykeen) extension

The `pykeen-extension` directory contains extension files compatible with [PyKEEN (Release: v1.4.0.)](https://github.com/pykeen/pykeen/releases/tag/v1.4.0). In this directory we implemented some extensions of the LiteralE model [4] which allow to train multimodal knowledge graph embeddings by also using textual information contained in entity descriptions. Details about the models and on how to install the extension files are available [in this README.md file](https://github.com/sntcristian/and-kge/blob/main/pykeen-extension/README.md).<br/>
The extended library provides an implementation of the following models:
- `DistMultText`: an extension of the DistMult model [5] for training KGEs by using entity descriptions attached to entities. 
- `ComplExText`: an extension of the ComplEx model [6] which allows to train KGEs by using information coming from short text descriptions attached to entities.
- `DistMult_gate_text`: an extension of the DistMult model which allows to train KGEs by using information coming from short text descriptions and numeric value associated with entities in KGs.<br/>
Entity descriptions are encoded by using SPECTER [7], a BERT language model for scientific documents.<br/>


## Code

Scripts used in our research are available in the `src` directory. The `disambiguation.py` file in the `src/disambiguation` folder contains the functions that we developed for carrying author name disambiguation by using knowledge graph embeddings. More specifically it contains:
- the `do_blocking()` function, which is used to preliminarily group the authors in the KG into different sub-sets by means of their last name and first initial,
- the `cluster_KGEs()` function, which takes as input the output of the `do_blocking` function and disambiguates the authors by means of Knowledge Graph Embeddings and Hierarchical Agglomerative Clustering.
- the evaluation functions that we used in our experiments.
The `src` folder also contains the various scripts used for extracting the scholarly KGs from the original sources and creating an evaluation dataset for AND.<br/>

## Results

### Knowledge Graph Embedding Evaluation

For evaluating the quality of our KGE models in representing the components of the studied KGs, **OpenCitations-782K** and **AMiner-534K**, we used entity prediction, one of the most common KG-completion tasks. In our experiments, we compared three architectures:
- A `DistMult` model trained with only structural triples, i.e. triples connecting just two entities.
- A `DistMultText` model which was trained by using titles of scholarly resources, i.e. journals and publications, along with structural triples.
- A `DistMult_gate_text` model which was trained using titles and publication dates of scholarly resources in order to leverage the representations of the entities associated with them.<br/>
Hyper-parameters were obtained by doing `hyper-parameter optimization` with PyKEEN. Details about the configuration files are available in the `kge-evaluation` folder.

The following table shows the results of our experiments for **OC-782K**.
| Model | MR | MRR | Hits@1 | Hits@3 | Hits@5 | Hits@10 |
|-------|----|-----|--------|--------|--------|---------|
| *DistMult* | **59901** | **0.3570** | 0.3157 | **0.3812** | **0.402** | **0.4267** |
| *DistMultText* | 60495 | 0.3568 | **0.3158** | 0.3809 | 0.4013 | 0.4252 |
| *DistMult_gate_text* | 61812 | 0.3534 | 0.3130 | 0.3767 | 0.3971 | 0.4218 |

The following table shows the results of our experiments for **AMiner-534K**.
| Model | MR | MRR | Hits@1 | Hits@3 | Hits@5 | Hits@10 |
|-------|----|-----|--------|--------|--------|---------|
| *DistMult* | 3585| 0.3285 | 0.1938 | 0.3996 |0.4911 | 0.5940 |
| *DistMultText* | **3474**	 | 0.3443 | **0.2139** | **0.4123** |**0.5014** | 0.6019 |
| *DistMult_gate_text* | 3560	 | **0.3452** | 0.2163 | **0.4123** | 0.5009 | **0.6028** |

### Author Name Disambiguation

We compared our architecture for Author Name Disambiguation (AND) for KGs with a simple Rule-based method inspired by Caron and Van Eck [8] on **OC-782K** and with other state-of-the-art graph embedding models on [the AMiner benchmark](https://www.aminer.org/) (results taken from [9]). The results are reported below.

| Model | Precision | Recall | F1 |
|-------|-----------|--------|----|
| *Caron & Van Eck* [8] | 84.66 | 50.20 | 63.03 |
| *DistMult* | **91.71** | 67.11 | **77.50** |
| *DistMultText* | 89.63 | 66.98 | 76.67 |
| *DistMult_gate_text* | 82.76 | **67.59** | 74.40 |

<br/>

| Model | Precision | Recall | F1 |
|-------|-----------|--------|----|
| *Zhang and Al Hasan* [10] | 70.63 | 59.53 | 62.81 |
| *Zhang et Al.* [9] |  77.96 | **63.03** |**67.79** |
| *DistMult* | **78.36** | 59.68 | 63.36 |
| *DistMultText* | 77.24 | 61.21 | 64.18 |
| *DistMult_gate_text* | 77.62 | 59.91 | 63.07 |


## References

[1] Massari, Arcangelo. (2021). Bibliographic dataset based on Scientometrics, containing provenance information compliant with the OpenCitations Data Model and non disambigued authors (1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5151264

[2] Santini, Cristian, Alam, Mehwish, Gesese, Genet Asefa, Peroni, Silvio, Gangemi, Aldo, & Sack, Harald. (2021). OC-782K: Knowledge Graph of "Scientometrics" modelled according to the OpenCitations Data Model [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5675787

[3] Santini, Cristian, Alam, Mehwish, Gesese. Genet Asefa, Peroni, Silvio, Gangemi, Aldo, & Sack, Harald. (2021). AMiner-534K: Knowledge Graph of AMiner benchmark for Author Name Disambiguation [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5675801


[4] Kristiadi A., Khan M.A., Lukovnikov D., Lehmann J., Fischer A. (2019) Incorporating Literals into Knowledge Graph Embeddings. In: Ghidini C. et al. (eds) The Semantic Web – ISWC 2019. ISWC 2019. Lecture Notes in Computer Science, vol 11778. Springer, Cham. [https://doi.org/10.1007/978-3-030-30793-6_20](https://doi.org/10.1007/978-3-030-30793-6_20).

[5] Yang, B., Yih, W., He, X., Gao, J., & Deng, L. (2015). Embedding Entities and Relations for Learning and Inference in Knowledge Bases. ArXiv:1412.6575 [Cs]. http://arxiv.org/abs/1412.6575

[6] Trouillon, T., Welbl, J., Riedel, S., Gaussier, É., & Bouchard, G. (2016). Complex Embeddings for Simple Link Prediction. ArXiv:1606.06357 [Cs, Stat]. http://arxiv.org/abs/1606.06357

[7] Cohan, A., Feldman, S., Beltagy, I., Downey, D., & Weld, D. S. (2020). SPECTER: Document-level Representation Learning using Citation-informed Transformers. ArXiv:2004.07180 [Cs]. http://arxiv.org/abs/2004.07180

[8] Caron, E., & van Eck, N.-J. (2014). Large scale author name disambiguation using rule-based scoring and clustering: International conference on science and technology indicators. Proceedings of the Science and Technology Indicators Conference 2014, 79–86. http://sti2014.cwts.nl

[9] Zhang, Y., Zhang, F., Yao, P., & Tang, J. (2018). Name Disambiguation in AMiner: Clustering, Maintenance, and Human in the Loop. Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 1002–1011. https://doi.org/10.1145/3219819.3219859

[10] Zhang, B., & Al Hasan, M. (2017). Name Disambiguation in Anonymized Graphs using Network Embedding. Proceedings of the 2017 ACM on Conference on Information and Knowledge Management, 1239–1248. https://doi.org/10.1145/3132847.3132873

## Citation

@article{corr/abs-2201-09555, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;author    = {Cristian Santini and
               Genet Asefa Gesese and 
               Silvio Peroni and 
               Aldo Gangemi and
               Harald Sack and
               Mehwish Alam}, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;title     = {A Knowledge Graph Embeddings based Approach for Author Name Disambiguation
               using Literals}, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;journal   = {CoRR}, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;volume    = {abs/2201.09555}, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;year      = {2022}, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;url       = {https://arxiv.org/abs/2201.09555}, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;eprinttype = {arXiv}, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;eprint    = {2201.09555}  <br/>
}

 
## Acknowledgments

The software and data here available are the result of a master thesis carried in collaboration between the [FICLIT department](https://ficlit.unibo.it/it) of the University of Bologna and the research department [FIZ - Information Service Engineering (ISE)](https://www.fiz-karlsruhe.de/index.php/en/forschung/information-service-engineering) of the Karlsruhe Institute of Technology (KIT).	

