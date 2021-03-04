import torch.nn as nn
import torch
from pytorch_lightning.metrics.utils import to_onehot

class KeywordsLoss(nn.Module):
    def __init__(self, alpha=0.9, loss_fct='kldiv'):
        super().__init__()
        self.alpha = alpha
        if loss_fct == 'kldiv':
            self.criterion = nn.KLDivLoss(reduction='batchmean')
        elif loss_fct == 'mse':
            self.criterion = nn.MSELoss()

    def forward(self, logits:torch.tensor, keywords: torch.tensor):
        """calculate keyword loss

        Args:
            logits (torch.tensor): B, S2, V
            keywords (torch.tensor): B, S1
        """
        logits = nn.functional.gelu(logits)
        logits = logits.mean(1)
        logits = torch.log_softmax(logits,  -1)

        mask = (keywords != 101) & ( keywords != 102) & (keywords != 117) & ( keywords != 120)
        kws = keywords.detach().clone()
        kws[~mask] = 0

        # B, vocab_size
        kw_matrix = torch.zeros((logits.shape[0], logits.shape[-1])).to(logits.device)
        for i, row in enumerate(kws):
            kw_matrix[i, :] = 1 - self.alpha
            kw_matrix[i, row] = self.alpha
        # print(kw_matrix)
        kw_matrix = torch.softmax(kw_matrix, -1)
        kw_matrix.requires_grad = False
        # print(kw_matrix)

        return self.criterion(logits, kw_matrix)


if __name__ == '__main__':
    kw_loss_fct = KeywordsLoss()
    logits = torch.rand((4, 5, 10))
    kw = torch.randint(0, 10, (4, 10))
    print(kw_loss_fct(logits, kw))
