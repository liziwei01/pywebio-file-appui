'''
Author: liziwei01
Date: 2022-07-10 16:18:35
LastEditors: liziwei01
LastEditTime: 2022-07-11 13:38:27
Description: file content
'''
# /*
#  * @Author: liziwei01
#  * @Date: 2022-03-04 22:06:10
#  * @LastEditors: liziwei01
#  * @LastEditTime: 2022-03-24 23:43:27
#  * @Description: file content
#  */
# package bootstrap

# import (
# 	"context"

# 	"github.com/liziwei01/gin-file-download/library/logit"
# 	"github.com/liziwei01/gin-file-download/middleware"

# 	"github.com/gin-gonic/gin"
# )

# def InitMust(ctx context.Context) {
# 	InitLog(ctx)
# 	InitMiddleware(ctx)
# }

# def InitLog(ctx context.Context) {
# 	logit.Init(ctx, "github.com/liziwei01/gin-file-download")
# }

# def InitRedis() {

# }

# def InitMiddleware(ctx context.Context) {
# 	middleware.Init(ctx)
# }

# # InitHandler 获取http handler
# def InitHandler(app *AppServer) *gin.Engine {
# 	gin.SetMode(app.Config.RunMode)
# 	handler := gin.New()
# 	# 注册log recover中间件
# 	ginRecovery := gin.Recovery()
# 	baiduLogger := logit.LogitMiddleware()
# 	handler.Use(ginRecovery, baiduLogger)
# 	return handler
# }
