# -*- coding: utf-8 -*-

"""Implementation of the DistMultLiteral model."""

from typing import Any, ClassVar, Mapping, Optional

import torch
import torch.nn as nn
from torch.nn import functional as F, Parameter

from ..base import MultimodalModel
from ..unimodal.distmult import DistMult
from ...constants import DEFAULT_DROPOUT_HPO_RANGE, DEFAULT_EMBEDDING_HPO_EMBEDDING_DIM_RANGE
from ...losses import Loss
from ...nn import Embedding
from ...regularizers import Regularizer
from ...triples import TriplesLiteralsFactory
from ...typing import DeviceHint


class GateMulti(nn.Module):

    def __init__(self, emb_size, num_lit_size, txt_lit_size, gate_activation=nn.functional.sigmoid):
        super(GateMulti, self).__init__()

        self.emb_size = emb_size
        self.num_lit_size = num_lit_size
        self.txt_lit_size = txt_lit_size

        self.gate_activation = gate_activation
        self.g = nn.Linear(emb_size+num_lit_size+txt_lit_size, emb_size)

        self.gate_ent = nn.Linear(emb_size, emb_size, bias=False)
        self.gate_num_lit = nn.Linear(num_lit_size, emb_size, bias=False)
        self.gate_txt_lit = nn.Linear(txt_lit_size, emb_size, bias=False)
        self.gate_bias = nn.Parameter(torch.zeros(emb_size))

    def forward(self, x_ent, x_lit_num, x_lit_txt):
        x = torch.cat([x_ent, x_lit_num, x_lit_txt], 1)
        g_embedded = F.tanh(self.g(x))
        gate = self.gate_activation(self.gate_ent(x_ent) + self.gate_num_lit(x_lit_num) + self.gate_txt_lit(x_lit_txt) + self.gate_bias)
        output = (1-gate) * x_ent + gate * g_embedded

        return output


class DistMult_gate_text(DistMult, MultimodalModel):
    """An implementation of DistMultLiteral from [kristiadi2018]_.

    ---
    citation:
        author: Kristiadi
        year: 2018
        link: https://arxiv.org/abs/1802.00934
    """

    #: The default strategy for optimizing the model's hyper-parameters
    hpo_default: ClassVar[Mapping[str, Any]] = dict(
        embedding_dim=DEFAULT_EMBEDDING_HPO_EMBEDDING_DIM_RANGE,
        input_dropout=DEFAULT_DROPOUT_HPO_RANGE,
    )
    #: The default parameters for the default loss function class
    loss_default_kwargs: ClassVar[Mapping[str, Any]] = dict(margin=0.0)

    def __init__(
        self,
        triples_factory: TriplesLiteralsFactory,
        embedding_dim: int = 50,
        input_dropout: float = 0.0,
        loss: Optional[Loss] = None,
        regularizer: Optional[Regularizer] = None,
        preferred_device: DeviceHint = None,
        random_seed: Optional[int] = None,
    ) -> None:
        super().__init__(
            triples_factory=triples_factory,
            embedding_dim=embedding_dim,
            loss=loss,
            preferred_device=preferred_device,
            random_seed=random_seed,
            regularizer=regularizer,
        )

        # Literal
        # num_ent x num_lit
        self.numeric_literals = Embedding(
            num_embeddings=triples_factory.num_entities,
            embedding_dim=triples_factory.numeric_literals.shape[-1],
            initializer=triples_factory.numeric_literals,
        )
        self.textual_literals = Embedding(
            num_embeddings=triples_factory.num_entities,
            embedding_dim=triples_factory.textual_literals.shape[-1],
            initializer=triples_factory.textual_literals,
        )

        self.num_lit_dim = self.numeric_literals.embedding_dim
        self.txt_lit_dim = self.textual_literals.embedding_dim
        self.emb_lit = GateMulti(self.embedding_dim, self.num_lit_dim, self.txt_lit_dim)
        self.inp_drop = torch.nn.Dropout(input_dropout)

    def _get_entity_representations(
        self,
        idx: torch.LongTensor,
    ) -> torch.FloatTensor:
        emb = self.entity_embeddings.get_in_canonical_shape(indices=idx)
        num_lit = self.numeric_literals.get_in_canonical_shape(indices=idx)
        txt_lit = self.textual_literals.get_in_canonical_shape(indices=idx)
        x = self.emb_lit.forward(emb, num_lit, txt_lit)
        return self.inp_drop(x)

    def forward(
        self,
        h_indices: Optional[torch.LongTensor],
        r_indices: Optional[torch.LongTensor],
        t_indices: Optional[torch.LongTensor],
    ) -> torch.FloatTensor:  # noqa: D102
        # TODO: this is very similar to ComplExLiteral, except a few dropout differences
        h = self._get_entity_representations(idx=h_indices)
        r = self.relation_embeddings.get_in_canonical_shape(indices=r_indices)
        t = self._get_entity_representations(idx=t_indices)
        return self.interaction_function(h=h, r=r, t=t)
