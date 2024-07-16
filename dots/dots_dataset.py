import torch as t
from torch.utils.data import Dataset
import numpy as np
import os


class DotsDataset(Dataset):
    def __init__(self, root_dir='path/', train=True):
        # to load train set
        if train:
            X = np.load(os.path.join(root_dir, 'X_train.npy'))
            y = np.load(os.path.join(root_dir, 'y_train.npy'))
        # to load test set
        else:
            X = np.load(os.path.join(root_dir, 'X_test.npy'))
            y = np.load(os.path.join(root_dir, 'y_test.npy'))
        
        # map [3,4,5,6,7,8] to [0,1,2,3,4,5]
        y = y - 3

        self.X = t.tensor(X, dtype=t.float64)
        self.y = t.tensor(y, dtype=t.long)

    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx] # (res,2) , (1,)