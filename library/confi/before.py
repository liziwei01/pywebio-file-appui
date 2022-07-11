
'''
Author: liziwei01
Date: 2022-07-10 18:02:58
LastEditors: liziwei01
LastEditTime: 2022-07-11 01:48:39
Description: file content
'''
from typing import Sequence, Any, Callable
from library import error
import re
import os

# Beforedef 辅助回调方法，在执行ParserFunc前，会先对配置的内容进行解析处理
# BeforeFunc: Callable[[Conf, bytearray], Sequence[bytearray, error]]
BeforeFunc: Any

# beforeHelper 辅助功能
# 在正式解析配置前执行
class beforeHelper:
    Name: str
    Func: BeforeFunc
    
    def __init__(self, name: str, func: BeforeFunc):
        self.Name = name
        self.Func = func

# 构建结构体
def newBeforeHelper(name: str, fn: BeforeFunc) -> beforeHelper:
	return beforeHelper(
		Name = name,
		Func = fn,
    )

# 模板变量格式：{env.变量名} 或者 {env.变量名|默认值}
osEnvVarReg = re.compile(r"\{env\.([A-Za-z0-9_]+)(\|[^}]+)?\}")

# helperOsEnvVars 将配置文件中的 {env.xxx} 的内容，从环境变量中读取并替换
# def helperOsEnvVars(conf: Conf, content: bytes) -> Sequence[bytes, error]:
def helperOsEnvVars(conf: Any, content: bytes) -> Sequence[bytes, error]:
	def envSub(subStr: bytearray) -> bytearray:
		# 将 {env.xxx} 中的 xxx 部分取出
		# 或者 将 {env.yyy|val} 中的 yyy|val 部分取出
		keyWithDefaultVal = subStr[len("{env.") : len(subStr)-1] # eg: xxx 或者 yyy|val
		idx = keyWithDefaultVal.index(b"|")
		if idx > 0:
			# {env.变量名|默认值} 有默认值的格式
			key = str(keyWithDefaultVal[:idx])  # eg: yyy
			defaultVal = keyWithDefaultVal[idx+1:] # eg: val
			envVal = os.getenv(key)
			if envVal == None:
				return defaultVal
			return bytearray(envVal.encode())

		# {env.变量名} 无默认值的部分
		return bytearray(os.getenv(str(keyWithDefaultVal)).encode())
	contentNew = osEnvVarReg.sub(envSub, content)
	return contentNew, None

# defaultHelpers 默认的helper方法：获取环境变量
defaultHelpers: list = [
	newBeforeHelper("env", helperOsEnvVars),
]