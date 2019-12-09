💡

#### 区块链概念理解

#### 使用:

1.启动两个节点，分别坚听不同端口，也可以在不同的机器上运行

```python
python web/web_app.py -p 7777
python web/web_app.py -p 7778
```

2.查看各节点的祖先区块

访问路由: `/chain`

![](https://tva1.sinaimg.cn/large/006tNbRwly1g9qhfpffs9j31qc0pkad8.jpg)

![](https://tva1.sinaimg.cn/large/006tNbRwly1g9qhg9xpmwj31r40sagox.jpg)

3.做一笔交易

路由:`/transactions/new`

参数

```json
{
 "sender": "my address 2",
 "recipient": "someone else's address 2",
 "details": "转账4十块钱"
}
```

![](https://tva1.sinaimg.cn/large/006tNbRwly1g9qhhi74asj31jx0u0q6x.jpg)

4.创建一个币

![](https://tva1.sinaimg.cn/large/006tNbRwly1g9qhipdvybj31jk0u0afe.jpg)

5.同步节点

![image-20191209150832900](https://tva1.sinaimg.cn/large/006tNbRwly1g9qhnjw0aqj31eo0u0461.jpg)