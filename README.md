# 2048-CLI

クラシックな2048パズルゲームの、モダンでミニマルなCUI版です。

## インストール

### バイナリダウンロード（推奨）

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

- Python 3.11 以上（3.13 未満）
- Poetry（推奨）または pyproject.toml 対応のパッケージマネージャー

#### セットアップ

1. リポジトリをクローン：

   ```bash
   git clone <repository-url>
   cd 2048-cli
   ```

2. 依存関係をインストール：

   **Poetry + pyenv（推奨）:**
   ```bash
   # Python環境管理と依存関係管理を統合
   pyenv install 3.11.9  # 必要に応じて
   pyenv local 3.11.9
   poetry install
   ```

   **Poetry のみ:**
   ```bash
   poetry install
   ```

   **uv（高速代替手段）:**
   ```bash
   uv sync
   ```

   **pip（最低限）:**
   ```bash
   pip install -e .
   ```

3. ゲームを実行：

   **Poetry:**
   ```bash
   poetry run python src/main.py
   ```

   **uv:**
   ```bash
   uv run python src/main.py
   ```

   **pip:**
   ```bash
   python src/main.py
   ```

#### バイナリビルド

自分でバイナリをビルドしたい場合：

```bash
# Pythonスクリプトでビルド（全プラットフォーム対応）
python build.py

# Makefileを使用（Linux/macOS）
make build
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
- 多言語対応（日本語・英語）
- アニメーション機能（タイル移動、マージ、スポーン）
- 設定メニュー（キーバインディング、アニメーション、言語設定）
- テーマシステム

## プロジェクト構造

```text
2048-cli/
├── src/
│   ├── main.py               # エントリーポイント
│   ├── config_example.json   # 設定ファイルのサンプル
│   ├── core/
│   │   ├── config.py         # 設定管理
│   │   ├── constants.py      # 定数定義
│   │   ├── i18n.py          # 国際化システム
│   │   ├── key_config.py     # キーバインディング設定
│   │   ├── key_display.py    # キーバインディング表示
│   │   ├── modern_themes.py  # カラーテーマとスタイリング
│   │   └── save_load.py      # セーブ/ロード機能
│   ├── game/
│   │   ├── board.py          # ゲームボードロジック
│   │   └── game.py           # コアゲームロジック
│   ├── locales/
│   │   ├── en.json          # 英語翻訳
│   │   └── ja.json          # 日本語翻訳
│   └── ui/
│       ├── animation.py      # アニメーションシステム
│       ├── input.py          # テキスト入力処理
│       ├── key_config_menu.py # キーバインディング設定メニュー
│       ├── menu.py           # メニューシステム
│       ├── modern_display.py # レンダリング
│       └── settings_menu.py  # 設定メニュー
├── .github/workflows/        # GitHub Actions CI/CD
│   └── build.yml             # 自動ビルド設定
├── build/                    # ビルド一時ファイル
├── dist/                     # ビルド成果物
├── build.spec                # PyInstaller設定
├── build.py                  # Pythonビルドスクリプト
├── config.json               # ゲーム設定
├── dev-setup.sh              # 開発環境セットアップスクリプト
├── Makefile                  # ビルドとタスク自動化
└── pyproject.toml            # プロジェクト設定と依存関係
```

## 設定

ゲーム設定は `config.json` で直接カスタマイズも可能です：

```json
{
  "keys": {
    "movement": {
      "up": ["KEY_UP", "w"],
      "down": ["KEY_DOWN", "s"],
      "left": ["KEY_LEFT", "a"],
      "right": ["KEY_RIGHT", "d"]
    },
    "actions": {
      "quit": ["q", "ESC"],
      "save": ["h"],
      "return_to_title": ["r"],
      "load": ["l"],
      "change_theme": ["t"]
    }
  },
  "theme": "modern",
  "language": "en",
  "save_path": null,
  "animations": {
    "enabled": false,
    "speed": 1.0,
    "fps": 60
  },
  "ui": {
    "emoji_enabled": false
  }
}
```

### 言語設定

ゲームは日本語と英語に対応しています。言語設定は以下の方法で変更できます：

- ゲーム内の設定メニューから変更
- `config.json` の `language` 設定を変更（`"en"` または `"ja"`）
- 絵文字表示の有効/無効は `ui.emoji_enabled` で設定

### アニメーション設定

タイル移動、マージ、スポーンのアニメーションを設定できます：

- `animations.enabled`: アニメーションの有効/無効
- `animations.speed`: アニメーション速度（0.5-2.0）
- `animations.fps`: フレームレート（30-120）

## 開発

### 開発環境

- Python 3.11+（3.13 未満）
- Poetry

### 開発セットアップ

クイックセットアップ:
```bash
# 開発環境を自動セットアップ
./dev-setup.sh
```

手動セットアップ:

**Poetry + pyenv（推奨）:**
```bash
# Python環境とパッケージ管理を統合
pyenv install 3.11.9  # 必要に応じて
pyenv local 3.11.9
poetry install --with dev

# プリコミットフックをインストール（推奨）
poetry run pre-commit install

# コード品質チェック
make check
```

**uv（代替手段）:**
```bash
# 高速な依存関係管理
uv sync --extra dev

# プリコミットフックをインストール（推奨）
uv run pre-commit install

# コード品質チェック
make check
```

**pip（最低限）:**
```bash
# 基本的な依存関係管理
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

特に厳密なアーキテクチャはありませんが、インターフェイス/ロジックは分離されており、ごく一般的な原則には従っています。

### 主要コンポーネント

- `Game` クラス: ゲーム状態とロジックを管理
- `Board` クラス: タイルの配置と移動を処理
- `modern_display.py`: モダンインターフェースをレンダリング
- `save_load.py`: ゲームの永続化を処理

### ビルドシステム

#### ローカルビルド

```bash
# Pythonスクリプトでビルド（全プラットフォーム対応）
python build.py

# Makefileを使用（Linux/macOS）
make build
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

- Python 3.11+（3.13 未満）
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
