@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist release mkdir release
if not exist release\assets mkdir release\assets
if not exist release\assets\images mkdir release\assets\images
if not exist release\data mkdir release\data
if not exist release\data\question-banks mkdir release\data\question-banks

copy /Y index.html release\
copy /Y app.js release\
copy /Y styles.css release\
copy /Y study-hub.js release\
copy /Y gratitude.js release\
copy /Y mastery.js release\
copy /Y VERSION release\
copy /Y CHANGELOG.md release\
copy /Y 发布打包.bat release\
copy /Y CONTRIBUTING.md release\
copy /Y README_EN.md release\
if not exist release\docs mkdir release\docs
xcopy /E /Y /I docs release\docs
copy /Y FINAL_PRODUCT_MANUAL.md release\
copy /Y PARENT_GUIDE.md release\
copy /Y DEPLOY.md release\
rem release\启动.bat is a launcher stub — do not overwrite with root 启动.bat
xcopy /E /Y /I assets release\assets
xcopy /E /Y /I data release\data
if not exist release\scripts mkdir release\scripts
xcopy /E /Y /I scripts release\scripts
if not exist release\.github mkdir release\.github
xcopy /E /Y /I .github release\.github
if not exist release\manifests mkdir release\manifests
if exist manifests xcopy /E /Y /I manifests release\manifests

echo.
echo [完成] release 目录已同步为最新运行包。
if /I not "%~1"=="nopause" pause
