# Map_generation_tool



基于Django框架开发的Web应用，用于将CSV文件中的地理数据转换为可视化的交互式地图。



## 功能特点

可生成以下地图类型

### **高德地图**

- #### 点标记地图

<img src="README.assets\image-20260114110932930.png" alt="image-20260114110932930" width="70%" />

- #### 海量点标记地图

<img src="README.assets\image-20260114111004940.png" alt="image-20260114111004940" width="70%" />

- #### 线图

<img src="README.assets\image-20260114111035229.png" alt="image-20260114111035229" width="70%" />

- #### 点聚合地图

<img src="README.assets\image-20260114111103707.png" alt="image-20260114111103707" width="70%" />

- #### 热力图（2D/3D）

<img src="README.assets\image-20260114111130457.png" alt="image-20260114111130457" width="70%" />

<img src="README.assets\image-20260114111153915.png" alt="image-20260114111153915" width="70%" />

### **百度地图**

相关功能后续完善

- #### 点标记地图

<img src="README.assets\image-20260114103909488.png" alt="image-20260114103909488" width="70%" />

### 支持的坐标系

- WGS84（全球定位系统）
- GCJ02（火星坐标系，高德地图使用）
- BD09（百度坐标系，百度地图使用）
- MapBar（图吧坐标系）



## 使用指南

