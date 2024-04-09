import torch.utils.data

from comp_vision.custom_dataset import WLASLDataset


def get_nr_labels(dataloader):
    dataset = dataloader.dataset
    return len(dataset)


train_data = WLASLDataset(split_name='train')
train_dataloader = torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True)
train_labels_len = get_nr_labels(train_dataloader)

test_data = WLASLDataset(split_name='test')
test_dataloader = torch.utils.data.DataLoader(test_data, batch_size=32, shuffle=True)
test_labels_len = get_nr_labels(test_dataloader)

val_data = WLASLDataset(split_name='val')
val_dataloader = torch.utils.data.DataLoader(val_data, batch_size=32, shuffle=True)
val_labels_len = get_nr_labels(val_dataloader)
