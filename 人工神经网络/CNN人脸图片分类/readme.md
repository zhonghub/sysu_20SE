# Readme.md

### 项目文件夹说明

```
 code
	|_______ main.py 源码
	|
	|_______ face_classification_500 图片文件夹
	|
	|_______ model_checkpoint.pth 训练好的checkpoint
	|
	|_______loss_acc.png 训练过程中训练集和验证集的Acc和loss曲线图
	
	
```



### 代码运行说明

main.py

#### 默认运行方式（测试训练好的模型，没有训练模型）：

导入训练好的checkpoint(model_checkpoint.pth)，并计算测试集正确率（在控制台输出）

```python
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 实例化模型
    model = CNN(classes, p_dropout)
    # 使用GPU
    if use_cuda:
        print("use GPU")
        model.cuda()
    else:
        print("use CPU")
    for i in range(1):
        print(i, " train:")
        lr = 0.1
        momentum = 0.7
        max_lr = 0.03
        weight_decay = 5e-4
        # 加载训练好的checkpoint, 可以在这个checkpoint上继续训练
        model.load_state_dict(torch.load('./model_checkpoint.pth'))
        # 计算测试集正确率
        test_model(model, dataloaders)
        # 训练model
        # train(model)

```

#### 训练新的模型：

注释掉加载checkpoint的语句

```python
		# 加载训练好的checkpoint, 可以在这个checkpoint上继续训练
        # model.load_state_dict(torch.load('./model_checkpoint.pth'))
        # 计算测试集正确率
        # test_model(model, dataloaders)
        # 训练model
        train(model)
```

模型训练完成后，会保存训练好的模型到'./model_checkpoint.pth'，

生成训练过程中训练集和验证集的Acc和loss曲线图（保存为loss_acc.png），

并在控制台输出测试集正确率。

#### 在训练好的模型上继续训练：

消除3句的注释注释

```python
		# 加载训练好的checkpoint, 可以在这个checkpoint上继续训练
        model.load_state_dict(torch.load('./model_checkpoint.pth'))
        # 计算测试集正确率
        test_model(model, dataloaders)
        # 训练model
        train(model)
```