部署了一个在线版本的，可以简单尝试下：[地图生成工具](http://xuenann.pythonanywhere.com/)

### 基本流程

<img src="README.assets\image-20260114102524944.png" alt="image-20260114102524944" width="50%" />

1. **选择文件或文件夹**
   - 点击"选择文件"按钮上传单个CSV文件
   - 点击"选择文件夹"按钮批量上传CSV文件
2. **配置参数**
   - **是否忽略第一行**：选择是否忽略CSV文件的表头行
   - **选择坐标系**：选择数据使用的坐标系
3. **选择地图类型**
   - 从下拉菜单中选择需要生成的地图类型
   - 根据地图类型配置相应参数（如经度列、纬度列等）
4. **生成地图**
   - 点击"生成地图"按钮
   - 等待地图生成完成
   - 查看生成结果和下载链接

### 高德地图功能

<img src="README.assets\image-20260114111400948.png" alt="image-20260114111400948" width="90%"/>

1. **工具条方向盘**：可以倾斜、旋转地图
2. **比例尺**
3. **地图信息**
   1. 当前地图级别：指当前显示地图的缩放级别
   2. 当前地图中心点坐标：GCJ02坐标
   3. 左击获取经纬度：鼠标左键点击获取该点GCJ02坐标坐标
   4. 当前所在省市区：当前显示的地图中心点所在省市区
4. **地图工具**
   1. 地图自适应显示：点击可将地图缩放调整至显示所有覆盖物
   2. 设置地图当前行政区：输入省市区可直接跳转至对应省市
   3. 卫星图层：添加卫星图层、删除卫星图层
   4. 路网图层：添加路网图层、删除路网图层
   5. 设置地图显示要素
      1. 区域面
      2. 道路
      3. 标注
      4. 建筑物
   6. 图层透明度：设置卫星图层的透明度
5. **鼠标右键菜单**
   1. 距离量测：鼠标左键可测量连续的距离，绘制时右键结束当前绘制，按Esc键结束绘制
   2. 添加标记：地图上添加一个红色标记，对标记右键可删除该标记

### CSV数据格式

确保CSV文件编码为UTF-8，需要包含经纬度信息，格式示例：

```csv
名称,经度,纬度,时间
地点1,116.397428,39.90923,2023-01-01
地点2,116.407428,39.91923,2023-01-02
地点3,116.417428,39.92923,2023-01-03
```

### 坐标列配置

- 经度列：输入CSV文件中经度数据所在的列索引（从0开始）
- 纬度列：输入CSV文件中纬度数据所在的列索引（从0开始）
- 标记列：可选，输入需要在标记上显示的附加信息列索引
- 排序列：可选，用于线图等需要有序数据的地图类型



## 安装与运行

### 环境要求

- Python 3.8+
- pip（Python包管理工具）

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/xuenann/Map_generation_tool.git
cd Map_generation_tool
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

> 注意：如果没有requirements.txt文件，可以手动安装Django：
> ```bash
> pip install django
> ```

3. **配置API密钥**

编辑 `myproject/settings.py` 文件，配置地图API密钥：

```python
GAODE_API_KEY = 'your_gaode_api_key'  # 高德地图API密钥
BAIDU_API_KEY = 'your_baidu_api_key'  # 百度地图API密钥
```

4. **运行开发服务器**

```bash
python manage.py runserver
```

5. **访问应用**

在浏览器中访问：`http://127.0.0.1:8000/`



## 系统配置

### 文件存储

- 上传文件默认存储在 `fileapp/uploads/<用户IP>/` 目录
- 生成的地图文件存储在同一目录下
- 批量处理时自动生成zip压缩包

### 静态文件

- 模板文件存储在 `fileapp/templates/` 目录
- 地图生成模块存储在 `fileapp/map_function/` 目录

### 项目结构

```python
Map_generation_tool/
├── fileapp/
│   ├── map_function/          # 地图生成功能模块
│   │   ├── baidu_marker.py     # 百度点标记
│   │   ├── gaode_big_marker.py # 高德海量点标记
│   │   ├── gaode_hotmap.py     # 高德热力图
│   │   ├── gaode_line.py       # 高德线图
│   │   ├── gaode_marker.py     # 高德点标记
│   │   └── gaode_marker_agg.py # 高德点聚合
│   ├── migrations/            # 数据库迁移文件
│   ├── templates/             # HTML模板和样例
│   │   ├── baidu_marker/      # 百度点标记模板
│   │   ├── gaode_big_marker/  # 高德海量点标记模板
│   │   ├── gaode_hotmap/      # 高德热力图模板
│   │   ├── gaode_line/        # 高德线图模板
│   │   ├── gaode_marker/      # 高德点标记模板
│   │   └── gaode_marker_agg/  # 高德点聚合模板
│   ├── coordinate_transform.py # 坐标转换工具
│   ├── models.py              # 数据模型
│   ├── tomap.py               # 地图生成核心逻辑
│   ├── urls.py                # 路由配置
│   └── views.py               # 视图函数
├── myproject/                 # Django项目配置
│   ├── settings.py            # 项目设置
│   ├── urls.py                # 主路由
│   └── wsgi.py                # WSGI配置
├── test/                      # 测试数据
├── .gitignore                 # Git忽略文件
├── LICENSE                    # 许可证
├── README.md                  # 项目说明
├── db.sqlite3                 # SQLite数据库
└── manage.py                  # Django管理脚本
```



## 📬 关注我 · 获取更多内容

### **📌 南墨的技术小栈**

<img src="README.assets\qrcode_for_gh_8be4598ab15d_1280.jpg" alt="qrcode_for_gh_8be4598ab15d_1280" width="30%" />

这里是我的个人知识分享空间。我会定期整理和分享工作与学习中积累的经验与资源，内容涵盖：

- 算法分享 —— 深入讲解算法原理、实现思路与代码示例。
- 工具分享 —— 推荐实用工具与脚本，包括我个人开发的小工具和精选开源工具。
- 开源项目 —— 精选 GitHub 上高星项目，拆解原理、使用方法和最佳实践。
- 数据分享 —— 工作学习中收集整理的数据资源。

无论你是技术爱好者、算法研究者，还是对数据与开源感兴趣的朋友，这里都希望能成为你学习、探索和实践的参考空间。

若在阅读或使用过程中有任何疑问，欢迎在公众号私信我，我会尽快与您交流。

如果本仓库对你有帮助，欢迎：

⭐ **Star 收藏**
 🔀 **Fork 学习参考**

你的支持将帮助我持续创作更高质量的内容！



