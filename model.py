import torch
import torch.nn as nn

class model(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(242, 4)

    def forward(self, x):
        return self.linear(x.flatten())