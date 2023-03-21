import torch

class SamSumDataset(torch.utils.data.Dataset):
    def __init__(self, input_ids, attention_mask, labels):
        self.attention_mask = attention_mask
        self.input_ids = input_ids
        self.labels = labels

    def __getitem__(self, idx):
        item = {"input_ids": self.input_ids[idx]}
        item["attention_mask"] = self.attention_mask[idx]
        item["labels"] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)