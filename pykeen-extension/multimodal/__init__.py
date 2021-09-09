# -*- coding: utf-8 -*-

"""Multimodal KGE Models.

.. [kristiadi2018] Kristiadi, A.., *et al.* (2018) `Incorporating literals into knowledge graph embeddings.
   <https://arxiv.org/abs/1802.00934>`_. *arXiv*, 1802.00934.
"""

from .complex_literal import ComplExLiteral
from .complex_text import ComplExText
from .distmult_literal import DistMultLiteral
from .distmult_gate_text import DistMult_gate_text
from .distmult_text import DistMultText

__all__ = [
    'ComplExLiteral',
    'DistMultLiteral',
    'DistMult_gate_text'
    'ComplExText'
    'DistMultText'
]
