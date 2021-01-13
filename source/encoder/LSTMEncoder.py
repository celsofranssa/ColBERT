import torch.nn
from pytorch_lightning import LightningModule
from torch import nn

from source.model.AveragePooling import AveragePooling
from source.model.MaxPooling import MaxPooling


class LSTMEncoder(LightningModule):
    """Encodes the input as embedding. Url article: https://guxd.github.io/papers/deepcs.pdf"""

    def __init__(self, hparams):
        """Set the network paramets."""
        super(LSTMEncoder, self).__init__()

        self.embedding = nn.Embedding(
            num_embeddings=hparams.vocabulary_size,
            embedding_dim=hparams.representation_size
        )

        self.lstm = torch.nn.LSTM(
            input_size=hparams.representation_size,
            hidden_size=hparams.hidden_size,
            batch_first=True,
            bidirectional=True)

        self.pool = MaxPooling()

    def forward(self, x):
        attention_mask = (x > 0).int()
        outputs = self.embedding(x)
        outputs, _ = self.lstm(outputs)
        return self.pool(attention_mask, outputs)
