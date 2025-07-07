# 2048-CLI

クラシックな2048パズルゲームの、モダンでミニマルなCUI版です。

## インストール

### 📦 バイナリダウンロード（推奨）

最新のビルド済みバイナリを[Releases](https://github.com/your-username/2048-cli/releases)からダウンロードできます：

#### Linux

- **binary**: `2048-cli`
- **AppImage**: `2048-cli-x86_64.AppImage`

```bash
# binaryの場合
chmod +x 2048-cli
./2048-cli

# AppImageの場合
chmod +x 2048-cli-x86_64.AppImage
./2048-cli-x86_64.AppImage
```

#### Windows

- **実行可能ファイル**: `2048-cli.exe`

```cmd
2048-cli.exe
```

### セルフビルド

#### 必要要件

- Python 3.13 以上
- Poetry

#### セットアップ

1. リポジトリをクローン：

   ```bash
   git clone <repository-url>
   cd 2048-cli
   ```

2. 依存関係をインストール：

   ```bash
   poetry install
   ```

3. ゲームを実行：

   ```bash
   poetry run python src/main.py
   ```

#### 代替実行方法

Pythonで直接実行することも可能です：

```bash
python src/main.py
```

#### バイナリビルド

自分でバイナリをビルドしたい場合：

```bash
# Linux/macOS
./build.sh

# Windows
build.bat

# または、Pythonスクリプトで
python build.py
```

## プレイ方法

### デフォルトコントロール

| キー | 動作 |
|-----|-----|
| 矢印キー / WASD | タイルを移動 |
| `h` | カスタム名でゲームを保存 |
| `l` | 保存されたゲームを読み込み |
| `r` | タイトル画面に戻る |
| `q` | ゲームを終了 |

*注: キーバインドはゲーム内でカスタマイズ可能です。*

### メニューナビゲーション

- 矢印キー: メニューオプションを移動
- Enter: オプションを選択
- `q` / Escape: 戻る または 終了

## ゲーム機能

- セーブ/ロード機能
- カスタムキーバインディング
- エンドレスモード

## プロジェクト構造

```text
2048-cli/
├── src/
│   ├── main.py               # エントリーポイント
│   ├── core/
│   │   ├── config.py         # 設定管理
│   │   ├── modern_themes.py  # カラーテーマとスタイリング
│   │   ├── save_load.py      # セーブ/ロード機能
│   │   └── key_display.py    # キーバインディング表示
│   ├── game/
│   │   ├── board.py          # ゲームボードロジック
│   │   └── game.py           # コアゲームロジック
│   └── ui/
│       ├── menu.py           # メニューシステム
│       ├── input.py          # テキスト入力処理
│       └── modern_display.py # レンダリング
├── .github/workflows/        # GitHub Actions CI/CD
│   └── build.yml             # 自動ビルド設定
├── build/                    # ビルド一時ファイル
├── dist/                     # ビルド成果物
├── build.spec                # PyInstaller設定
├── build.py                  # Pythonビルドスクリプト
├── build.sh                  # Linux/macOS用ビルドスクリプト
├── build.bat                 # Windows用ビルドスクリプト
├── config.json               # ゲーム設定
└── pyproject.toml            # プロジェクト設定と依存関係
```

## 設定

ゲーム設定は `config.json` で直接カスタマイズも可能です：

```json
{
  "controls": {
    "up": ["KEY_UP", "w"],
    "down": ["KEY_DOWN", "s"],
    "left": ["KEY_LEFT", "a"],
    "right": ["KEY_RIGHT", "d"]
  }
}
```

## 開発

### 開発環境

- Python 3.13+
- Poetry または pip

### 開発セットアップ

クイックセットアップ:
```bash
# 開発環境を自動セットアップ
./dev-setup.sh
```

手動セットアップ:
```bash
# 開発依存関係をインストール
pip install -e ".[dev]"

# プリコミットフックをインストール（推奨）
pre-commit install

# コード品質チェック
make check
```

### コード品質

このプロジェクトは以下のツールでコード品質を管理しています：

- **Ruff**: 高速なPythonリンター・フォーマッター
- **MyPy**: 静的型チェック
- **Pre-commit**: コミット前の自動チェック

利用可能なコマンド:
```bash
make lint       # リンターを実行
make format     # コードをフォーマット
make type-check # 型チェックを実行
make check      # すべてのチェックを実行
make fix        # 自動修正可能な問題を修正
```

### アーキテクチャ

特に厳密なアーキテクチャはありませんが、表示/ロジックは分離されており、ごく一般的な原則には従っています。

### 主要コンポーネント

- `Game` クラス: ゲーム状態とロジックを管理
- `Board` クラス: タイルの配置と移動を処理
- `modern_display.py`: モダンインターフェースをレンダリング
- `save_load.py`: ゲームの永続化を処理

### ビルドシステム

#### ローカルビルド

```bash
# Linux/macOS
./build.sh

# Windows
build.bat

# Python（全プラットフォーム）
python build.py
```

#### 出力形式

- **Linux**: バイナリ実行可能ファイル + AppImage
- **Windows**: .exe実行可能ファイル
- **macOS**: バイナリ実行可能ファイル（将来: .appバンドル）

#### 自動ビルド

GitHub Actionsにより以下のタイミングで自動ビルドが実行されます：

- `master`/`main`ブランチへのプッシュ
- プルリクエストの作成
- タグ（`v*`）のプッシュ時にリリースを自動作成

#### ビルド設定

- `build.spec`: PyInstallerの設定ファイル
- `.github/workflows/build.yml`: GitHub Actionsワークフロー
- `pyproject.toml`: プロジェクト設定とビルド依存関係

## システム要件

- Python 3.13+
- カラーサポート付きターミナル
- 最小ターミナルサイズ: 80x24（推奨）

## 互換性

- Linux: 完全サポート
- macOS: 完全サポート
- Windows: 適切なターミナル（Windows Terminal推奨）でサポート

## トラブルシューティング

### よくある問題

**ターミナルが小さすぎる**: ターミナルが少なくとも80x24文字であることを確認

**色が表示されない**: ターミナルが256色をサポートしているか確認

**キーバインディングが機能しない**: ターミナルのキーマッピング設定を確認

**セーブファイルが見つからない**: ゲームが自動的に `saves/` ディレクトリを作成

### パフォーマンス

ゲームはターミナルパフォーマンス向けに最適化されています：

- 複雑なアニメーションなし
- 効率的な画面更新
- 最小メモリ使用量
- 高速起動時間

## バージョン履歴

- **v0.1.0**: 根幹的機能のみを実装した仮リリース

## ライセンス

**このプロジェクトはCC0 1.0 Universal (Public Domain Dedication)の下で公開されています。**

このアプリケーションは、コードの大部分がLLMによって生成されているため、作者は著作権を主張せず、パブリックドメインとして公開します。

どなたでも、目的を問わず自由に本ソフトウェアを使用、複製、改変、配布することができます。報告義務やクレジット表記の必要も一切ありません。
ただし、本ソフトウェアは現状有姿で提供され、その利用によって生じたいかなる損害についても、作者は一切の責任を負いません。

ライセンスの正式な条文については、[LICENSE](LICENSE.txt)ファイルをご確認ください。
