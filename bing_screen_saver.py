#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime
import urllib.request
import json

import cv2

import win32api, win32con, win32gui

HOME = 'D:/'
pic_dir = HOME + 'Bing'

if not os.path.exists(pic_dir):
    os.makedirs(pic_dir)


def download():
    global HOME
    global pic_dir
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(date) # The type of date is str

    picture = pic_dir + '/' + date + '.jpg'

    bing_json_file = HOME + '.bing.json'
    json_url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
    bing_url = 'https://www.bing.com'

    if not os.path.exists(picture):
        urllib.request.urlretrieve(json_url, bing_json_file)
        with open(bing_json_file, 'r', encoding='utf-8') as f:
            bing_json = json.load(f)

        url_append = bing_json['images'][0]['url']
        url = bing_url + url_append

        urllib.request.urlretrieve(url, picture)

    return picture


def convert_to_bmp(pic_jpg):
    global HOME
    global pic_dir

    date = os.path.split(pic_jpg)[-1][:-4]
    print(date)
    pic_temp = cv2.imread(pic_jpg)
    pic_temp_path = os.path.join(pic_dir, date + '.bmp')
    cv2.imwrite(pic_temp_path, pic_temp)
    os.remove(pic_jpg)
    return pic_temp_path


def set_wallpaper(pic_bmp):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)

    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")

    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")

    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_bmp, win32con.SPIF_SENDWININICHANGE)


if __name__ == '__main__':
    pic_jpg = download()
    pic_bmp = convert_to_bmp(pic_jpg)
    set_wallpaper(pic_bmp)
