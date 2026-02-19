@echo off
echo ========================================
echo 智投项目 - 推送到GitHub
echo ========================================
echo.

echo [1/5] 初始化Git仓库...
git init
echo.

echo [2/5] 添加远程仓库...
git remote add origin https://github.com/hey345437-boop/ai-geo-zhitou.git
echo.

echo [3/5] 添加所有文件...
git add .
echo.

echo [4/5] 创建提交...
git commit -m "Initial commit: 智投 - GEO优化机器学习系统"
echo.

echo [5/5] 推送到GitHub...
git branch -M main
git push -u origin main
echo.

echo ========================================
echo ✅ 推送完成！
echo 仓库地址: https://github.com/hey345437-boop/ai-geo-zhitou
echo ========================================
pause
