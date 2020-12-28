采用notebook对sagemaker测试第三方模型流程：
0.环境准备，创建sagemaker， 创建notebook，创建S3桶
1. 上传模型文件和数据文件（看需要）
2. 将PB转成saved model的格式，可以用notebook写代码转，转完后需要将文件夹打包成tar.gz的格式
 从S3下载到本地notebook本地，从nodebook本地上传
 mm = sagemaker_session.download_data(path='model/',bucket=bucket, key_prefix='model/res50.tar.gz')
 inputs = sagemaker_session.upload_data(path='model/mm.tar.gz', bucket=bucket, key_prefix='model')
 本地路径 默认 /home/ec2-user/SageMaker/

model要求是tar.gz的格式
entry_point是源码的py文件，pb先试试指定为None，有的框架必须要模型代码才能还原成模型。
An error occurred (ValidationException) when calling the CreateEndpointConfig operation: 1 validation error detected: Value 'ml.t3.medium' at 'productionVariants.1.member.instanceType' failed to satisfy constraint: Member must satisfy enum value set: 
[ml.r5d.12xlarge, ml.r5.12xlarge, ml.p2.xlarge, ml.m5.4xlarge, ml.m4.16xlarge, ml.r5d.24xlarge, ml.r5.24xlarge, ml.p3.16xlarge, ml.m5d.xlarge, ml.m5.large, ml.t2.xlarge, ml.p2.16xlarge, ml.m5d.12xlarge, ml.inf1.2xlarge, ml.m5d.24xlarge, ml.c4.2xlarge, ml.c5.2xlarge, ml.c4.4xlarge, ml.inf1.6xlarge, ml.c5d.2xlarge, ml.c5.4xlarge, ml.g4dn.xlarge, ml.g4dn.12xlarge, ml.c5d.4xlarge, ml.g4dn.2xlarge, ml.c4.8xlarge, ml.c4.large, ml.c5d.xlarge, ml.c5.large, ml.g4dn.4xlarge, ml.c5.9xlarge, ml.g4dn.16xlarge, ml.c5d.large, ml.c5.xlarge, ml.c5d.9xlarge, ml.c4.xlarge, ml.inf1.xlarge, ml.g4dn.8xlarge, ml.inf1.24xlarge, ml.m5d.2xlarge, ml.t2.2xlarge, ml.c5d.18xlarge, ml.m5d.4xlarge, ml.t2.medium, ml.c5.18xlarge, ml.r5d.2xlarge, ml.r5.2xlarge, ml.p3.2xlarge, ml.m5d.large, ml.m5.xlarge, ml.m4.10xlarge, ml.t2.large, ml.r5d.4xlarge, ml.r5.4xlarge, ml.m5.12xlarge, ml.m4.xlarge, ml.m5.24xlarge, ml.m4.2xlarge, ml.p2.8xlarge, ml.m5.2xlarge, ml.r5d.xlarge, ml.r5d.large, ml.r5.xlarge, ml.r5.large, ml.p3.8xlarge, ml.m4.4xlarge]

https://sagemaker.readthedocs.io/en/stable/frameworks/tensorflow/using_tf.html#deploy-tensorflow-serving-models
https://sagemaker.readthedocs.io/en/stable/frameworks/tensorflow/using_tf.html#deploying-directly-from-model-artifacts
3. 测试编译后模型的步骤：
1）创建一个TensorFlow model 对象
2）调用其compile方法，编译模型，根据目标硬件，优化基本上采用tensorRT和TVM进行优化
3）调用deploy方法部署编译后模型
4）predictor.predict，注意predict接受的数据需要是TensorFlow的restAPI的格式。如果是未经编译的需要严格遵守rest API，如果是经过编译后的模型，可以有类json格式的API。具体可以参考：
predictor 由 deploy返回，predictor接收的数据格式由 TF的rest 接口定义
Once you have the Predictor instance returned by model.deploy(...) or estimator.deploy(...), you can send prediction requests to your Endpoint.
The formats of the input and the output data correspond directly to the request and response formats of the Predict method in the TensorFlow Serving REST API.
来自：https://sagemaker.readthedocs.io/en/stable/frameworks/tensorflow/using_tf.html?highlight=predict#making-predictions-against-a-sagemaker-endpoint

Request format
The request body for predict API must be JSON object formatted as follows:
'''
{
  // (Optional) Serving signature to use.
  // If unspecifed default serving signature is used.
  "signature_name": <string>,

  // Input Tensors in row ("instances") or columnar ("inputs") format.
  // A request can have either of them but NOT both.
  "instances": <value>|<(nested)list>|<list-of-objects>
  "inputs": <value>|<(nested)list>|<object>
}
'''
来自 https://www.tensorflow.org/tfx/serving/api_rest


待解决问题：
1. 已存在的endpoint，怎么推理
2. transform批量推理
支持的输入数据分割 None | Line(csv) | RecordIO(MXNet) | TFRecord(TF)
输入数据支持目录(S3Prefix)或者具体的文件(ManifestFile)
3. 单条推理的时候，bs超过8就报错
https://github.com/aws/sagemaker-python-sdk/issues/831
Unfortunately, SageMaker's InvokeEndpoint API does have a 5MB limit on the size of incoming requests.
参考这里，应该是5MB的限制，5MB/224*224*3*4(float)(单张图大小) = 8.707482993197279


