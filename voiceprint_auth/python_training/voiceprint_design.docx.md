  
**VOICEPRINT // SPEAKER.ID**

詳細設計書

| 項目 | 内容 |
| :---- | :---- |
| 文書番号 | VPID-DD-001 |
| バージョン | 1.0 |
| 作成日 | 2026-03-10 |
| ステータス | Draft |
| 技術スタック | PWA / Pyodide / MFCC / WebAudio API |
| 対象環境 | モダンブラウザ（Chrome 90+ / Firefox 88+ / Safari 15+） |

# **1\. システム概要**

本書はブラウザ完結型話者識別システム「VOICEPRINT // SPEAKER.ID」の詳細設計を記述する。本システムはPWA（Progressive Web App）としてオフライン動作し、Pyodide（WebAssembly上のCPython）を用いてブラウザ内でMFCC（メル周波数ケプストラム係数）抽出と話者照合を実施する。サーバーサイドへの音声データ送信は一切行わない。

## **1.1 設計方針**

* ゼロサーバー：全処理をクライアント（ブラウザ）内で完結

* プライバシーファースト：音声データはメモリ内のみで処理・保持

* Pure Python DSP：MFCC計算はnumpy/scipy依存のスクラッチ実装

* PWA対応：Service Workerによるオフラインキャッシュ（将来拡張）

## **1.2 システム構成図**

【ブラウザ内処理フロー】

マイク入力（getUserMedia）

  └─ Web Audio API（AudioContext / MediaRecorder）

       └─ Blob → ArrayBuffer → AudioBuffer（decodeAudioData）

            └─ Float32Array（PCMサンプル列）

                 └─ Pyodide（CPython on WASM）

                      ├─ numpy / scipy

                      └─ MFCC Engine（Pure Python）

                           ├─ 登録モード → speakerProfiles（JS Object）

                           └─ 識別モード → コサイン類似度 → 結果表示

# **2\. モジュール詳細設計**

## **2.1 初期化モジュール（initPyodide）**

アプリケーション起動時に一度だけ実行され、Pyodide実行環境を構築する。

| 処理ステップ | 詳細 | 失敗時挙動 |
| :---- | :---- | :---- |
| Pyodideロード | cdn.jsdelivr.net/pyodide/v0.25.1 からJS・WASMを取得 | オーバーレイにエラー表示 |
| numpy ロード | loadPackage('numpy') を呼び出し | 同上 |
| scipy ロード | loadPackage('scipy') を呼び出し | 同上 |
| MFCCエンジンコンパイル | Python文字列をrunPythonAsync()で評価・グローバル登録 | 同上 |
| 初期化完了 | ローディングオーバーレイを非表示 | — |

## **2.2 音声入力モジュール（startRecord / stopRecord）**

### **2.2.1 入力仕様**

| パラメータ | 値 | 備考 |
| :---- | :---- | :---- |
| 取得API | navigator.mediaDevices.getUserMedia | audio:true, video:false |
| 録音形式 | MediaRecorder（audio/webm） | ブラウザのデフォルトコーデック |
| 自動停止 | 3000ms | setTimeout によるauto-stop |
| サンプリングレート | ブラウザデフォルト（通常44100Hz） | decodeAudioData後にsr取得 |

### **2.2.2 デコード処理**

MediaRecorder出力のBlob（audio/webm）を以下の手順でPCMサンプルに変換する。

1. Blob → ArrayBuffer（blob.arrayBuffer()）

2. ArrayBuffer → AudioBuffer（AudioContext.decodeAudioData()）

3. AudioBuffer.getChannelData(0) → Float32Array（ch.0モノラル）

4. Array.from() でJS配列化 → Pyodideへ渡す

# **3\. MFCCエンジン設計（Python / Pyodide）**

## **3.1 パラメータ仕様**

