'''
Author: liziwei01
Date: 2022-07-10 16:19:39
LastEditors: liziwei01
LastEditTime: 2022-07-10 17:49:25
Description: file content
'''
import os
from typing import Sequence
from library import error

# var
pid: int
pidstr: str
localIP = "unknown"


# PID 得到 PID
def PID() -> int:
	return pid

# PIDstr 得到PID 字符串形式
# 如打印日志的场景
def PIDstr() -> str:
	return pidstr

# LocalIP 本机IP，返回非127域的第一个ipv4 地址
# 极端特殊情况获取失败返回 机器名 或者 unknown
def LocalIP() -> str:
	return localIP

def init() -> None:
	global pid, pidstr, localIP
	pid = os.getpid()
	pidstr = str(pid)
	val, err = localIPV4()
	if err == None:
		localIP = val

# TODO: 实现获取本机ipv4地址
def localIPV4() -> Sequence[str, error]:
	return "127.0.0.1", None
	# addrs, err = net.InterfaceAddrs()
	# if err != None:
	#	 return os.Hostname()
		
	# for a in addrs:
	#	 ipnet, ok := a.(*net.IPNet)
	#	 if ok and not ipnet.IP.IsLoopback():
	#		 if ipnet.IP.To4() != None:
	#			 return ipnet.IP.str(), None
				
	# return "", "fail to get local ip"
