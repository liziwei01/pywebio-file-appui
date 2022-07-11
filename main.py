'''
Author: liziwei01
Date: 2022-07-10 09:18:15
LastEditors: liziwei01
LastEditTime: 2022-07-11 13:44:10
Description: file content
'''
import bootstrap
import os

def main():
	app, err = bootstrap.Setup()
	if err != None:
		print(err)
		os.abort()
	# 注册接口路由
	# httpapi.InitRouters(app.Handler)

	app.Start()
