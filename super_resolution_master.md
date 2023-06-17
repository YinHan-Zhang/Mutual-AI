### 项目简介

​		当我们看到一张低分辨率的图像时，我们希望能够通过一种算法或模型来生成一张更高分辨率、更清晰的图像。EDSR就是这样一种模型。

​		EDSR模型的原理很简单。它是一个由多个层次组成的神经网络，每个层次都会学习图像的一些特征。这些特征包括图像中的边缘、纹理、颜色等。然后，模型会将这些特征组合起来，生成一张更高分辨率的图像。

​		模型的训练过程是通过观察大量的低分辨率图像和对应的高分辨率图像来进行的。模型会不断地尝试不同的参数和权重，直到找到最好的参数组合，使得生成的高分辨率图像与真实的高分辨率图像尽量相似。

​		一旦训练完成，我们就可以使用这个训练好的模型来对新的低分辨率图像进行处理。模型会根据之前学到的知识，将低分辨率图像中的特征转换为更高分辨率图像的特征，从而生成一张更清晰的图像。

### EDSR.py

#### 步骤

1. 导入所需的模块和函数。
2. 定义了一个名为`edsr`的函数，它创建了一个EDSR模型。
3. 在`edsr`函数中，首先创建了一个输入层`x_in`，接着使用`Lambda`层对输入进行归一化处理。
4. 然后通过一系列卷积操作和残差块构建了EDSR模型的主体部分。
5. `res_block`函数定义了一个残差块，包括两个卷积层和一个残差连接。
6. `upsample`函数定义了上采样操作，根据指定的缩放因子对输入进行上采样。
7. 最后，通过卷积层将输出通道数调整为3，然后使用`Lambda`层对输出进行反归一化处理。
8. 返回一个模型对象，其中输入为`x_in`，输出为生成的高分辨率图像。

#### 详细代码

```python
def edsr(scale, num_filters=64, num_res_blocks=8, res_block_scaling=None):
    # 定义输入层，形状为 (None, None, 3)
    x_in = Input(shape=(None, None, 3))
    # 对输入进行归一化处理
    x = Lambda(normalize)(x_in)

    # 第一个卷积层，使用 num_filters 个卷积核，卷积核大小为 3，padding 设置为 'same'
    x = b = Conv2D(num_filters, 3, padding='same')(x)
    
    # 构建 num_res_blocks 个残差块
    for i in range(num_res_blocks):
        b = res_block(b, num_filters, res_block_scaling)
    
    # 最后一个卷积层，使用 num_filters 个卷积核，卷积核大小为 3，padding 设置为 'same'
    b = Conv2D(num_filters, 3, padding='same')(b)
    
    # 将输入层和最后一个卷积层的输出进行相加
    x = Add()([x, b])

    # 上采样操作
    x = upsample(x, scale, num_filters)
    
    # 最后一个卷积层，将通道数调整为 3，卷积核大小为 3，padding 设置为 'same'
    x = Conv2D(3, 3, padding='same')(x)

    # 对输出进行反归一化处理
    x = Lambda(denormalize)(x)
    
    # 创建并返回一个模型对象，输入为 x_in，输出为 x，模型名称为 "edsr"
    return Model(x_in, x, name="edsr")


def res_block(x_in, filters, scaling):
    # 第一个卷积层，使用 filters 个卷积核，卷积核大小为 3，padding 设置为 'same'，激活函数为 'relu'
    x = Conv2D(filters, 3, padding='same', activation='relu')(x_in)
    
    # 第二个卷积层，使用 filters 个卷积核，卷积核大小为 3，padding 设置为 'same'
    x = Conv2D(filters, 3, padding='same')(x)
    
    # 如果指定了 scaling，则对第二个卷积层的输出进行缩放处理
    if scaling:
        x = Lambda(lambda t: t * scaling)(x)
    
    # 将输入层和第二个卷积层的输出进行相加，形成残差连接
    x = Add()([x_in, x])
    
    # 返回残差块的输出
    return x


def upsample(x, scale, num_filters):
    def upsample_1(x, factor, **kwargs):
        # 卷积层，使用 num_filters * (factor ** 2) 个卷积核，卷积核大小为 3，padding 设置为 'same'
        x = Conv2D(num_filters * (factor ** 2), 3, padding='same', **kwargs)(x)
        
        # 使用 pixel_shuffle 函数进行像素洗牌操作，缩放因子为 factor
        return Lambda(pixel_shuffle(scale=factor))(x)

    if scale == 2:
        # 缩放因子为 2 的上采样操作
        x = upsample_1(x, 2, name='conv2d_1_scale_2')
    elif scale == 3:
        # 缩放因子为 3 的上采样操作
        x = upsample_1(x, 3, name='conv2d_1_scale_3')
    elif scale == 4:
        # 先进行缩放因子为 2 的上采样操作
        x = upsample_1(x, 2, name='conv2d_1_scale_2')
        # 再进行缩放因子为 2 的上采样操作
        x = upsample_1(x, 2, name='conv2d_2_scale_2')

    # 返回上采样后的结果
    return x
```

