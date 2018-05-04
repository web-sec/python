import tensorflow as tf


a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)
op1 = tf.multiply(a,b)
session = tf.Session()
c = tf.constant([[1,2,3],[2,2,2],[4,4,5]])
d = tf.constant([[1,2,3],[2,2,2],[4,4,5]])
e = tf.Va
op2 = tf.multiply(c,d)
with tf.Session() as sess:
    result = sess.run(tf.transpose(c))
    print(result)
#
# # 导入数据集
# from tensorflow.examples.tutorials.mnist import input_data
# mnist = input_data.read_data_sets("data/", one_hot=True)
#
# # 变量
# batch_size = 100
#
# #训练的x(image),y(label)
# # x = tf.Variable()
# # y = tf.Variable()
# x = tf.placeholder(tf.float32, [None, 784]) #image赋值给x label赋值给y  784=28*28
# y = tf.placeholder(tf.float32, [None, 10]) #10（0-9）   实际开发中 训练数据庞大 用variable很占内存 所以引入placeholder占位容器
# #placeholder 装多少批 每批装载多少个 自己定义 每批装100  None事先无法确定
#
# # 模型权重
# #[55000,784] * W = [55000,10]
# W = tf.Variable(tf.zeros([784, 10])) #懵W和b  W*x W的行=x的列=784 最终得lable10列的矩阵 W的列=x的行=10
# b = tf.Variable(tf.zeros([10])) #矩阵相加 行列相同
#
# # 用softmax构建逻辑回归模型
# pred = tf.nn.softmax(tf.matmul(x, W) + b) #TensorFlow在nn模块已经提供好了softmax的API
# #pred 预测的label
#
# # 损失函数(交叉熵)
# cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), 1))
#
# # 低度下降
# optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(cost)
#
# # 初始化所有变量
# init = tf.global_variables_initializer()
#
# # 加载session图
# with tf.Session() as sess:
#     sess.run(init) #运行初始化变量
#
#     # 开始训练
#     for epoch in range(25): #25自己指定
#         avg_cost = 0.
#
#         total_batch = int(mnist.train.num_examples/batch_size) #batch_size分页
#         for i in range(total_batch): #一页一页的训练
#             batch_xs, batch_ys = mnist.train.next_batch(batch_size)
#             sess.run(optimizer, {x: batch_xs,y: batch_ys})
#             #计算损失平均值 当前页所有训练集代价函数的平均值
#             avg_cost += sess.run(cost,{x: batch_xs,y: batch_ys}) / total_batch
#         if (epoch+1) % 5 == 0:
#             print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))
#
#     print("运行完成")
#
#     # 测试求正确率
#     correct = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#     print("正确率:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))