| パラメータ名 | デフォルト値 | 説明 |
| :---- | :---- | :---- |
| sr | 44100 | サンプリングレート（Hz） |
| n\_mfcc | 13 | 出力MFCC係数次元数 |
| n\_filters | 26 | メルフィルタバンク数 |
| n\_fft | 2048 | FFTサイズ（サンプル数） |
| hop | 512 | フレームシフト（サンプル数） |
| f\_min | 0 | メルフィルタ最低周波数（Hz） |
| f\_max | sr/2 | メルフィルタ最高周波数（Hz） |
| preemphasis\_coeff | 0.97 | プリエンファシス係数 |

## **3.2 処理パイプライン**

### **3.2.1 プリエンファシス**

高域強調フィルタ。係数0.97で高周波成分を補強し、スペクトル推定の精度を改善する。

y\[n\] \= x\[n\] \- 0.97 \* x\[n-1\]  （n \>= 1）

y\[0\] \= x\[0\]

### **3.2.2 フレーム分割 \+ 窓関数**

n\_fft=2048サンプル単位にhop=512ずつスライドしながらフレームを切り出す。各フレームにハミング窓を乗算してスペクトル漏れを抑制する。

window \= scipy.signal.get\_window('hamming', n\_fft)

frame\[i\] \= signal\[i\*hop : i\*hop \+ n\_fft\] \* window

### **3.2.3 FFT → パワースペクトル**

各フレームにDFTを適用し、片側パワースペクトルを算出する。

