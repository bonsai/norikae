# 🔐 Micro:bit Smart Lock

> **スマホをポケットに入れたまま、ドアに近づくだけで自動解錠**
> 
> povo 2.0 と古いスマホを活用した、月額ほぼ 0 円の DIY スマートロック

---

## 📋 目次

- [概要](#-概要)
- [システム構成](#-システム構成)
- [特徴](#-特徴)
- [必要なもの](#-必要なもの)
- [クイックスタート](#-クイックスタート)
- [ハードウェア設計](#-ハードウェア設計)
- [ソフトウェア](#-ソフトウェア)
- [UX 設計](#-ux-設計)
- [コスト](#-コスト)
- [FAQ](#-faq)
- [ライセンス](#-ライセンス)

---

## 🎯 概要

このプロジェクトは、**Micro:bit v2** と **サーボモーター**、そして **povo 2.0 を挿した古いスマホ** を活用して、本格的なスマートロックを自作するものです。

### 実現できること

| 機能 | 説明 |
|------|------|
| 🚶 **自動解錠** | 自宅に近づくだけで GPS が反応して自動解錠 |
| 📱 **リモート操作** | Blynk アプリで外出先からも操作可能 |
| 🔔 **通知機能** | 解錠・施錠時にスマホへプッシュ通知 |
| 🔋 **低電力運用** | povo 2.0 の 128kbps で十分動作 |
| 🛠️ **手動 Override** | 磁気結合で手動操作も可能（家族も使える） |

---

## 🏗️ システム構成

```
┌─────────────────────────────────────────────────────────────────┐
│                         外出先                                 │
│  ┌──────────────┐                                              │
│  │ メインスマホ  │ GPS 検知 → Blynk クラウドへ送信               │
│  │ (Blynk App)  │                                              │
│  └──────────────┘                                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓ (4G/5G)
┌─────────────────────────────────────────────────────────────────┐
│                          自宅                                   │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │ povo スマホ   │ ←── │   Micro:bit  │ ──→ │   サーボ     │   │
│  │ (Blynk Gateway)│ BT │   v2         │ 信号 │   MG90S      │   │
│  └──────────────┘     └──────────────┘     └──────┬───────┘   │
│                                                    │           │
│                                              ┌─────▼─────┐     │
│                                              │ サムターン │     │
│                                              │  (鍵)     │     │
│                                              └───────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### 通信フロー

1. **GPS トリガー**: メインスマホが自宅半径 100m 以内に進入
2. **Blynk クラウド**: 位置情報を検知してコマンド送信
3. **povo スマホ**: 128kbps 回線でコマンド受信
4. **Bluetooth**: Micro:bit へ指令転送
5. **サーボ動作**: 0°（解錠）または 90°（施錠）へ回転

---

## ✨ 特徴

### 🎁 他製品との比較

| 製品 | 価格 | 月額 | GPS 自動 | 手動 Override | 改造必要 |
|------|------|------|----------|---------------|----------|
| **本プロジェクト** | ¥7,550 | ¥0* | ✅ | ✅ | あり |
| SwitchBot Lock | ¥12,800 | ¥0 | ❌ | ✅ | なし |
| SESAME 5 | ¥19,800 | ¥0 | ✅ | ✅ | なし |
| Native (Amazon) | ¥29,800 | ¥0 | ✅ | ❌ | なし |

\* povo 2.0 は 180 日に 1 回トッピング購入が必要（最低¥330）

### 🔥 独自の強み

1. **磁気結合クラッチ機構**
   - サーボと鍵を磁石で結合
   - 手動で回すと空回り（ギア破損防止）
   - 家族が普通に鍵を使える

2. **povo 2.0 活用**
   - 月額基本料¥0
   - 128kbps でも IoT 制御には十分
   - 古いスマホの有効活用

3. **完全カスタマイズ可能**
   - オープンソース設計
   - 3D プリントで自分好みのホルダー
   - コードも自由に改造

---

## 🛒 必要なもの

### 必須コンポーネント

| # | 部品 | 仕様 | 数量 | 単価 | 小計 |
|---|------|------|------|------|------|
| 1 | **Micro:bit v2** | BBC 製 | 1 | ¥2,500 | ¥2,500 |
| 2 | **サーボモーター** | MG90S（金属ギア） | 1 | ¥1,000 | ¥1,000 |
| 3 | **ネオジム磁石** | 6mm×3mm N52 | 2 | ¥50 | ¥100 |
| 4 | **電池ボックス** | 単三×4 本用 | 1 | ¥300 | ¥300 |
| 5 | **充電池** | エネループ×4 | 1 | ¥1,000 | ¥1,000 |
| 6 | **ジャンパーワイヤ** | メス - メス | 3 | ¥100 | ¥300 |
| 7 | **Command ストリップ** | 大サイズ | 1 | ¥500 | ¥500 |
| 8 | **povo SIM** | nano-SIM | 1 | ¥550 | ¥550 |
| 9 | **古いスマホ** | Android/iOS | 1 | ¥5,000 | ¥5,000 |
| 10 | **3D プリント** | PLA/PETG | 1 | ¥1,500 | ¥1,500 |
| | **合計** | | | | **¥12,750** |

### 工具

- 小型プラスドライバー
- 紙ヤスリ（220 番）
- 消毒用エタノール
- 定規またはノギス

---

## 🚀 クイックスタート

### ステップ 1: ハードウェア準備（1 時間）

```bash
1. サーボホルダーを 3D プリント
   └─ files/hardware/servo-holder/ から STL ファイルを使用

2. 磁石をホルダーに埋め込む
   ⚠️ 極性に注意（同じ極が外向き）

3. サーボをホルダーに取り付け
   └─ M2 ネジで固定

4. Micro:bit と配線
   P0  ── オレンジ（信号）
   GND ── ブラウン（アース）
   電池 + ── レッド（電源）
```

### ステップ 2: Micro:bit プログラム（30 分）

MakeCode で以下のコードを作成：

```javascript
// Blynk 拡張機能を追加
blynk.onVirtualPinWrite(1, function(value) {
    let target = parseInt(value);
    
    if (target === 1) {
        // 解錠
        pins.servoWritePin(AnalogPin.P0, 0);
        basic.showIcon(IconNames.Happy);
        music.playTone(523, music.beat(BeatFraction.Half));
    } else {
        // 施錠
        pins.servoWritePin(AnalogPin.P0, 90);
        basic.showIcon(IconNames.Asleep);
        music.playTone(262, music.beat(BeatFraction.Half));
    }
    
    // 状態を同期
    basic.pause(1000);
    blynk.virtualWrite(2, target);
});

radio.setGroup(1);
```

[▶️ **MakeCode で開く**](https://makecode.microbit.org/)

### ステップ 3: Blynk 設定（20 分）

1. **Blynk IoT アプリ**をインストール
2. **テンプレート**を作成
   - デバイスタイプ: `Micro:bit`
   - 接続タイプ: `Bluetooth`
3. **Datastreams** を設定
   - `V1`: Integer (0-1) - 制御用
   - `V2`: Integer (0-1) - 状態表示用
4. **Dashboard** を作成
   - Button ウィジェット（V1）
   - LED インジケータ（V2）

### ステップ 4: GPS 自動化設定（10 分）

1. Blynk アプリで **Automation** タブを開く
2. **Create Automation** → **Location**
3. 自宅住所を入力、半径 100m を設定
4. トリガー: **Enter Area**
5. アクション: **V1 = 1**（解錠）
6. 同様に **Exit Area** で **V1 = 0**（施錠）を設定

### ステップ 5: 取り付け（30 分）

```
1. ドア枠の清掃（エタノール）
2. Command ストリップをサーボに貼付
3. 位置合わせ（サムターンとホルダー）
4. 1 時間放置（接着剤硬化）
5. 動作テスト
```

---

## 🔧 ハードウェア設計

### サーボホルダー

詳細は [`hardware/servo-holder/`](hardware/servo-holder/) を参照

#### 設計コンセプト

```
┌─────────────────────────────────────────────────────────┐
│                    ドア面                               │
│  ┌─────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │  Servo  │────▶│  Magnet A   │ ◯ │  Magnet B   │──▶│ Thumb-turn │
│  │ (固定)  │     │ (サーボ側)  │ ◯ │ (ホルダー側)│   │            │
│  └─────────┘     └─────────────┘     └─────────────┘   │
│                         │                    │          │
│                    [2-3mm 隙間]         [固定]          │
└─────────────────────────────────────────────────────────┘
```

**磁気結合の利点:**
- ✅ 手動操作時に空回り（ギア保護）
- ✅ 取り付けが簡単（位置調整不要）
- ✅ 非常時でも物理キー使用可能

### 3D プリント設定

| パラメータ | 値 |
|-----------|-----|
| 材料 | PETG（推奨）または PLA+ |
| レイヤー高 | 0.2mm |
| インフィル | 100% |
| 壁厚 | 1.2mm (3 perimeters) |
| サポート | 不要 |

---

## 💻 ソフトウェア

### Micro:bit ファームウェア

[`firmware/main.ts`](firmware/main.ts)

```typescript
// 完全なコード例
// Blynk 仮想ピン V1: 制御（0=施錠，1=解錠）
// Blynk 仮想ピン V2: 状態フィードバック

let lockState = 0;

blynk.onVirtualPinWrite(1, function(value) {
    let target = parseInt(value);
    
    if (target === 1 && lockState !== 1) {
        // 解錠処理
        pins.servoWritePin(AnalogPin.P0, 0);
        basic.showIcon(IconNames.Happy);
        music.playTone(523, music.beat(BeatFraction.Half));
        lockState = 1;
    } else if (target === 0 && lockState !== 0) {
        // 施錠処理
        pins.servoWritePin(AnalogPin.P0, 90);
        basic.showIcon(IconNames.Asleep);
        music.playTone(262, music.beat(BeatFraction.Half));
        lockState = 0;
    }
    
    // 状態を Blynk に同期
    basic.pause(1000);
    blynk.virtualWrite(2, lockState);
});

// ハートビート（1 時間に 1 回）
basic.forever(function() {
    blynk.virtualWrite(3, input.temperature());
    basic.pause(3600000);
});
```

### Blynk Dashboard 設定

```yaml
Template: Micro:bit Smart Lock
Hardware: Micro:bit v2
Connection: Bluetooth

Datastreams:
  - Key: V1
    Name: Lock Control
    Type: Integer
    Min: 0
    Max: 1
    Default: 0
    
  - Key: V2
    Name: Lock Status
    Type: Integer
    Min: 0
    Max: 1
    
  - Key: V3
    Name: Temperature
    Type: Integer
    Min: -10
    Max: 50

Widgets:
  - Type: Button
    Pin: V1
    Label: Unlock/Lock
    Mode: Switch
    
  - Type: LED
    Pin: V2
    Label: Status
    On Color: "#00ff00"
    Off Color: "#ff0000"
```

---

## 🎨 UX 設計

### 状態同期の仕組み

```
ユーザー体験 (表)              内部機構 (裏)
─────────────────────────    ─────────────────────────
スマホアイコン = 解錠    ←→   V2 ピン = 1
                             Micro:bit LED = 😊
                             完了音 = ピロリン
                             
ドアの前で待つ 0 秒       ←→   ジオフェンス 2 段構え
                             1. 200m でスタンバイ
                             2. 5m で解錠実行
                             
手動で回せる             ←→   磁気クラッチ機構
                             2-3mm 隙間で空回り
```

### フィードバック設計

| イベント | 視覚 | 聴覚 | 触覚 |
|---------|------|------|------|
| 解錠完了 | 😊 LED | 523Hz | - |
| 施錠完了 | 😴 LED | 262Hz | - |
| エラー | ❌ LED | 150Hz×3 | - |
| 低電池 | 🔋 LED | - | Blynk 通知 |

---

## 💰 コスト

### 初期費用

| 内訳 | 金額 |
|------|------|
| 電子部品 | ¥6,250 |
| 3D プリント | ¥1,500 |
| 古いスマホ | ¥5,000 |
| povo SIM | ¥550 |
| **合計** | **¥13,300** |

### ランニングコスト

| 項目 | 金額 | 頻度 |
|------|------|------|
| povo トッピング | ¥330 | 180 日に 1 回 |
| 充電池交換 | ¥1,000 | 2-3 年に 1 回 |
| **月額換算** | **¥2-3** | |

### 市販品との比較

```
SwitchBot Lock     ¥12,800 ─┐
SESAME 5           ¥19,800  ├─ 平均 ¥18,000
Native             ¥29,800 ─┘

Micro:bit Smart Lock  ¥13,300
                     ─────────
                     節約額 ¥4,700+
```

---

## ❓ FAQ

### Q. 雨に濡れても大丈夫？

**A.** 屋内使用を想定しています。屋外設置の場合は防水ケースが必要です。

### Q. 電池はどのくらい持つ？

**A.** 充電池（2000mAh）で約 2-3 ヶ月（1 日 10 回開閉の場合）。

### Q. 家族も使えますか？

**A.** はい。磁気結合なので手動で回せます。Blynk アプリをインストールすれば GPS 自動解錠も可能。

### Q. 物理キーは使えますか？

**A.** はい。外側からは物理キー、内側からはサーボまたは手動で操作可能です。

### Q. 扉を傷つけませんか？

**A.** Command ストリップ使用なので、跡を残さず撤去可能です。

### Q. どのくらいの扉に使えますか？

**A.** 一般的なサムターン式錠（内側のつまみ鍵）に対応。直径 20mm 以内のつまみに最適化されています。

---

## 📁 プロジェクト構成

```
microbit-smartlock/
├── README.md                 # このファイル
├── hardware/
│   ├── PARTS_LIST.md        # 部品リスト
│   └── servo-holder/
│       ├── DESIGN.md        # 設計ドキュメント
│       ├── ASSEMBLY.md      # 組み立て説明
│       ├── microbit-smartlock-servo-holder.scad
│       ├── servo-holder-diagram.svg
│       ├── laser-cut-template.txt
│       └── generate-*.py    # 画像生成スクリプト
├── firmware/
│   ├── main.ts              # Micro:bit コード
│   └── test.ts              # テスト用コード
├── docs/
│   ├── blynk-setup.md       # Blynk 設定ガイド
│   └── troubleshooting.md   # トラブルシューティング
└── assets/
    ├── wiring-diagram.png   # 配線図
    └── demo-video.mp4       # デモ動画
```

---

## 🤝 コントリビューション

このプロジェクトはオープンソースです。改善点やバグ報告を歓迎します。

- 🐛 バグ報告: Issues で報告
- 💡 機能提案: Discussions で議論
- 🔧 プルリク: `dev` ブランチへ送信

---

## 📜 ライセンス

- ハードウェア設計: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- ソフトウェア: [MIT License](https://opensource.org/licenses/MIT)

---

## 🔗 リンク

- [Micro:bit 公式サイト](https://microbit.org/)
- [Blynk IoT](https://blynk.io/)
- [povo 2.0](https://povo.jp/)
- [MakeCode エディタ](https://makecode.microbit.org/)
- [OpenSCAD](https://www.openscad.org/)

---

<div align="center">

**🏠 Made with ❤️ for DIY Smart Home Enthusiasts**

[🔝 ページトップへ](#-microbit-smart-lock)

</div>
