#!/usr/bin/env python3
"""
MNIST手写数字识别训练脚本
基于PyTorch官方示例简化版本

运行方式：python train.py
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import argparse
import os

# 超参数配置
BATCH_SIZE = 64
TEST_BATCH_SIZE = 1000
LEARNING_RATE = 0.01
MOMENTUM = 0.5
EPOCHS = 3
SEED = 1
LOG_INTERVAL = 10

# 设备配置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 使用设备: {device}")


# 简单的神经网络模型
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # MNIST图像是 28x28 单通道灰度图
        self.fc1 = nn.Linear(28 * 28, 128)  # 输入层：784 -> 128
        self.fc2 = nn.Linear(128, 64)      # 隐藏层：128 -> 64
        self.fc3 = nn.Linear(64, 10)       # 输出层：64 -> 10 (0-9 十个数字)

    def forward(self, x):
        # 展平图像 [batch, 1, 28, 28] -> [batch, 784]
        x = x.view(-1, 28 * 28)

        # 激活函数 ReLU
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))

        # 输出层（不需要softmax，CrossEntropyLoss会自动处理）
        x = self.fc3(x)
        return x


def train(model, device, train_loader, optimizer, epoch):
    """训练一个epoch"""
    model.train()
    criterion = nn.CrossEntropyLoss()

    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        # 前向传播
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)

        # 反向传播
        loss.backward()
        optimizer.step()

        if batch_idx % LOG_INTERVAL == 0:
            print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)} '
                  f'({100. * batch_idx / len(train_loader):.0f}%)]\tLoss: {loss.item():.6f}')


def test(model, device, test_loader):
    """测试模型"""
    model.eval()
    test_loss = 0
    correct = 0
    criterion = nn.CrossEntropyLoss(reduction='sum')

    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print(f'\n🧪 测试集: 平均损失: {test_loss:.4f}, '
          f'准确率: {correct}/{len(test_loader.dataset)} '
          f'({100. * correct / len(test_loader.dataset):.2f}%)\n')

    return 100. * correct / len(test_loader.dataset)


def main():
    # 设置随机种子
    torch.manual_seed(SEED)

    # 数据预处理
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST均值和标准差
    ])

    print("📥 下载MNIST数据集...")
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('./data', train=False, download=True, transform=transform)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=TEST_BATCH_SIZE, shuffle=False)

    print("🏗️  创建模型...")
    model = Net().to(device)

    print("🎯 开始训练...")
    optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=MOMENTUM)

    best_accuracy = 0
    for epoch in range(1, EPOCHS + 1):
        print(f"\n{'='*50}")
        print(f"Epoch {epoch}/{EPOCHS}")
        print(f"{'='*50}")
        train(model, device, train_loader, optimizer, epoch)
        accuracy = test(model, device, test_loader)

        # 保存最佳模型
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            torch.save(model.state_dict(), 'mnist_model.pt')
            print(f"💾 保存最佳模型 (准确率: {accuracy:.2f}%)")

    print(f"\n🎉 训练完成！最佳准确率: {best_accuracy:.2f}%")


if __name__ == '__main__':
    main()
