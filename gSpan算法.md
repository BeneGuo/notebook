gSpan是一种频繁子图挖掘算法。
关于频繁子图挖掘算法的介绍可以参考：[频繁子图挖掘介绍](http://shuju.philippe-fournier-viger.com/%E9%A2%91%E7%B9%81%E5%AD%90%E5%9B%BE%E6%8C%96%E6%8E%98%E7%AE%97%E6%B3%95%E4%BB%8B%E7%BB%8D)


graph1：
```t # 0
v 0 2
v 1 2
v 2 2
v 3 3
v 4 2
v 5 4
v 6 2
v 7 3
v 8 3
v 9 3
e 0 1 2
e 0 2 2
e 2 3 3
e 2 4 2
e 3 5 2
e 4 6 2
e 5 7 2
e 5 8 2
e 5 9 2
e 6 9 3
```
graph3:
```
t # 3
v 0 2
v 1 2
v 2 2
v 3 3
v 4 2
v 5 4
e 0 1 2
e 0 2 2
e 2 3 3
e 2 4 2
e 3 5 2
```
数据格式：
t开头表示一个新的图; v开头表示一个顶点，第二列是顶点的编号，第三列是顶点的值；e开头表示一条边，第二列和第三列是表的起止顶点编号，第四列是边的值。
橙色是顶点编号，顶点中的数字是顶点的值。绿色是边的值


从这两个图(例子中总共有5个图)中挖掘频繁子图，设置为最小支持度(-s)为2，最小顶点数(-l)为5，可以挖掘出4个子图。

depth-First Search Tree（https://www.cnblogs.com/zhang293/p/9427988.html 中DFS编码的那个截图）
从一个顶点出发，进行深度搜索，每个节点都搜索forward edge 和 backward edge，其中forward edge都被包含在 DFS tree edge中，也就是图中的实线部分。
backward edge是每个节点连接已经在当前子图中的节点了，这种edge不被包含在DFS tree中，也就是图中的虚线部分。同时，<i, j, li, l(i,j), lj>,如果i<j则是forward edge，反之是backward edge（因此每个子图实际上是要重新进行顶点的编号的）。
每个子图由v0-vn-1构成，其中v0称之为root，vn-1称之为rightmost vertex. v0-vn-1的实线的路径为该子图的right most path。


