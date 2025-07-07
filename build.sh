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
python3 -m pip install --user pyinstaller>=5.0.0

# ビルドディレクトリを作成
echo "ビルドディレクトリを作成しています..."
mkdir -p build dist

# PyInstallerでビルド
echo "実行可能ファイルをビルドしています..."
python3 -m PyInstaller --clean --onefile --distpath dist --workpath build/temp --specpath build build.spec

echo "✅ ビルド完了!"
echo "📁 成果物: dist/"
ls -la dist/

echo ""
echo "実行方法:"
echo "  ./dist/2048-cli"