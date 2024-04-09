import os

train_path = os.path.join('../train')
test_path = os.path.join('../test')
val_path = os.path.join('../val')

try:
    os.makedirs(train_path)
    os.makedirs(test_path)
    os.makedirs(val_path)
except:
    pass

train_words = os.listdir(train_path)
train_mapping = {i: word for i, word in enumerate(train_words)}

test_words = os.listdir(test_path)
test_mapping = {i: word for i, word in enumerate(test_words)}

val_words = os.listdir(val_path)
val_mapping = {i: word for i, word in enumerate(val_words)}
