#初始化项目目录变量
HOMEDIR := $(shell pwd)
OUTDIR  := $(HOMEDIR)/output

# 可以修改为其他的名字
APPNAME = $(shell basename `pwd`)
#初始化命令变量
# PYROOT  := /usr/local/python
# PY      := $(PYROOT)/bin/python
PY      := $(shell which python3)
# PYTEST  := $(PY) test

# 执行编译，可使用命令 make 或 make all 执行, 顺序执行prepare -> compile -> test -> package 几个阶段
all: compile package

# prepare阶段, 可单独执行命令: make prepare
# prepare: prepare-dep
# prepare-dep:
# 	git config --global http.sslVerify false
set-env:
	$(PY) env -w PYPROXY=https://goproxy.cn,direct
	$(PY) env -w PYNOSUMDB=\*
	
# complile阶段，执行编译命令,可单独执行命令: make compile
compile:build
build: set-env
	$(PYMOD) download #下载Go依赖
	$(PYBUILD) -o $(HOMEDIR)/bin/$(APPNAME)

# test阶段，进行单元测试， 可单独执行命令: make test
test: test-case
test-case: set-env
	$(PYTEST) -race -v -cover $(PYPKGS) -gcflags="-N -l"
	
# package阶段，对编译产出进行打包，输出到output目录, 可单独执行命令: make package
package: package-bin
package-bin:
	$(shell rm -rf $(OUTDIR))
	$(shell mkdir -p $(OUTDIR))
	$(shell cp -a bin $(OUTDIR)/bin)
	$(shell cp -a conf_online $(OUTDIR)/conf)
	$(shell if [ -d "data_online"  ]; then cp -r data_online $(OUTDIR)/data; fi)
	$(shell if [ -d "noahdes"  ]; then cp -r noahdes $(OUTDIR)/; fi)

# clean阶段，清除过程中的输出, 可单独执行命令: make clean
clean:
	rm -rf $(OUTDIR)

# avoid filename conflict and speed up build
# .PHONY: all prepare compile test package  clean build
.PHONY: all compile test package  clean build
