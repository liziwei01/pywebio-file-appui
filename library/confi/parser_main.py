'''
Author: liziwei01
Date: 2022-07-10 18:02:58
LastEditors: liziwei01
LastEditTime: 2022-07-11 01:12:38
Description: file content
'''
from library import error
from typing import Any, Tuple, Callable
from types import SimpleNamespace
import json
import toml

# Parserdef 针对特定文件后缀的配置解析方法
# 当前已经内置了 .toml  和 .json的解析方法
ParserFunc: Callable[[bytearray], error]

# const: 
# 已支持的文件后缀
# FileTOML toml
FileTOML = ".toml"
# FileJSON  json
FileJSON = ".json"

# stripComment 去除单行的'#'注释
# 只支持单行，不支持行尾
def stripComment(input: bytearray) -> bytearray:
	buf = bytearray()
	lines = input.split(b"\n")
	for line in lines:
		lineN = line.strip()
		# 若内容以 # 开头，则该为注释
		if not lineN.startswith(b"#"):
			buf.extend(line)
		buf.extend(b"\n")
	return buf.strip()

def jsonParserFunc(input: bytearray) -> Tuple[Any, error]:
	bf = stripComment(input)
	try:
		# Parse JSON into an object with attributes corresponding to dict keys.
		return json.loads(bf.strip(b"\t\r\n"), object_hook=lambda d: SimpleNamespace(**d)), None
	except json.JSONDecodeError as e:
		return None, e.msg

def tomlParserFunc(input: bytearray) -> Tuple[Any, error]:
	bf = stripComment(input)
	dec = toml.loads(bf.strip(b"\t\r\n").decode())
	enc = json.dumps(dec)
	return jsonParserFunc(bytearray(enc.encode()))

# JSONParserdef .json配置文件格式解析函数
JSONParserFunc: ParserFunc = jsonParserFunc

# TOMLParserdef .toml配置文件格式解析函数
TOMLParserFunc: ParserFunc = tomlParserFunc

# DefaultParserFuncs 所有默认的ParserFunc
DefaultParserFuncs = {
	FileJSON: JSONParserFunc,
	FileTOML: TOMLParserFunc,
}