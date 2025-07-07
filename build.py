#!/usr/bin/env python3
"""
2048-CLI ビルドスクリプト
単一バイナリのみをビルドします。
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """コマンドを実行し、エラーがあれば終了"""
    print(f"実行中: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, cwd=cwd, capture_output=True, text=True)
        print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"エラー: {e}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def check_dependencies():
    """必要な依存関係をチェック"""
    print("依存関係をチェックしています...")
    
    # PyInstallerをチェック
    try:
        import PyInstaller
        print(f"PyInstaller {PyInstaller.__version__} が見つかりました")
    except ImportError:
        print("PyInstallerが見つかりません。インストールしています...")
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0.0"])


def build_executable():
    """PyInstallerで実行可能ファイルをビルド"""
    print("実行可能ファイルをビルドしています...")
    
    # PyInstallerでビルド
    run_command([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onefile",
        "--distpath", "dist",
        "--workpath", "build/temp",
        "--specpath", "build",
        "build.spec"
    ])
    
    return Path("dist/2048-cli")


def main():
    """メイン処理"""
    print("2048-CLI ビルドスクリプト")
    print("=" * 40)
    
    # 依存関係をチェック
    check_dependencies()
    
    # ビルドディレクトリを作成
    Path("build").mkdir(exist_ok=True)
    Path("dist").mkdir(exist_ok=True)
    
    # 実行可能ファイルをビルド
    exe_path = build_executable()
    
    if exe_path.exists():
        print(f"✓ 実行可能ファイルが作成されました: {exe_path}")
    else:
        print("✗ 実行可能ファイルの作成に失敗しました")
        sys.exit(1)
    
    print("\nビルド完了!")
    print("distディレクトリを確認してください。")


if __name__ == "__main__":
    main()