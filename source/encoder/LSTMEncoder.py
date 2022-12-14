import torch.nn
from pytorch_lightning import LightningModule
from torch import nn

from source.encoder.EncoderOutput import EncoderOutput


class LSTMEncoder(LightningModule):
    """Encodes the input as embeddings."""

    def __init__(self, vocabulary_size, representation_size, hidden_size, pooling):
        super(LSTMEncoder, self).__init__()

        self.embedding = nn.Embedding(
            num_embeddings=vocabulary_size,
            embedding_dim=representation_size
        )

        self.lstm = torch.nn.LSTM(
            input_size=representation_size,
            hidden_size=hidden_size,
            batch_first=True,
            bidirectional=True)

        self.linear = nn.Linear(2 * representation_size, representation_size)

        self.pooling = pooling

    def forward(self, x):
        attention_mask = (x > 1).int()
        emb_outs = self.embedding(x)
        last_hidden_state, pooler_output = self.lstm(emb_outs)

        last_hidden_state = self.linear(last_hidden_state)

        return self.pooling(
            attention_mask,
            EncoderOutput(last_hidden_state, pooler_output)
        )
