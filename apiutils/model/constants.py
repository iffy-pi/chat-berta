import torch
MAX_LENGTH = 512
BATCH_SIZE = 4
GRAD_ACCUMULATION = 8
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"