'''
Author: liziwei01
Date: 2022-07-10 18:02:58
LastEditors: liziwei01
LastEditTime: 2022-07-11 13:01:42
Description: file content
'''
from library import error
from typing import Any
import env
from conf_main import *
from before import *
from parser_main import *

# New 创建一个新的配置解析实例
# 返回的实例是没有注册任何解析能力的
def New(e: env.AppEnv) -> Conf:
	conf_ = conf(
		env = e,
		parsers = {},
		# parsers = map[str]ParserFunc{},
	)
	return conf_

# NewDefault 创建一个新的配置解析实例
# 会注册默认的配置解析方法和辅助方法
def NewDefault(e: env.AppEnv) -> Conf:
	conf_ = New(e)
	for name, fn in DefaultParserFuncs:
		conf.RegisterParserFunc(name, fn)

	for h in defaultHelpers:
		err = conf.RegisterBeforeFunc(h.Name, h.Func)
		if err != None:
			print(("RegisterHelper({0}) err={1}".format(h.Name, err)))
			os.abort()
	return conf_

# Default 默认的实例,全局的Parse、ParseBytes、Exists等方法均使用该对象
Default: Conf = NewDefault(None)

# Parse 解析配置，配置文件默认认为在 conf/目录下
#
# 	如配置文件 conf/abc.toml ，则读取时使用 Parse("abc.toml",&xxx)
# 	推荐使用上述相对文件名老读取配置，这样可通过修改全局应用环境信息的env.ConfDir，来调整配置目录
#
# 	也支持传入一个绝对路径 或者 相对路径
# 	如  /tmp/test.toml 或者  ./conf/test.toml
def Parse(confName: str) -> Sequence[Any, error]:
	return Default.Parse(confName)

# ParseBytes 解析bytes
#
# fileExt 是file extension 文件后缀，如.json、.toml
def ParseBytes(fileExt: str, content: bytes) -> Sequence[Any, error]:
	return Default.ParseBytes(fileExt, content)

# Exists  判断是否存在
def Exists(confName: str) -> bool:
	return Default.Exists(confName)

# RegisterParserdef 注册一个解析器
def RegisterParserFunc(fileExt: str, fn: ParserFunc) -> error:
	return Default.RegisterParserFunc(fileExt, fn)

# RegisterBeforedef 注册一个在解析前执行辅助回调方法
# 
# name 唯一的名字；fn 回调函数
def RegisterBeforeFunc(name: str, fn: BeforeFunc) -> error:
	return Default.RegisterBeforeFunc(name, fn)
