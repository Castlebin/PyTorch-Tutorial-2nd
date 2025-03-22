# -*- coding:utf-8 -*-

import os
import zipfile
import requests
from tqdm import tqdm


# 下载文件
def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size),
                          total=total_size / chunk_size, unit='KB', desc=save_path, ncols=80, mininterval=1):
            f.write(chunk)
    return save_path


# 解压文件
def unzip_file(zip_path, extract_path):
    zip_file = zipfile.ZipFile(zip_path)
    for name in zip_file.namelist():
        try:
            zip_file.extract(name, extract_path)
        except Exception as e:  # 解压异常，打印异常信息。继续解压下一个文件
            print("Error: ", e, name)
    return extract_path


# 下载并解压
def download_unzip(url, save_path, extract_path):
    if os.path.exists(extract_path):
        print("Dataset already exists.")
        return

    if os.path.exists(save_path):
        print("Zip file already exists.")
    else:
        # 下载
        print("Downloading...")
        download_url(url, save_path)

    # 解压
    print("Extracting...")
    unzip_file(save_path, extract_path)
    print("Done!")


# 数据集下载地址
url = "https://data.mendeley.com/public-files/datasets/rscbjbr9sj/files/f12eaf6d-6023-432f-acc9-80c9d7393433/file_downloaded"
# 保存路径
save_path = "./data/ChestXRay2017.zip"
# 解压路径
extract_path = "./data/ChestXRay2017"
# 下载并解压
download_unzip(url, save_path, extract_path)
