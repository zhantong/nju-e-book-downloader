# 南大图书馆电子书下载器

## Deprecated

由于图书馆已不再提供电子书查找和下载服务，本仓库暂时失效。

## 简介

由于图书馆电子书网站仅提供扫描版电子书的在线阅读，造成诸多不便。本下载器通过输入电子书ID，即可生成PDF版的电子书。

请支持正版图书。

## 使用方法

### 安装依赖

需要用到第三方库Pillow和Reportlab。

如下代码安装依赖：

```bash
pip3 install pillow

pip3 install reportlab
```

### 下载电子书

浏览器中登录南大图书馆电子书网站[http://114.212.7.104:8181]，搜索到希望下载的电子书后，记录下其ID。在提供的Python脚本中运行`convert_to_pdf(book_id)`，稍等片刻即可得到PDF格式的电子书。

## 工作原理

1. 根据ID下载所有扫描图片；
2. 利用Pillow将图片统一为jpeg格式；
3. 利用Reportlab将图片转换为PDF。
