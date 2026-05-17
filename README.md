# EQ Muster

[P2P地震情報](https://www.p2pquake.net/) の WebSocket API をリアルタイムで受信し、指定震度以上の地震を Discord に通知するサービスです。

## 動作概要

```
P2P地震情報 WebSocket → eq-muster → Discord Webhook
```

接続が切れた場合は自動再接続します。

## 環境変数

| 変数名 | 必須 | 説明 |
|--------|------|------|
| `DISCORD_WEBHOOK_URL` | ✅ | 通知先の Discord Webhook URL |
| `MIN_INTENSITY` | - | 通知する最小震度（デフォルト: `3`） |
| `SANDBOX` | - | サンドボックス API を使う場合 `true`（デフォルト: `false`） |

`.env.example` をコピーして設定してください。

```bash
cp .env.example .env
```

## Docker で動かす（本番推奨）

```bash
# .env を用意してから
docker compose up -d
```

Docker Hub イメージ: `heki0323/eq-muster:latest`

## ローカル開発

```bash
# 依存関係のインストール（uv が必要）
uv sync

# 実行
uv run eq-muster
```

## 震度フィルタ

`MIN_INTENSITY` には震度の整数値を指定します。

| 値 | 震度 |
|----|------|
| 1 | 震度1 |
| 2 | 震度2 |
| 3 | 震度3 |
| 4 | 震度4 |
| 5 | 震度5弱 / 5強 |
| 6 | 震度6弱 / 6強 |
| 7 | 震度7 |

## ライセンス

MIT
