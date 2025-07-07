#!/bin/bash

# 2048-CLI Simple Build Script
# 単一バイナリのみをビルドします

set -e

echo "2048-CLI Build Script"
echo "===================="

# 依存関係のチェック
echo "依存関係をチェックしています..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3が見つかりません"
    exit 1
fi

# PyInstallerをインストール
echo "PyInstallerをインストールしています..."
if [ -d "venv" ]; then
    echo "仮想環境を使用してPyInstallerをインストールします..."
    venv/bin/pip install pyinstaller>=5.0.0
else
    echo "システムにPyInstallerをインストールします..."
    python3 -m pip install --user pyinstaller>=5.0.0 || {
        echo "pipでのインストールに失敗しました。仮想環境を作成してください:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -e '.[build]'"
        exit 1
    }
fi

# ビルドディレクトリを作成
echo "ビルドディレクトリを作成しています..."
mkdir -p build dist

# PyInstallerでビルド
echo "実行可能ファイルをビルドしています..."
if [ -d "venv" ]; then
    echo "仮想環境のPythonを使用してビルドします..."
    venv/bin/python -m PyInstaller --clean --distpath dist --workpath build/temp build.spec
else
    python3 -m PyInstaller --clean --distpath dist --workpath build/temp build.spec
fi

echo "✅ ビルド完了!"
echo "📁 成果物: dist/"
ls -la dist/

echo ""
echo "実行方法:"
echo "  ./dist/2048-cli"