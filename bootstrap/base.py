'''
Author: liziwei01
Date: 2022-07-10 16:18:35
LastEditors: liziwei01
LastEditTime: 2022-07-11 13:42:45
Description: file content
'''
from app import *
from mxnet import context
from typing import Sequence
from library import error
from library import env

appConfPath = "./conf/app.toml"

# AppServer struct.
class AppServer:
	# Handler *gin.Engine
	ctx: context.Context
	config: Config
	# Cancel: context.CancelFunc

	def __init__(self, ctx: context.Context | None, config: Config | None):
		self.ctx = ctx
		self.config = config
		# self.Cancel = cancel
		# self.Handler = None

	# Start 启动http服务器.
	def Start(self) -> None:
		app = NewApp(self.ctx, self.config)
		app.Start()

# Setup 准备.
def Setup() -> Sequence[AppServer, error]:
	appServer = AppServer()
	appServer.config, err = ParserAppConfig(appConfPath)
	if err != None:
		return None, err
	env.Default = appServer.config.Env
	# appServer.Ctx, appServer.Cancel = context.WithCancel(context.Background())
	appServer.ctx = context.Context()
	# InitMust(appServer.Ctx)
	# appServer.Handler = InitHandler(appServer)

	return appServer, None

# SetupScript 准备.
def SetupScript(conf: str | None) -> Sequence[AppServer, error]:
	cPath = appConfPath
	if conf != None:
		cPath = conf

	appServer = AppServer()
	appServer.config, err = ParserAppConfig(appConfPath)
	if err != None:
		return None, err
	env.Default = appServer.config.Env
	# appServer.Ctx, appServer.Cancel = context.WithCancel(context.Background())
	appServer.ctx = context.Context()
	# InitMust(appServer.Ctx)
	# appServer.Handler = InitHandler(appServer)

	return appServer, None