#### 知识补充

1.归一化：不同的特征可能具有不同的尺度和范围，通过对输入数据进行归一化，可以将不同特征的尺度统一，使得模型更容易学习到特征之间的关系。归一化可以使得梯度下降算法更快地收敛到最优解。通过归一化，可以减少数值计算中的不稳定性，避免激活函数的饱和现象。

2.卷积层：卷积层通过卷积操作对输入数据进行特征提取和表示学习，从而捕捉到图像中的重要特征。卷积层通过使用局部感知野（卷积核）来处理输入数据，能够有效地捕捉到输入数据的局部结构和特征。这种局部感知能力使得卷积层能够对图像中的空间局部特征进行提取，例如边缘、纹理等。卷积层可以大大减少需要学习的参数数量，从而降低模型的复杂性，减少过拟合的风险。卷积层具有空间不变性的特性，这使得卷积层在处理图像时能够保持对平移、旋转和缩放等变换的不变性，从而提高模型的鲁棒性和泛化能力。

### common.py

#### 步骤

1. `DIV2K_RGB_MEAN`：一个常量数组，用于图像归一化操作。
2. `resolve_single(model, lr)`：给定一个模型和低分辨率图像(lr)，返回通过模型生成的超分辨率图像。
3. `resolve(model, lr_batch)`：给定一个模型和一个批次的低分辨率图像(lr_batch)，返回通过模型生成的超分辨率图像批次(sr_batch)。
4. `evaluate(model, dataset)`：给定一个模型和一个数据集，对数据集中的图像进行超分辨率处理，并计算平均峰值信噪比（PSNR）作为评估指标。
5. `normalize(x, rgb_mean=DIV2K_RGB_MEAN)`：对图像进行归一化操作，将像素值减去RGB均值并除以127.5。
6. `denormalize(x, rgb_mean=DIV2K_RGB_MEAN)`：对图像进行反归一化操作，将归一化的图像乘以127.5并加上RGB均值。
7. `normalize_01(x)`：将RGB图像归一化到[0, 1]的范围。
8. `normalize_m11(x)`：将RGB图像归一化到[-1, 1]的范围。
9. `denormalize_m11(x)`：`normalize_m11`的逆操作，将归一化的图像还原到原始范围。
10. `psnr(x1, x2)`：计算两个图像之间的峰值信噪比（PSNR）。
11. `pixel_shuffle(scale)`：像素洗牌操作，用于将通道深度调整为原始大小的一定比例。

#### 详细代码

