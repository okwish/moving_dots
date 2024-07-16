import torch as t
from torch.utils.data import Dataset
import numpy as np
import os


class MovingDotsDataset(Dataset):
    def __init__(self, root_dir='path/', train=True):
        # to load train set
        if train:
            X = np.load(os.path.join(root_dir, 'X_train.npy'))
            y = np.load(os.path.join(root_dir, 'y_train.npy'))
        # to load test set
        else:
            X = np.load(os.path.join(root_dir, 'X_test.npy'))
            y = np.load(os.path.join(root_dir, 'y_test.npy'))
        

        self.X = t.tensor(X, dtype=t.float64) # (n, n_frames, n_dots, 2)
        self.y = t.tensor(y, dtype=t.long) # (n,)

    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, idx):
        return self.X[idx].reshape(-1,2), self.y[idx] # (n_frames*n_dots, 2) , (1,)