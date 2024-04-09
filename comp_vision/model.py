import torch as torch
from torch.nn import ReLU, LSTM, Linear

from comp_vision import train_mapping
from comp_vision.dataloaders import train_dataloader, test_dataloader, val_dataloader, train_labels_len


class Model(torch.nn.Module):

    def __init__(self, nr_classes):
        super(Model, self).__init__()
        self.LSTM1 = LSTM(126, hidden_size=512, batch_first=True)
        self.LSTM2 = LSTM(512, hidden_size=128, batch_first=True)
        self.LSTM3 = LSTM(128, hidden_size=64, batch_first=True)
        self.Dense1 = Linear(64, 64)
        self.Dense2 = Linear(64, 32)
        self.Dense3 = Linear(32, nr_classes)
        self.relu = ReLU()

    def forward(self, x):
        x, _ = self.LSTM1(x)
        x = self.relu(x)
        x, _ = self.LSTM2(x)
        x = self.relu(x)
        x, _ = self.LSTM3(x)
        x = self.relu(x)
        x = self.relu(self.Dense1(x[:, -1, :]))
        x = self.relu(self.Dense2(x))
        x = self.Dense3(x)
        return x

    def train_model(self):
        num_epochs = 100
        optimizer = torch.optim.Adam(self.parameters(), lr=0.01)
        criterion = torch.nn.CrossEntropyLoss()
        for epoch in range(num_epochs):
            self.train(True)
            running_loss = 0.0
            correct = 0
            total = 0

            for batch in train_dataloader:
                inputs, labels = batch
                inputs = inputs.type(torch.FloatTensor)
                optimizer.zero_grad()

                outputs = self(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()

                _, predicted = torch.max(outputs, dim=1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)

            train_loss = running_loss / len(train_dataloader)
            train_acc = correct / total
            print(f'epoch {epoch} with loss {train_loss} and acc {train_acc}')

            # self.val_model()

    def predict(self, inputs):
        self.eval()
        with torch.no_grad():
            outputs = self(inputs)
            _, predicted = torch.max(outputs, dim=1)
            label = train_mapping[predicted]
            return label

    def test_model(self):
        criterion = torch.nn.CrossEntropyLoss()
        self.eval()

        with torch.no_grad():
            running_loss = 0.0
            correct = 0
            total = 0
            for batch in test_dataloader:
                inputs, labels = batch

                outputs = self(inputs)
                _, predicted = torch.argmax(outputs, dim=1)
                loss = criterion(outputs, torch.tensor(labels))
                running_loss += loss.item()
                correct += (predicted == labels).sum().item()
                total += labels.size(0)
            loss = running_loss / len(test_dataloader)
            test_acc = correct / total
            print(f'test loss {loss}, acc {test_acc}')

    def val_model(self):
        criterion = torch.nn.CrossEntropyLoss()
        self.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for batch in val_dataloader:
                inputs, labels = batch
                inputs = inputs.type(torch.FloatTensor)

                outputs = self(inputs)
                predicted = torch.argmax(outputs, dim=1)
                loss = criterion(outputs, torch.tensor(labels))
                running_loss += loss.item()
                correct += (predicted == labels).sum().item()
                total += labels.size(0)
            loss = running_loss / len(val_dataloader)
            val_acc = correct / total
            print(f'val loss {loss}, acc {val_acc}')


if __name__ == '__main__':
    model = Model(train_labels_len)
    model.train_model()