spectrum \= |fft(frame)|\[:n\_fft//2 \+ 1\]

power    \= spectrum \*\* 2

### **3.2.4 メルフィルタバンク**

n\_filters=26個の三角フィルタをメルスケール上で等間隔に配置し、パワースペクトルに適用する。フィルタ出力がゼロのビンはeps（最小浮動小数点値）で置換する。

mel\_min \= 2595 \* log10(1 \+ f\_min/700)

mel\_max \= 2595 \* log10(1 \+ f\_max/700)

mel\_pts \= linspace(mel\_min, mel\_max, n\_filters+2)

hz\_pts  \= 700 \* (10^(mel\_pts/2595) \- 1\)

### **3.2.5 対数変換 \+ DCT**

メルエネルギーの対数を取った後、離散コサイン変換（DCT-II相当）を適用してケプストラル係数を得る。先頭n\_mfcc=13個を使用する。

log\_mel \= log(mel\_energy)

mfcc\[n\] \= Σ log\_mel\[m\] \* cos(π\*n\*(m+0.5)/M)  (n=0..n\_mfcc-1)

### **3.2.6 フレーム平均化**

全フレームのMFCCベクトルを算数平均し、発話全体を代表する13次元ベクトルを生成する。このベクトルが話者プロファイルとして保存・照合に使われる。

mfcc\_vec \= mean(frames, axis=0)  →  shape: (13,)

# **4\. 話者管理・照合モジュール設計**

## **4.1 データ構造**

話者プロファイルはJavaScriptオブジェクトとしてメモリ内に保持される。永続化は現バージョンでは行わない。

speakerProfiles \= {

  'ALICE': \[ \[v1\_0, v1\_1, ... v1\_12\],   // サンプル1

             \[v2\_0, v2\_1, ... v2\_12\] \],  // サンプル2

  'BOB':   \[ \[v3\_0, ...\] \]

}

## **4.2 登録フロー**

1つの話者に対して複数回登録することで照合精度が向上する（3回以上推奨）。

| ステップ | 処理内容 |
| :---- | :---- |
| 1\. 名前入力 | speakerName InputにUPPERCASE変換して格納（未入力時は'UNKNOWN'） |
| 2\. 録音 | startRecord('register') → 3秒録音 |
| 3\. MFCC抽出 | processAudio() → Python extract\_mfcc() → 13次元ベクトル |
| 4\. プロファイル追加 | speakerProfiles\[name\].push(mfccVec) |
| 5\. リスト更新 | renderSpeakerList() でUI再描画 |

## **4.3 識別フロー**

| ステップ | 処理内容 |
| :---- | :---- |
| 1\. 録音 | startRecord('identify') → 3秒録音 |
| 2\. MFCC抽出 | 同上（登録時と同一パイプライン） |
| 3\. 全話者スキャン | speakerProfilesの全名前に対してループ |
| 4\. サンプル平均類似度 | 各サンプルとのコサイン類似度を算出し平均 |
| 5\. 最高スコア選択 | 最大平均スコアの話者を候補とする |
| 6\. 閾値判定 | スコア \>= 0.85 → 識別成功 / スコア \< 0.85 → UNKNOWN |

## **4.4 コサイン類似度**

2つのMFCCベクトルa, bの類似度を以下の式で計算する。値域は\[-1, 1\]で1に近いほど類似している。

cosine\_sim(a, b) \= dot(a, b) / (||a|| \* ||b||)

| スコア範囲 | 判定 | 信頼度表示 |
| :---- | :---- | :---- |
| 0.85 以上 | 識別成功（話者名表示） | バープログレスで視覚化 |
| 0.85 未満 | UNKNOWN（識別失敗） | 警告表示 |

# **5\. UI / UX 設計**

## **5.1 レイアウト構成**

| コンポーネント | 役割 | 備考 |
| :---- | :---- | :---- |
| ヘッダー | システム名・稼働ステータス表示 | パルスアニメーション付きLEDドット |
| 波形キャンバス | 録音中リアルタイム波形表示 | requestAnimationFrame \+ analyser |
| MFCCキャンバス | 録音後エネルギー分布プレビュー | 40チャンク×エネルギーバー |
| モードタブ | 登録/識別モード切替 | CSSクラストグル |
| 登録パネル | 話者名入力・録音ボタン・プロファイル一覧 | 登録モードのみ表示 |
| 識別パネル | 録音ボタン・結果表示エリア | 識別モードのみ表示 |
| ログエリア | システムイベントのリアルタイム出力 | タイムスタンプ付き |
| ローディングオーバーレイ | Pyodide初期化中の全画面表示 | アニメーションバー付き |

## **5.2 ビジュアルデザイン**

| 要素 | 値 |
| :---- | :---- |
| テーマ | サイバーパンク / バイオメトリクス |
| 背景色 | \#020408（ほぼ黒）+ グリッドテクスチャ（CSS） |
| アクセントカラー1 | \#00ff9f（アシッドグリーン）— 主要操作・ステータス |
| アクセントカラー2 | \#00cfff（サイアン）— 情報・識別系 |
| 警告色 | \#ff4060（レッド）— エラー・UNKNOWN結果 |
| フォント | Share Tech Mono（等幅）/ Rajdhani（見出し） |
| アニメーション | 波形描画・録音点滅・結果バー遷移・ローディングアニメ |

# **6\. 非機能要件**

## **6.1 パフォーマンス**

| 項目 | 目標値 | 備考 |
| :---- | :---- | :---- |
| 初期ロード時間（初回） | 〜15秒 | Pyodide+numpy+scipy DL込み（約10MB） |
| 初期ロード時間（2回目以降） | 〜2秒 | ブラウザキャッシュ利用時 |
| MFCC処理時間 | \< 1秒 | 3秒音声 / M1 Mac Chrome基準 |
| 識別処理時間 | \< 0.5秒 | 登録話者10名 / サンプル3件/名 |
| メモリ使用量 | \< 300MB | Pyodideヒープ含む |

## **6.2 ブラウザ互換性**

| ブラウザ | 最低バージョン | 制限事項 |
| :---- | :---- | :---- |
| Chrome / Edge | 90+ | なし（フルサポート） |
| Firefox | 88+ | なし（フルサポート） |
| Safari | 15+ | getUserMedia要https必須 |
| モバイルChrome | 90+ | 画面レイアウトは1カラム |
| IE / 旧Edge | 非対応 | WebAssembly非対応 |

## **6.3 セキュリティ・プライバシー**

* 音声データはブラウザメモリのみで処理し、外部サーバーへの送信はしない

* 話者プロファイル（MFCCベクトル）はページ閉鎖時に消失（永続化なし）

* マイクアクセスはブラウザ標準のパーミッション要求に従う

* HTTPS環境でのみgetUserMediaが動作する（localhost除く）

# **7\. 制限事項・既知課題**

| No. | 課題 | 影響度 | 対応方針 |
| :---- | :---- | :---- | :---- |
| 1 | 初回ロード時間が長い（Pyodide \+ packages） | 中 | Service Workerによる事前キャッシュで改善可能 |
| 2 | 話者プロファイルの永続化がない | 中 | IndexedDB or localStorage保存を将来実装 |
| 3 | 背景雑音に弱い（前処理なし） | 高 | VAD（音声区間検出）の追加を推奨 |
| 4 | MFCCデルタ特徴量未使用 | 中 | 精度改善のためデルタ・デルタデルタ追加を推奨 |
| 5 | コサイン類似度のみで話者モデリング | 中 | GMM-UBMまたはd-vectorへの移行を検討 |
| 6 | 閾値0.85がハードコード | 低 | ユーザー調整UIの追加を推奨 |
| 7 | 多チャンネル音声はch.0のみ使用 | 低 | 現状問題なし |

# **8\. 将来拡張計画**

| 優先度 | 機能 | 技術的アプローチ |
| :---- | :---- | :---- |
| 高 | IndexedDBによるプロファイル永続化 | pyodide.runPythonAsync内からJSブリッジ経由で保存 |
| 高 | Service Workerによるオフラインキャッシュ | Workbox または手動SW登録 |
| 中 | d-vector / ECAPA-TDNNへの移行 | ONNX Runtime Web \+ 事前学習済みモデル |
| 中 | リアルタイムストリーミング識別 | AudioWorkletで逐次フレーム処理 |
| 中 | VAD（音声区間検出）統合 | WebRTC VAD またはsilero-vadのWASM移植 |
| 低 | MFCCデルタ特徴量追加 | extract\_mfcc()にdelta/delta-delta計算を追加 |
| 低 | 話者数上限・類似度ランキング表示 | UIの結果パネル拡張 |

# **付録A. 依存ライブラリ一覧**

| ライブラリ | バージョン | 用途 | 配布元 |
| :---- | :---- | :---- | :---- |
| Pyodide | 0.25.1 | Python on WebAssembly ランタイム | cdn.jsdelivr.net/pyodide |
| numpy | Pyodide同梱 | 配列演算・数値計算 | Pyodide package |
| scipy | Pyodide同梱 | FFT・窓関数 | Pyodide package |
| Google Fonts | — | Share Tech Mono / Rajdhani | fonts.googleapis.com |

# **付録B. 関数インターフェース一覧**

| 関数名 | 言語 | 引数 | 戻り値 | 説明 |
| :---- | :---- | :---- | :---- | :---- |
| extract\_mfcc | Python | audio\_list, sr, n\_mfcc, n\_filters, n\_fft, hop | list\[float\] (13次元) | MFCCベクトル抽出 |
| cosine\_sim | Python | a: list, b: list | float \[-1, 1\] | コサイン類似度計算 |
| initPyodide | JS | なし | Promise\<void\> | Pyodide初期化 |
| startRecord | JS | mode: 'register'|'identify' | Promise\<void\> | 録音開始 |
| stopRecord | JS | なし | void | 録音停止 |
| processAudio | JS | mode: string | Promise\<void\> | 音声デコード+MFCC実行 |
| registerSpeaker | JS | mfccVec: number\[\] | void | 話者プロファイル追加 |
| identifySpeaker | JS | mfccVec: number\[\] | Promise\<void\> | 話者識別実行 |
| showResult | JS | name: string|null, score: float | void | 識別結果表示 |

