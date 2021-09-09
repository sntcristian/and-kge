import logging
from typing import Dict, Optional, TextIO, Tuple, Union
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm
import torch

from .instances import MultimodalLCWAInstances, MultimodalSLCWAInstances
from .triples_factory import TriplesFactory
from .utils import load_triples
from ..typing import EntityMapping, LabeledTriples

__all__ = [
    'TriplesTextualLiteralsFactory',
]

logger = logging.getLogger(__name__)


def create_matrix_of_txt_literals(
    textual_triples: np.array,
    entity_to_id: EntityMapping,
) -> np.ndarray:
    # Prepare literal matrix, set every literal to zero, and afterwards fill in the corresponding value if available
    txt_literals = np.zeros([len(entity_to_id), 768], dtype=np.float32)
    model = SentenceTransformer('allenai-specter')
    # TODO vectorize code
    pbar = tqdm(len(textual_triples))
    for h, r, lit in textual_triples:
        try:
            sentences = [lit]
            embeddings = model.encode(sentences)
            # row define entity, and column the literal. Set the corresponding literal for the entity
            txt_literals[entity_to_id[h], :] = embeddings[0]
        except KeyError:
            logger.info("Either entity or relation to literal doesn't exist.")
            continue
        pbar.update(1)
    pbar.close()

    return txt_literals


class TriplesTextualLiteralsFactory(TriplesFactory):
    """Create multi-modal instances given the path to triples."""

    def __init__(
        self,
        *,
        path: Union[None, str, TextIO] = None,
        triples: Optional[LabeledTriples] = None,
        path_to_textual_triples: Union[None, str, TextIO] = None,
        textual_triples: Optional[np.ndarray] = None,
        path_to_textual_embeddings: Union[None, str, TextIO] = None,
        save_literals: bool = False,
        **kwargs
    ) -> None:
        if path is None:
            base = TriplesFactory.from_labeled_triples(triples=triples, **kwargs)
        else:
            base = TriplesFactory.from_path(path=path, **kwargs)
        super().__init__(
            entity_to_id=base.entity_to_id,
            relation_to_id=base.relation_to_id,
            mapped_triples=base.mapped_triples,
            create_inverse_triples=base.create_inverse_triples,
        )
        assert self.entity_to_id is not None
        if path_to_textual_embeddings is not None:
            self.textual_literals = np.load(path_to_textual_embeddings)
        else:
            if path_to_textual_triples is None and textual_triples is None:
                raise ValueError('Must specify one of path_to_textual_triples or textual_triples')
            elif path_to_textual_triples is not None and textual_triples is not None:
                raise ValueError('Must not specify both path_to_textual_triples and textual_triples')
            elif path_to_textual_triples is not None:
                textual_triples = load_triples(path_to_textual_triples)
            self.textual_literals = create_matrix_of_txt_literals(
                textual_triples=textual_triples,
                entity_to_id=self.entity_to_id,
            )
        if save_literals == True:
            np.save("textual_literals.npy", self.textual_literals)

    def extra_repr(self) -> str:  # noqa: D102
        return super().extra_repr() + (
            f"num_num_literals={len(self.entity_to_id)}"
        )

    def create_slcwa_instances(self) -> MultimodalSLCWAInstances:
        """Create multi-modal sLCWA instances for this factory's triples."""
        slcwa_instances = super().create_slcwa_instances()
        return MultimodalSLCWAInstances(
            mapped_triples=slcwa_instances.mapped_triples,
            numeric_literals=None,
            textual_literals=self.textual_literals
        )

    def create_lcwa_instances(self, use_tqdm: Optional[bool] = None) -> MultimodalLCWAInstances:
        """Create multi-modal LCWA instances for this factory's triples."""
        lcwa_instances = super().create_lcwa_instances(use_tqdm=use_tqdm)
        return MultimodalLCWAInstances(
            pairs=lcwa_instances.pairs,
            compressed=lcwa_instances.compressed,
            numeric_literals=None,
            textual_literals=self.textual_literals
        )
