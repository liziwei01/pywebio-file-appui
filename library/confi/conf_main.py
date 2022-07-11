import env
from abc import abstractmethod, ABCMeta
from typing import Sequence, Any
from library import error
from os import path
from before import newBeforeHelper

# Conf 配置解析定义接口
class Conf(metaclass=ABCMeta):
	# 读取并解析配置文件
	# confName 支持相对路径和绝对路径
	@abstractmethod
	def Parse(confName: str) -> Sequence[Any, error]:
		...
	# 解析bytes内容
	@abstractmethod
	def ParseBytes(fileExtL: str, content: bytes) -> Sequence[Any, error]:
		...
	# 配置文件是否存在
	@abstractmethod
	def Exists(confName: str) -> bool:
		...
	# 注册一个指定后缀的配置的parser
	# 如要添加 .ini 文件的支持，可在此注册对应的解析函数即可
	# def RegisterParserFunc(fileExt: str, fn: ParserFunc) -> error:
	def RegisterParserFunc(fileExt: str, fn: Any) -> error:
		...
	# 注册一个在解析前执行辅助回调方法
	# 先注册的先执行，不能重复
	# def RegisterBeforeFunc(name: str, fn: BeforeFunc) -> error:
	def RegisterBeforeFunc(name: str, fn: Any) -> error:
		...
	# 配置的环境信息
	@abstractmethod
	def Env() -> env.AppEnv:
		...

relPathPre = "." + str(path.sep)

# conf实现Conf接口
class conf(Conf):
	env_: env.AppEnv
	parsers: dict # str:ParserFunc
	helpers: list # beforeHelper

	def __init__(self, env_: env.AppEnv, parsers: dict={}, helpers: list=[]):
		self.env_ = env_
		self.parsers = parsers
		self.helpers = helpers

	# 传入文件名和接收obj实现解析配置文件，配置文件默认认为在 conf/ 目录下
	def Parse(self, confName: str) -> Sequence[str, error]:
		confAbsPath = self.confFileRealPath(confName)
		return self.parseByAbsPath(confAbsPath)

	# 将文件名组装为文件实际所在目录
	def confFileRealPath(self, confName: str) -> str:
		# 若文件名已经是绝对路径或以./开头，视为找到了绝对路径
		if path.isabs(confName) or confName.startswith(relPathPre):
			return confName
		# 将文件名加上环境变量里面的confdir的前缀
		return path.join(self.Env().ConfDir(), confName)

	# 通过绝对路径找到文件，确保文件名不空并解析
	def parseByAbsPath(self, confAbsPath: str) -> Sequence[str, error]:
		if len(self.parsers) == 0:
			return None, "no parser found"
		return self.readConfDirect(confAbsPath)

	# 开始读取配置文件并解析
	def readConfDirect(self, confPath: str) -> Sequence[str, error]:
		try:
			content = open(confPath, "r").read()
		except FileNotFoundError:
			return None, "conf file not found"
		# 读取文件扩展名，现在支持.toml .json
		fileExt = path.splitext(confPath)[-1]
		return self.ParseBytes(fileExt, content)

	# 配置里面如果设置了环境就返回设置好的，没有就返回default环境
	def Env(self) -> env.AppEnv:
		if self.env_ == None:
			return env.Default
		return self.env_

	# 开始按照文件扩展名分配解析函数解析配置文件
	def ParseBytes(self, fileExt: str, content: bytearray)->Sequence[Any, error]:
		if fileExt == "":
			return None, "{0}, fileExt {1} is not supported yet".format("no parser found", fileExt)
		try:
			parserFn = self.parsers[fileExt]
		except KeyError:
			return None, "{0}, fileExt {1} is not supported yet".format("no parser found", fileExt)
		contentNew, errHelper = self.executeBeforeHelpers(content, self.helpers)
		if errHelper != None:
			return None, "{0}, content=\n{1}".format(errHelper, str(contentNew))

		obj, errParser = parserFn(contentNew)
		if errParser != None:
			return None, "{0}, content=\n{1}".format(errParser, str(contentNew))
		return obj, None

	# executeBeforeHelpers 执行
	# def executeBeforeHelpers(self, input: bytearray, helpers: list[beforeHelper]) -> Sequence[bytearray, error]:
	def executeBeforeHelpers(self, input: bytearray, helpers: list[Any]) -> Sequence[bytearray, error]:
		if len(helpers) == 0:
			return input, None
		output = input
		for helper in helpers:
			output, err = helper.Func(self, output)
			if err != None:
				return None, "beforeHelper={0} has error:{1}".format(helper.Name, err)
		return output, err

	# 检查该配置文件是否存在
	def Exists(self, confName: str) -> bool:
		return path.exists(self.confFileRealPath(confName))

	# 注册解析能力
	# def RegisterParserFunc(self, fileExt: str, fn: ParserFunc) -> error:
	def RegisterParserFunc(self, fileExt: str, fn: Any) -> error:
		has = True
		if fileExt == "":
			return "fileExt is empty"
		try:
			parserFn = self.parsers[fileExt]
		except KeyError:
			has = False
		if has:
			return "parser={0} already exists".format(fileExt)
		self.parsers[fileExt] = fn
		return None

	# def RegisterBeforeFunc(self, name: str, fn: BeforeFunc) -> error:
	def RegisterBeforeFunc(self, name: str, fn: Any) -> error:
		if name == "":
			return "name is empty, not allow"
		for h1 in self.helpers:
			if name == h1.Name:
				return "beforeHelper={0} already exists".format(name)
		self.helpers.extend(newBeforeHelper(name, fn))
		return None

# 为了在编译期即确保实现了接口
# var _ Conf = (*conf)(nil)
