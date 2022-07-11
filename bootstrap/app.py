'''
Author: liziwei01
Date: 2022-07-10 16:18:35
LastEditors: liziwei01
LastEditTime: 2022-07-11 13:42:28
Description: file content
'''
from os import path
from typing import Any, Callable, Sequence
from library import env, confi, error
from mxnet import context
from pywebio import start_server
from modules.login.login import UserLogin

DefaultWriter = print

# Config app's conf
# default conf/app.toml
class Config:
	APPName: str
	RunMode: str

	Env: env.AppEnv

	# conf of http service
	class HTTPServer:
		Listen:	   str
		ReadTimeout:  int # ms
		WriteTimeout: int # ms
		IdleTimeout:  int # ms

		def __init__(self, listen: str | None = ..., readTimeout: int | None = ..., writeTimeout: int | None = ..., idleTimeout: int | None = ...):
			self.Listen = listen
			self.ReadTimeout = readTimeout
			self.WriteTimeout = writeTimeout
			self.IdleTimeout = idleTimeout

	def __init__(self, APPName: str | None = ..., RunMode: str | None = ..., Env: env.AppEnv | None = ..., HTTPServer: HTTPServer | None = ...):
		self.APPName = APPName
		self.RunMode = RunMode
		self.Env = Env
		self.HTTPServer = HTTPServer

# ParserAppConfig
def ParserAppConfig(filePath: str) -> Sequence(Config, error):
	confPath, err = path.abspath(filePath)
	if err != None:
		return None, err

	c = Config()
	c, err = confi.Parse(confPath)
	if err != None:
		return None, err

	# parse and set global conf
	rootDir = path.dirname(path.dirname(confPath))
	opt = env.Option(
		AppName = c.APPName,
		RunMode = c.RunMode,
		RootDir = rootDir,
		DataDir = path.join(rootDir, "data"),
		LogDir = path.join(rootDir, "log"),
		ConfDir = path.join(rootDir, path.basename(path.dirname(confPath))),
	)
	c.Env = env.New(opt)
	return c, None

# App application
class App:
	ctx: context.Context
	config: Config
	server: Any # http.Server
	close: Callable[[Any], Any]

	# def initHTTPServer(self): # handler: gin.Engine) 
	# 	ser = &http.Server{
	# 		Addr:		 app.config.HTTPServer.Listen,
	# 		Handler:	  handler,
	# 		ReadTimeout:  time.Millisecond * time.Duration(app.config.HTTPServer.ReadTimeout),
	# 		WriteTimeout: time.Millisecond * time.Duration(app.config.HTTPServer.WriteTimeout),
	# 		IdleTimeout:  time.Millisecond * time.Duration(app.config.HTTPServer.IdleTimeout),
	# 	}
	# 	app.server = ser

	# Start start the service
	def Start(self) -> error:
		# start listening to port
		DefaultWriter("[APP START] Listening and serving HTTP on {0}\n".format(self.config.HTTPServer.Listen))
		# start distribute routers
		# return self.server.ListenAndServe()
		start_server(
			applications={"UserLogin": UserLogin, "ShowFileTree": UserLogin, "Download": UserLogin}, 
			port=self.config.HTTPServer.Listen, 
			auto_open_webbrowser=True,
		)

# NewApp establish an APP
def NewApp(ctx: context.Context, c: Config) -> App:
	ctxRet, cancel = context.Context(ctx) #.WithCancel(ctx)
	app = App(
		ctx = ctxRet,
		config = c,
		close = cancel,
	)
	# app.initHTTPServer(handler)
	return app