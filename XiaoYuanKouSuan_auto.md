# XiaoYuanKouSuan_auto

小猿口算自动答题程序，实现自动答题（目前只有比大小）

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />

  <h3 align="center">“小猿口算自动答题”</h3>
  <p align="center">
  小猿口算自动答题程序，实现自动答题（目前只有比大小）<br />
  OCR文字识别+模拟输入，纯算法实现自动答题，不是抓包改数据<br />
  使用了mss库实现高效跨平台截屏，OpenCV图像处理，Tesseract OCR识别引擎识别数字，pynput库模拟鼠标操作<br />
  为此我还写了个能截取屏幕区域的模块😐<br />
    <a href="https://github.com/23666hh/XiaoYuanKouSuan_auto"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/23666hh/XiaoYuanKouSuan_auto/issues">报告Bug</a>
    ·
    <a href="https://github.com/23666hh/XiaoYuanKouSuan_auto/issues">提出新特性</a>
  </p>


</p>

## 目录

- [上手指南](#上手指南)
  - [开发前的配置要求](#开发前的配置要求)
  - [安装步骤](#安装步骤)
- [使用指南](#使用指南)
  - [快速开始](#快速开始)
  - [详细使用说明](#详细使用说明)
  - [自定义模块](#自定义模块)
- [文件目录说明](#文件目录说明)
- [贡献者](#贡献者)
  - [如何参与开源项目](#如何参与开源项目)
- [作者](#作者)
- [鸣谢](#鸣谢)



### 上手指南


###### 开发前的配置要求

1. 适用于Windows、Mac、Linux系统
2. 基于Python 3.12.2进行开发，使用了PyCharm编辑器（VSCode也可以）
3. 使用了tesseract文本识别引擎
4. 使用了MuMu模拟器

###### **安装步骤**

1. 点击绿色的 **Code** 按钮，再点击 **Download Zip** 下载整个项目,熟悉git也可用git下载
2. 在[Python官网](https://www.python.org/downloads/) 下载Python，版本最新也应该没问题，打不开就点这个[Python中文网](https://python.p2hp.com/downloads/)
3. 在[PyCharm官网](https://www.jetbrains.com/pycharm/download/) 下载PyCharm Community版，如果实在不会下载Python和PyCharm，就看这篇文章[超详细下载安装](https://blog.csdn.net/junleon/article/details/120698578)
4. 如是Windows则点击[Windows版tesseract](https://github.com/UB-Mannheim/tesseract/wiki)，其他版本在[tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)下载，同时也可安装中文语言（是能识别中文不是汉化），[完整安装步骤与配置](https://blog.csdn.net/qq_38463737/article/details/109679007)
5. 在[MuMu](https://mumu.163.com/) 下载MuMu模拟器，设置性能配置为 “ **高性能** ” ， 分辨率为 “ **手机版1080\*1920** ” ，帧率为 “ **240（拉满）** ” ，重启后安装小猿口算并设置**窗口置顶**
6. `Pycharm`新建项目  
方法一：使用虚拟解释器（就是新建后的界面）  
![](https://github.com/23666hh/XiaoYuanKouSuan_auto/blob/main/image/new.png)  
方法二：使用系统解释器（建议使用）  
新建界面点击**自定义环境**，点击**选择现有**  
![](https://github.com/23666hh/XiaoYuanKouSuan_auto/blob/main/image/new1.png)  
解压项目包把里面的`requirements.txt`、`screen_selector.py`、`小猿口算.py`复制到新建项目里（如果是虚拟解释器注意别放错在**.venv**文件夹里），打开终端（左边栏倒数第三个），输入下面命令安装依赖

```sh
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```



### 使用指南


###### 快速开始

打开小猿口算app（记得**置顶**），点击口算练习场10道题**开始练习**，移动窗口到合适的位置（不要挡住左下角控制台就行），运行`小猿口算.py`，根据控制台的信息完成配置信息录入，录入后只要模拟器窗口位置不移动都成功

下次重新打开模拟器会变位置，打开生成的配置文件`selection_config.json`，把`rectangle`的值改为null（`"rectangle": null`）或直接删掉，运行`小猿口算.py`重新录入配置信息

###### 详细使用说明

模拟器先移动到合适的位置（建议靠屏幕右侧），运行`小猿口算.py`，第一次运行会生成配置文件，**程序强制退出快捷键是 `-`（减号）**

**鼠标移动到识别区域的一个角上，按下左键往对角方向拖动松开结束（就是选截屏区域，四个角都可以），退出按Esc（选错了左键不要松开，直接按Esc退出）**

![](https://github.com/23666hh/XiaoYuanKouSuan_auto/blob/main/image/select.gif)
选区后会自动识别，第一次还需录入模拟输入的位置点

**鼠标移动到绘画框中心，右键点击选中，中键点击退出（选错了只要中键没点击是不会退出的，再点右键更新点就行）**

录入后自动识别并模拟输入，**鼠标放开不要移动**，如果一直判断出错用减号退出并增加main函数里的停顿时间，后续再慢慢加快

```python
// time.sleep(0.008)
time.sleep(0.1)
```

下次重新打开模拟器会变位置，打开配置文件`selection_config.json`，把`rectangle`的值改为null（`"rectangle": null`）或直接删掉，运行`小猿口算.py`重新录入配置信息



###### 自定义模块

`screen_selector.py` 屏幕选择工具

用于选择屏幕区域或某个点且有截屏功能

选区采用`pynput`库，截屏采用`PIL`库

使用方法：

```python
from screen_selector import ScreenSelector  // 导入模块
selector = ScreenSelector()  // 创建ScreenSelector实例
selector.run()  // 选区主函数
selector.screenshot(字典键)  // 截屏
```



### 文件目录说明

```
root
│  ├── /image/				# 相关图片
│  │  ├── fastest.png
│  │  ├── new.png
│  │  └── new1.png
├── LICENSE					# 软件许可证
├── README.md				# 本项目的说明文件
├── requirments.txt			# Python项目依赖文件
├── screen_selector.py		# 屏幕选择工具
├── selection_config.json	# 配置文件
└── 小猿口算.py				# 主程序
```



### 贡献者

本项目由 [23666hh](https://github.com/23666hh) 独立开发与维护

#### 如何参与开源项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



### 作者

3359713615@qq.com

### 版权说明

该项目签署了GNU 通用公共许可证 v3.0 授权许可，详情请参阅 [LICENSE](https://github.com/23666hh/XiaoYuanKouSuan_auto/blob/master/LICENSE)

### 鸣谢


- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

<!-- links -->

[your-project-path]:23666hh/XiaoYuanKouSuan_auto
[contributors-shield]: https://img.shields.io/github/contributors/23666hh/XiaoYuanKouSuan_auto.svg?style=flat-square
[contributors-url]: https://github.com/23666hh/XiaoYuanKouSuan_auto/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/23666hh/XiaoYuanKouSuan_auto.svg?style=flat-square
[forks-url]: https://github.com/23666hh/XiaoYuanKouSuan_auto/network/members
[stars-shield]: https://img.shields.io/github/stars/23666hh/XiaoYuanKouSuan_auto.svg?style=flat-square
[stars-url]: https://github.com/23666hh/XiaoYuanKouSuan_auto/stargazers
[issues-shield]: https://img.shields.io/github/issues/23666hh/XiaoYuanKouSuan_auto.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/23666hh/XiaoYuanKouSuan_auto.svg
[license-shield]: https://img.shields.io/github/license/23666hh/XiaoYuanKouSuan_auto.svg?style=flat-square
[license-url]: https://github.com/23666hh/XiaoYuanKouSuan_auto/blob/master/LICENSE

