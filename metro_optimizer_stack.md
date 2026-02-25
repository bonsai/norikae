# 🚀 Project: Metro-Optimizer Agent (Colab Native)

Google Colab上で動作し、Gmailから移動指示を抽出、メトロ路線の「エクストリーム乗り換え」を最適化してカレンダーとBigQueryに同期するエージェント。

## 🏗️ System Stack

| Layer | Technology | Role |
|-------|------------|------|
| Runtime | Google Colab | 実行環境。Pythonで制御し、Gemini APIを叩くメインハブ。 |
| Intelligence | Gemini 1.5 Pro/Flash | メールの構造化解析、最適なルートの推論、ユーザーとの対話。 |
| Data Source | Gmail API | 移動指示書（HTML/Text）の取得。 |
| Calendar | Google Calendar API | 確定した行程の自動登録と重複チェック。 |
| Optimization | Custom Logic + Maps API | メトロ優先ルートの計算。徒歩20分許容の徒歩・地下鉄ミックス。 |
| Storage | BigQuery (BQ) | 過去のルート、乗り換え成功率、車両位置データを蓄積し、次回の最適化へ。 |

## 🛠️ Data Flow & Architecture

### Phase 1: メール解析と構造化 (Gmail to JSON)
Geminiを使用して、画像やテキストメールから「地点・時間・路線」を抜き出します。

- Input: 2/27(金) 12:40 和光市駅 -> 有楽町線 -> 永田町
- Output: `{ "date": "2026-02-27", "steps": [...] }`

### Phase 2: メトロ最適化 (Metro Logic)
- メトロ優先: JRや私鉄を避け、極力メトロ（および直通）で完結させる。
- 徒歩20分ルール: 駅から目的地まで、または駅間の「歩いたほうが早い」ルートを許容。
- エクストリーム乗り換え: BQに「〇号車に乗れば階段が近い」というメタデータを蓄積し、次回からそれを反映。

### Phase 3: 対話型フィードバック (Human-in-the-loop)
「28日のこのルート、徒歩15分ありますが大丈夫ですか？」といった相談をメール返信形式、またはColab上のインタラクションで実行。

## 📂 BigQuery Schema (蓄積用)

BQに以下のテーブルを作成し、移動するたびに「賢くなる」仕組みを作ります。

```sql
CREATE TABLE `your_project.travel_logs.route_optimization` (
  event_date DATE,
  departure_station STRING,
  arrival_station STRING,
  metro_line STRING,
  walking_duration_minutes INT64,
  best_car_number INT64, -- 最適な乗車車両位置
  feedback STRING -- 「この乗り換えはきつかった」等のメモ
);
```

## 💻 Colab実装のコード骨子 (Python)

```python
import google.generativeai as genai
from google.colab import auth
from google.cloud import bigquery

# 認証設定 (BQ, Calendar, Gmail)
auth.authenticate_user()

def process_travel_plan(target_date):
    # 1. Gmailから対象日のメールを取得
    raw_mail = fetch_gmail_by_date(target_date)
    
    # 2. Geminiで構造化
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"以下のメールから移動行程をJSONで抽出して。メトロ優先で最適化案も出して。: {raw_mail}"
    structured_plan = model.generate_content(prompt)
    
    # 3. カレンダー確認 & 登録
    if not is_already_registered(structured_plan):
        register_to_calendar(structured_plan)
        
    # 4. BQへ記録
    save_to_bq(structured_plan)
    
    return "28日の行程をカレンダーに登録し、BQへ蓄積しました。"
```

## 📅 次のステップ：28日の行程

28日の移動について、まずは**「どのメール（またはどの場所）」**をターゲットにするか確定させましょう。

- メールの特定: 私がGmailから「28日」に該当する可能性のあるメール（あるいは27日の指示書の続き）を再度スキャンします。
- プロトタイプ作成: 1つの移動ルートを実際にBQへ書き込み、カレンダーに反映させる「最小構成のColabノートブック」を一緒に書き始めましょう。

**「28日はこの場所に行く予定なんだ」**という情報をいただければ、即座にこのStackを回し始めます！