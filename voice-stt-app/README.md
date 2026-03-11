# Voice Digit STT App

声で数字（0-9）を認識する Web アプリケーション。GitHub Pages でホスティング可能。

## 🎯 機能

- **音声認識**: 0 から 9 の数字を声で認識
- **WASM 実行**: Pyodide を使用して Python 代码をブラウザで実行
- **サーバーレス**: GitHub Pages のみで動作（バックエンド不要）
- **管理者ページ**: 数字の音声テンプレートを登録・管理

## 📁 プロジェクト構成

```
voice-stt-app/
├── index.html          # ユーザー用：数字認識画面
├── admin.html          # 管理者用：音声テンプレート登録
├── digits.json         # 数字の音声特徴量テンプレート
├── css/
│   └── style.css       # スタイルシート
└── js/
    ├── pyodide_setup.js  # Pyodide 初期化・Python 代码
    ├── audio.js          # 音声録音モジュール
    └── stt.js            # 音声認識ロジック
```

## 🚀 クイックスタート

### 1. 管理者ページで音声テンプレートを登録

1. `admin.html` をブラウザで開く
2. 各数字（0-9）を 3 回ずつ録音
3. 生成された JSON をコピーして `digits.json` に貼り付け

### 2. GitHub Pages にデプロイ

```bash
# GitHub リポジトリにプッシュ
git add .
git commit -m "Initial commit: Voice STT App"
git push origin main
```

### 3. GitHub Pages 設定

1. リポジトリの **Settings** → **Pages** を開く
2. **Source** で `Deploy from a branch` を選択
3. **Branch** で `main` / `(root)` を選択して保存
4. 数分後、`https://[ユーザー名].github.io/[リポジトリ名]/` で公開

## 🔧 使い方

### ユーザー（index.html）

1. ページを読み込む
2. 「クリックして話す」ボタンをクリック
3. 数字を 1 つ発話（例：「さん」）
4. 認識された数字が表示される

### 管理者（admin.html）

1. 各数字の「録音」ボタンをクリック
2. カウントダウン後に数字を発話（2 秒間）
3. 3 回録音すると自動で平均化され登録完了
4. すべての数字を登録後、JSON をコピーして `digits.json` に保存

## ⚙️ 技術スタック

- **フロントエンド**: HTML5, CSS3, JavaScript (ES Modules)
- **音声処理**: Web Audio API
- **WASM ランタイム**: [Pyodide](https://pyodide.org/)
- **数値計算**: NumPy (via Pyodide)
- **ホスティング**: GitHub Pages

## 🔬 音声認識の仕組み

1. **特徴量抽出**: 音声データを FFT（高速フーリエ変換）で周波数解析
2. **次元圧縮**: 16 個の周波数バンドに分割して平均化
3. **パターンマッチング**: コサイン類似度で登録済みテンプレートと比較
4. **閾値判定**: 類似度 80% 以上を有効と判定

## 📝 カスタマイズ

### 認識感度の調整

`js/stt.js` の `recognizeDigit` 関数の閾値を変更：

```javascript
const result = await recognizeDigit(audio, 0.8);  // 0.8 → 0.7 (甘く), 0.9 (厳しく)
```

### 録音時間の変更

`index.html` または `admin.html` の録音時間を変更：

```javascript
const audio = await recordAudio(2500);  // 2500ms → 3000ms (長く)
```

### 特徴量抽出の高度化

`js/pyodide_setup.js` の `get_features_temporal` を使用して時間軸の特徴を追加：

```python
def get_features_temporal(audio_data):
    # 音声を 3 区間に分割して特徴量抽出
    ...
```

## ⚠️ 注意点

- **HTTPS 必須**: `getUserMedia` (マイク) は HTTPS または localhost でのみ動作
- **ブラウザ互換**: Chrome, Firefox, Edge 推奨
- **初期データ**: `digits.json` が空だと認識できないため、必ず登録が必要
- **個人差**: 登録した人の声に近いほど精度が向上

## 📊 精度向上のヒント

1. **静かな環境**: 背景ノイズが少ない場所で登録・認識
2. **はっきり発話**: 「いち」「に」「さん」と明確に
3. **同じトーン**: 登録時と同じ音量・距離で話す
4. **複数回登録**:  admin ページで各数字を 3 回録音（自動平均化）

## 🛠️ 開発

### ローカルでの動作確認

```bash
# ローカルサーバーを起動（HTTPS 推奨）
npx serve .
# または
python -m http.server 8000
```

### ADR (Architecture Decision Record)

詳細な設計判断は `docs/ADR-001.md` を参照（作成予定）。

## 📄 ライセンス

MIT License

## 🙏 謝辞

このプロジェクトは [Pyodide](https://pyodide.org/) のおかげで実現しています。