```python
DIV2K_RGB_MEAN = np.array([0.4488, 0.4371, 0.4040]) * 255


def resolve_single(model, lr):
    # 单张低分辨率图像的超分辨
    return resolve(model, tf.expand_dims(lr, axis=0))[0]


def resolve(model, lr_batch):
    # 批量低分辨率图像的超分辨
    lr_batch = tf.cast(lr_batch, tf.float32)
    sr_batch = model(lr_batch)
    sr_batch = tf.clip_by_value(sr_batch, 0, 255)
    sr_batch = tf.round(sr_batch)
    sr_batch = tf.cast(sr_batch, tf.uint8)
    return sr_batch


def evaluate(model, dataset):
    # 评估模型在数据集上的性能
    psnr_values = []
    for lr, hr in dataset:
        sr = resolve(model, lr)
        psnr_value = psnr(hr, sr)[0]
        psnr_values.append(psnr_value)
    return tf.reduce_mean(psnr_values)


# ---------------------------------------
#  Normalization
# ---------------------------------------

def normalize(x, rgb_mean=DIV2K_RGB_MEAN):
    # 归一化输入张量 x，通过减去 RGB 均值并除以 127.5
    return (x - rgb_mean) / 127.5


def denormalize(x, rgb_mean=DIV2K_RGB_MEAN):
    # 反归一化输入张量 x，通过乘以 127.5 并加上 RGB 均值
    return x * 127.5 + rgb_mean


def normalize_01(x):
    # 将 RGB 图像归一化到范围 [0, 1]
    return x / 255.0


def normalize_m11(x):
    # 将 RGB 图像归一化到范围 [-1, 1]
    return x / 127.5 - 1


def denormalize_m11(x):
    # 将范围在 [-1, 1] 的 RGB 图像反归一化到范围 [0, 255]
    return (x + 1) * 127.5


# ---------------------------------------
#  Metrics
# ---------------------------------------

def psnr(x1, x2):
    # 计算两个图像 x1 和 x2 之间的峰值信噪比 (PSNR)
    return tf.image.psnr(x1, x2, max_val=255)


# ---------------------------------------
#  See https://arxiv.org/abs/1609.05158
# ---------------------------------------

def pixel_shuffle(scale):
    # 根据论文中描述的像素洗牌操作进行实现
    return lambda x: tf.nn.depth_to_space(x, scale)
```

#### 知识补充

1.batch：将多个样本打包成批处理可以减少内存消耗。相较于逐个处理样本，批处理可以更有效地利用内存，减少数据传输和存储的开销。批处理可以提高模型的训练和推理性能。通过一次前向传播和一次反向传播处理多个样本，可以减少参数更新的次数，提高模型的收敛速度和稳定性。批处理允许一次处理多个样本，减少推理的总体时间。

2.反归一化：通过反归一化操作，可以将模型输出映射回原始像素值的范围，以便于可视化、后处理或与其他数据进行比较。这样可以确保模型输出的结果与实际场景或任务要求相匹配，并使结果更易于理解和使用。

3.峰值信噪比：衡量图像或信号质量的常用指标之一。它用于比较原始信号与经过处理或传输的信号之间的差异，以评估图像重建、压缩、去噪等算法的效果。

### utils.py

#### 步骤

1. **load_image(path)**：这个函数用于加载图像文件。它接受一个文件路径作为参数，并返回加载的图像的NumPy数组表示。它使用PIL库的`Image.open()`函数打开图像文件，然后使用`np.array()`函数将图像转换为NumPy数组。
2. **plot_sample(lr, sr)**：这个函数用于绘制示例图像。它接受两个图像数组作为参数：`lr`表示低分辨率图像，`sr`表示超分辨率图像（通过某个算法得到的高分辨率图像的估计值）。函数使用Matplotlib库创建一个包含两个子图的图像窗口，并在每个子图中显示相应的图像。函数最后调用`plt.show()`显示图像。

#### 详细代码

```python
def load_image(path):
    # 加载图像并将其转换为numpy数组
    return np.array(Image.open(path))


def plot_sample(lr, sr):
    # 创建一个绘图窗口
    plt.figure(figsize=(20, 10))

    # 将LR和SR图像存储在一个列表中，并为它们设置标题
    images = [lr, sr]
    titles = ['LR', f'SR (x{sr.shape[0] // lr.shape[0]})']

    # 遍历图像列表并创建子图
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, 2, i+1)  # 创建子图
        plt.imshow(img)  # 显示图像
        plt.title(title)  # 设置标题
        plt.xticks([])  # 隐藏x轴刻度线
        plt.yticks([])  # 隐藏y轴刻度线

    # 显示绘图窗口
    plt.show()
```

#### 知识补充

1.LR、SR：LR是低分辨率图像，SR是高分辨率图像

2.plt：matplotlib是python的一个绘图库，提供了类似于MATLAB绘图界面的函数，使得用户可以方便地创建各种类型的图表、绘制数据、自定义图形属性等。

### example_edsr.py

