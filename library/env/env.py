from abc import abstractmethod, ABCMeta
from typing import Sequence, Optional
from library import error
from os import path

# const: 常量
# 可以依据不同的运行等级来开启不同的调试功能、接口
# RunModeDebug 调试
RunModeDebug = "debug"
# RunModeTest 测试
RunModeTest = "test"
# RunModeRelease 线上发布
RunModeRelease = "release"

# var: 变量
# DefaultAppName 默认的app名称
DefaultAppName = "liziwei01APP"
# DefaultRunMode 测试默认运行等级
DefaultRunMode = RunModeRelease

# Option 具体的环境信息
# 
# 所有的选项都是可选的
class Option:
	# AppName 应用名称
	AppName: str
	# RunMode 运行模式
	RunMode: str
	# RootDir 应用根目录地址
	# 若为空，将通过自动推断的方式获取
	RootDir: str
	# DataDir 应用数据根目录地址
	# 默认为 RootDir+"/data/"
	DataDir: str
	# LogDir 应用日志根目录地址
	# 默认为 RootDir+"/log/"
	LogDir: str
	# ConfDir 应用配置文件根目录地址
	# 默认为RootDir+"/conf/"
	ConfDir: str

	def __init__(self, AppName: str | None=..., RunMode: str | None = ..., RootDir: str | None = ..., DataDir: str | None = ..., LogDir: str | None = ..., ConfDir: str | None = ...):
		self.AppName = AppName
		self.RunMode = RunMode
		self.RootDir = RootDir
		self.DataDir = DataDir
		self.LogDir = LogDir
		self.ConfDir = ConfDir

	# str 序列化，方便查看
	# 目前输出的是一个json
	def str(self) -> str:
		format = "\"AppName\":%q,\"RootDir\":%q,\"DataDir\":%q,\"LogDir\":%q,\"ConfDir\":%q,\"RunMode\":%q"
		return format.format(self.AppName, self.RootDir, self.DataDir, self.LogDir, self.ConfDir, self.RunMode)

	# Merge 合并
	# 传入的Option不为空则合并，否则使用老的值
	def Merge(self, newOpt: "Option") -> "Option":
		return Option(
			AppName = SecondStrFirst(self.AppName, newOpt.AppName),
			RunMode = SecondStrFirst(self.RunMode, newOpt.RunMode),
			RootDir = SecondStrFirst(self.RootDir, newOpt.RootDir),
			DataDir = SecondStrFirst(self.DataDir, newOpt.DataDir),
			LogDir = SecondStrFirst(self.LogDir, newOpt.LogDir),
			ConfDir = SecondStrFirst(self.ConfDir, newOpt.ConfDir),
		)

def SecondStrFirst(v1: str, v2: str) -> str:
	if v2 != "":
		return v2
	return v1


# RootDirEnv 应用根目录环境信息接口
class RootDirEnv(metaclass=ABCMeta):
	@abstractmethod
	def RootDir(self) -> str:
		...

# ConfDirEnv 配置环境信息接口
class ConfDirEnv(metaclass=ABCMeta):
	@abstractmethod
	def ConfDir(self) -> str:
		...

# DataDirEnv 数据目录环境信息接口
class DataDirEnv(metaclass=ABCMeta):
	@abstractmethod
	def DataDir(self) -> str:
		...

# LogDirEnv 日志目录环境信息接口
class LogDirEnv(metaclass=ABCMeta):
	@abstractmethod
	def LogDir(self) -> str:
		...

# AppNameEnv 应用名称接口
class AppNameEnv(metaclass=ABCMeta):
	@abstractmethod
	def AppName() -> str:
		...

# RunModeEnv 运行模式/等级接口
class RunModeEnv(metaclass=ABCMeta):
	@abstractmethod
	def RunMode() -> str:
		...

# AppEnv 应用环境信息完整的接口定义
class AppEnv(RootDirEnv, ConfDirEnv, DataDirEnv, LogDirEnv, AppNameEnv, RunModeEnv):
	# 应用名称
	AppNameEnv
	# 应用根目录
	RootDirEnv
	# 应用配置文件根目录
	ConfDirEnv
	# 应用数据文件根目录
	DataDirEnv
	# 应用日志文件更目录
	LogDirEnv
	# 应用运行情况
	RunModeEnv
	# 获取当前环境的选项详情
	def Options(self) -> Option:
		...
	# 复制一个新的env对象，并将传入的Option merge进去
	def CloneWithOption(self, opt: Option) -> "AppEnv":
		...

