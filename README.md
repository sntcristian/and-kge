# Author Name Disambiguation with Knowledge Graph Embeddings

This is the repository for the master thesis project on Knowledge Graph Embeddings for Author Name Disambiguation presented by Cristian Santini at [Digital Humanities and Digital Knowledge - University of Bologna](https://corsi.unibo.it/2cycle/DigitalHumanitiesKnowledge), with the collaboration of [Information Service Engineering - FIZ Karlsruhe](https://www.fiz-karlsruhe.de/en/forschung/information-service-engineering), in a.y. 2020/2021.

## Datasets

This repository contains notebooks and scripts used for a research on Author Name Disambiguation using Knowledge Graph Embeddings (KGEs) with literals.<br/>
For this research, we developed two newly collected scholarly Knowledge Graphs: **OpenCitations-782K** [1] and **AMiner-534K** [2].
- OpenCitations-782K is a KG covering information about the journal *Scientometrics* and modelled according to the OpenCitations Data Model [3]. Literal triples are stored separately.
- AMiner-534K is a KG extracted from a well-known author name disambiguation benchmark made publicly available by AMiner [4]. Literals are stored separately.

## Summary

This repository contains all the scripts and pieces of code used for our research in order to maximize the riproducibility of our methodology. <br/>
The `open-citations` and `aminer` folders contain all the scripts used for generating the scholarly knowledge graph studied, along with the configuration files for training KGEs on these datasets and the results of the models on entity prediction.<br/>
The `pykeen-extension` directory contains an extension of [pykeen (Release: v1.4.0.)](https://github.com/pykeen/pykeen/releases/tag/v1.4.0). In this directory we implemented three new models: `DistMultText`, `ComplExText` and `DistMult_gate_text` , all extension of the LiteralE model which allow to train knowledge graph embeddings by means of structural and literal information [5]. More details are available in the `README.md` file of the directory.<br/>
The `author-disambiguation` directory contains `disambiguation` module, with all the functions used to perform author name disambiguation with KGEs and evaluate the performances of the models. The directory contains also the results of the evaluation that we carried in our research.

## References

[1] Santini, Cristian. (2021). OC-782K: Knowledge Graph of "Scientometrics" modelled according to the OpenCitations Data Model [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5569438

[2] Santini, Cristian. (2021). AMiner-534K - Dataset [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5565220

[3] Daquino, M., Peroni, S., Shotton, D., Colavizza, G., Ghavimi, B., Lauscher, A., Mayr, P., Romanello, M., & Zumstein, P. (2020). The OpenCitations Data Model. arXiv:2005.11981 [cs]. http://arxiv.org/abs/2005.11981

[4] https://static.aminer.cn/misc/na-data-kdd18.zip

[5] Kristiadi A., Khan M.A., Lukovnikov D., Lehmann J., Fischer A. (2019) Incorporating Literals into Knowledge Graph Embeddings. In: Ghidini C. et al. (eds) The Semantic Web – ISWC 2019. ISWC 2019. Lecture Notes in Computer Science, vol 11778. Springer, Cham. [https://doi.org/10.1007/978-3-030-30793-6_20](https://doi.org/10.1007/978-3-030-30793-6_20).

## Affiliation 

[Digital Humanities and Digital Knowledge - University of Bologna](https://corsi.unibo.it/2cycle/DigitalHumanitiesKnowledge)<br/>
[Information Service Engineering - FIZ Karlsruhe](https://www.fiz-karlsruhe.de/en/forschung/information-service-engineering)

