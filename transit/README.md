# Transit Knowledge

`norikae` の乗り換え知識レイヤー。

ここでは **交通そのもの** と **乗り換えのベストプラクティス** を蓄積する。

## Separation

- `transit/` — 駅・路線・乗換・徒歩・待ち時間・ベストプラクティス
- `iot/` — IoT / センサー / デバイス実験。交通データとは独立
- `tokyo-norikae` — 乗換データを表示・利用するUI
- `odekake-mcp` — 乗換データと体験データを組み合わせる上位レイヤー

乗換データは「どこからどこへ行くか」を扱い、IoT は「現実世界から何を計測・操作するか」を扱う。

## Best Practice

乗り換えは最短時間だけで評価しない。

```text
route
  -> transfer
  -> walk
  -> wait
  -> platform
  -> reliability
  -> accessibility
  -> comfort
```

同じ駅間でも、乗換距離、ホーム移動、混雑、迷いやすさ、余裕時間などで「良いルート」は変わる。

## Data

`best-practices.yaml` に、再利用可能な判断知識を蓄積する。

各レコードは以下を基本とする。

- `id`
- `category`
- `rule`
- `when`
- `prefer`
- `avoid`
- `confidence`
- `source`
- `updated`

実測・公式情報・利用者の経験を混ぜず、`source` と `confidence` を残す。
