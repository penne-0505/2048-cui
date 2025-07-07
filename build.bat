@echo off
REM 2048-CLI Windows Build Script
REM 単一バイナリのみをビルドします

echo 2048-CLI Build Script
echo ====================

REM 依存関係のチェック
echo 依存関係をチェックしています...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pythonが見つかりません
    pause
    exit /b 1
)

REM PyInstallerをインストール
echo PyInstallerをインストールしています...
python -m pip install --user pyinstaller>=5.0.0

REM ビルドディレクトリを作成
echo ビルドディレクトリを作成しています...
if not exist build mkdir build
if not exist dist mkdir dist

REM PyInstallerでビルド
echo 実行可能ファイルをビルドしています...
python -m PyInstaller --clean --onefile --distpath dist --workpath build\temp --specpath build build.spec

if exist dist\2048-cli.exe (
    echo ✅ ビルド完了!
    echo 📁 成果物: dist\
    dir dist\
    echo.
    echo 実行方法:
    echo   dist\2048-cli.exe
) else (
    echo ❌ ビルドに失敗しました
    pause
    exit /b 1
)

pause