import torch
from torch import nn


class NPairsLoss(nn.Module):

    def __init__(self, params):
        super(NPairsLoss, self).__init__()
        self.params = params

    def forward(self, r1, r2):
        """
        Computes the N-Pairs Loss between the r1 and r2 representations.
        :param r1: Tensor of shape (batch_size, representation_size)
        :param r2: Tensor of shape (batch_size, representation_size)
        :return: the scalar loss
        """

        scores = torch.matmul(r1, r2.t())
        diagonal_mean = torch.mean(torch.diag(scores))
        mean_log_row_sum_exp = torch.mean(torch.logsumexp(scores, dim=1))
        return -diagonal_mean + mean_log_row_sum_exp