#### 步骤

1. 定义了一个函数`base64_to_image`：该函数用于将Base64编码的图像字符串转换为PIL图像对象。它首先从Base64字符串中提取图像数据，然后使用`BytesIO`将数据转换为字节流，最后通过`Image.open`将字节流转换为PIL图像。
2. 定义了一个函数`pil_base64`：该函数用于将PIL图像保存为Base64编码的字符串。它将图像对象保存在内存中的字节流中，然后使用`base64.b64encode`对字节流进行编码，最终生成Base64编码的图像字符串。
3. 定义了一个函数`evavalue`：该函数加载EDSR模型的权重，并返回加载后的模型对象。具体的模型定义和权重加载的代码没有包含在你提供的代码中，可能在其他文件中实现。
4. 定义了一个函数`resolve_and_plot`：该函数接受一个低分辨率图像作为输入，在加载的EDSR模型上进行超分辨率处理，并返回超分辨率处理后的图像的Base64编码字符串。具体的处理过程包括将输入图像转换为Numpy数组，调用`resolve_single`函数进行超分辨率处理，然后将处理后的图像转换为Base64编码字符串。

#### 详细代码

```python
depth = 16  # EDSR模型的深度
scale = 4  # 超分辨率的比例因子

# 权重文件路径
weights_file = os.path.join(os.path.dirname(__file__), 'weights', 'weights.h5')


def base64_to_image(base64_str, image_path=None):
    # 将Base64编码的图像转换为PIL图像对象
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img = img.convert('RGB')
    if image_path:
        img.save(image_path)
    return img


def pil_base64(img, coding='utf-8'):
    # 将PIL图像对象转换为Base64编码字符串
    img_format = img.format
    if img_format is None:
        img_format = 'JPEG'

    format_str = 'JPEG'
    if 'png' == img_format.lower():
        format_str = 'PNG'
    if 'gif' == img_format.lower():
        format_str = 'gif'

    if img.mode == "P":
        img = img.convert('RGB')
    if img.mode == "RGBA":
        format_str = 'PNG'
        img_format = 'PNG'

    output_buffer = BytesIO()
    # img.save(output_buffer, format=format_str)
    img.save(output_buffer, quality=100, format=format_str)
    byte_data = output_buffer.getvalue()
    base64_str = 'data:image/' + img_format.lower() + ';base64,' + base64.b64encode(byte_data).decode(coding)

    return base64_str


def evavalue():
    # 创建EDSR模型并加载权重
    model = edsr(scale=scale, num_res_blocks=depth)
    model.load_weights(weights_file)

    return model


def resolve_and_plot(lr_image):
    # 将Base64编码的图像转换为Numpy数组
    lr_image = base64_to_image(lr_image)
    lr = np.array(lr_image)

    # 使用EDSR模型进行超分辨率图像处理
    sr = resolve_single(evavalue(), lr)
    # plot_sample(lr, sr)  # 绘制样本图像

    # 将SR图像编码为PNG格式的Base64字符串
    encode_image = tf.image.encode_png(sr)
    res = str(base64.b64encode(encode_image.numpy()), 'utf-8')

    return 'data:image/png;base64,' + res
```

#### 知识补充

1.Base64：Base64编码是一种将二进制数据转换为可打印字符的编码方法。Base64编码常用于在文本环境中传输或存储二进制数据，例如在电子邮件中传输图像、在网页中嵌入图像或将二进制数据存储在数据库中。通过Base64编码，二进制数据可以表示为由A-Z、a-z、0-9和两个特殊字符组成的字符串。

2.PIL：PIL（Python Imaging Library）是Python中广泛使用的图像处理库，它提供了丰富的图像操作功能和图像文件格式的支持。PIL图像是PIL库中定义的图像对象。它是在内存中表示和操作图像的数据结构，可以进行各种图像处理操作，如调整大小、裁剪、旋转、滤镜应用等。PIL图像可以是彩色图像（RGB模式）或灰度图像（L模式）。

3.权重：在机器学习和深度学习中，权重（weights）是模型训练过程中学习到的参数。权重表示了模型中每个神经元或每个特征的重要程度，决定了模型对输入数据的响应和预测结果的准确性。
