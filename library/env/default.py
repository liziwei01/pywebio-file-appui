'''
Author: liziwei01
Date: 2022-07-10 16:19:39
LastEditors: liziwei01
LastEditTime: 2022-07-10 17:50:16
Description: file content
'''
from env import *

# Default (全局)默认的环境信息
#
# 全局的 RootDir() 、DataDir() 等方法均使用该环境信息
Default = New(Option())

# Default 现在为AppEnv接口，现在开始实现接口要求的方法
# RootDir (全局)获取应用根目录
def RootDir() -> str:
	return Default.RootDir()

# DataDir (全局)设置应用数据根目录
def DataDir() -> str:
	return Default.DataDir()

# LogDir (全局)获取应用日志根目录
def LogDir() -> str:
	return Default.LogDir()

# ConfDir (全局)获取应用配置根目录
def ConfDir() -> str:
	return Default.ConfDir()

# AppName (全局)应用的名称
def AppName() -> str:
	return Default.AppName()

# RunMode (全局) 程序运行等级
# 默认是 release(线上发布)，还可选 RunModeDebug、RunModeTest
def RunMode() -> str:
	return Default.RunMode()

# Options 获取当前环境的选项详情
def Options() -> Option:
	return Default.Options()

# CloneWithOption 复制一个新的env对象，并将传入的Option merge进去
def CloneWithOption(opt: Option) -> AppEnv:
	return Default.CloneWithOption(opt)