# New 创建新的应用环境
def New(opt: Option) -> AppEnv:
	env = appEnv()
	if opt.AppName != "":
		env.setAppName(opt.AppName)
	if opt.RunMode != "":
		env.setRunMode(opt.RunMode)
	if opt.RootDir != "":
		env.setRootDir(opt.RootDir)
	if opt.ConfDir != "":
		env.setConfDir(opt.ConfDir)
	if opt.DataDir != "":
		env.setDataDir(opt.DataDir)
	if opt.LogDir != "":
		env.setLogDir(opt.LogDir)
	return env

# appEnv 实现了以上接口
class appEnv(AppEnv):
	rootDir: str
	dataDir: str
	confDir: str
	logDir:  str
	appName: str
	runMode: str

	def __init__(self, rootDir: str="", dataDir: str="", confDir: str="", logDir: str="", appName: str="", runMode: str=""):
		self.rootDir = rootDir
		self.dataDir = dataDir
		self.confDir = confDir
		self.logDir = logDir
		self.appName = appName
		self.runMode = runMode

	# 获取AppName
	def AppName(self) -> str:
		if self.appName != "":
			return self.appName
		return DefaultAppName

	# 设定AppName
	def setAppName(self, name: str) -> None:
		self.appName = setValue(name, "AppName")

	# 获取RunMode
	def RunMode(self) -> str:
		if self.runMode != "":
			return self.runMode
		return DefaultRunMode

	# 设定RunMode
	def setRunMode(self, mod: str) -> None:
		self.runMode = setValue(mod, "RunMode")

	# 获取RootDir
	def RootDir(self) -> str:
		if self.rootDir != "":
			return self.rootDir
		return AutoDetectAppRootDir()

	# 设定RootDir
	def setRootDir(self, dir: str) -> None:
		self.rootDir = setValue(dir, "RootDir")

	# 获取DataDir
	def DataDir(self) -> str:
		return self.chooseDir(self.dataDir, "data")

	# 设定DataDir
	def setDataDir(self, dir: str) -> None:
		self.dataDir = setValue(dir, "DataDir")

	# 获取LogDir
	def LogDir(self) -> str:
		return self.chooseDir(self.logDir, "log")

	# 设定LogDir
	def setLogDir(self, dir: str):
		self.logDir = setValue(dir, "LogDir")

	# 获取ConfDir
	def ConfDir(self) -> str:
		return self.chooseDir(self.confDir, "conf")

	# 设定ConfDir
	def setConfDir(self, dir: str) -> None:
		self.confDir = setValue(dir, "ConfDir")

	# 获取Dir的时候不直接返回，走个兜底，如果为空就拼接RootDir和文件夹名字
	def chooseDir(self, dir: str, subDirName: str) -> str:
		if dir != "":
			return dir
		return path.join(self.RootDir(), subDirName)

	# 以Option的形式输出现存的环境配置信息
	def Options(self) -> Option:
		return Option(
			AppName = self.AppName(),
			RunMode = self.RunMode(),
			RootDir = self.RootDir(),
			DataDir = self.DataDir(),
			LogDir =  self.LogDir(),
			ConfDir = self.ConfDir(),
		)

	# 建立新环境配置的时候可以用老环境做base
	def CloneWithOption(self, opt: Option) -> AppEnv:
		opts = self.Options().Merge(opt)
		return New(opts)

# 所有环境变量设定时都走日志输出
def setValue(value: str, fieldName: str) -> str:
	print("[env] set {0}={1}\n".format(fieldName, value))
	return value

# 通过找含有app.toml的conf文件夹的位置来确定APP现在工作目录
def autoDetect() -> str:
	wd = path.abspath(path.dirname(__file__))

	names = [
		path.join("conf", "app.toml"),
	]
	dir, err = findDirMatch(wd, names)
	if err == None:
		return dir

	return wd

# 为了在编译期即确保appEnv实现了AppEnv接口
# var _ AppEnv = (*appEnv)(None)

# AutoDetectAppRootDir 自动获取应用根目录
# 定义为变量，这样若默认实现不满足，可进行替换
AutoDetectAppRootDir = autoDetect

# findDirMatch 在指定目录下，向其父目录查找对应的文件是否存在
# 若存在，则返回匹配到的路径
def findDirMatch(baseDir: str, fileNames: Sequence[str]) -> Sequence[str, error]:
	currentDir = baseDir
	# 最多寻找20层父目录
	for i in range(20):
		for fileName in fileNames:
			depsPath = path.join(currentDir, fileName)
			# 找到即返回
			if path.exists(depsPath):
				return currentDir, None

		# 向父目录走
		currentDir = path.dirname(currentDir)
		if currentDir == ".":
			break

	return "", "cannot found"
