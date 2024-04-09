import os.path

import numpy as np
import torch.utils.data


class WLASLDataset(torch.utils.data.Dataset):

    def __init__(self, split_name='train'):
        self.X = []
        self.Y = []

        split_dir = os.path.join(f'../{split_name}')
        words = os.listdir(split_dir)

        words_mapping = {word: i for i, word in enumerate(words)}

        for word in words:
            word_dir = os.path.join(split_dir, word)
            video_ids = os.listdir(word_dir)
            for video_id in video_ids:
                file_path = os.path.join(split_dir, word, video_id)
                keypoints = np.load(file_path)
                self.X.append(keypoints)
                self.Y.append(words_mapping[word])

    def __len__(self):
        return len(np.unique(self.Y)) if self.Y else 0

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]
