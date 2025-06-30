
# 💸 Telegram Wallet Alert Bot (ETH, TRC20, BTC)

This bot monitors incoming transactions for ETH, TRC20 (on Tron), and BTC addresses, and sends alerts to your Telegram group or private chat.

---

## 🚀 Features

- ✅ Detects **incoming transactions** only
- ✅ Supports multiple addresses per coin
- ✅ Displays USD estimated value from Binance API
- ✅ Sends notification via **Telegram Bot**
- ✅ Designed for **Railway deployment** or standalone use

---

## 📁 Included Files

- `final_bot_entry_alert.py` – Main bot script
- `requirements.txt` – Dependencies (`requests`)
- `Procfile` – For Railway deployment

---

## 🧪 Environment Variables Required

| Variable            | Description                            |
|---------------------|----------------------------------------|
| `BOT_TOKEN`         | Telegram bot token from BotFather      |
| `CHAT_ID`           | Group ID or your Telegram user ID      |
| `ETH_ADDRESS`       | ETH addresses, comma-separated         |
| `TRON_ADDRESS`      | TRC20 addresses (TRON), comma-separated|
| `BTC_ADDRESS`       | BTC addresses, comma-separated         |
| `ETHERSCAN_API_KEY` | Your Etherscan.io API key              |

---

## 🛠️ Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run bot locally:
   ```bash
   python final_bot_entry_alert.py
   ```

3. Or deploy to [Railway](https://railway.app):
   - Upload this repo
   - Add environment variables
   - Railway will auto-detect `Procfile` and start the bot

---

## 📬 Example Notification

```
🟢 *ETH 入金*
从: `0xFromAddress`
到: `0xYourAddress`
💰 0.123456 ETH ≈ $398.76
```

---

## ⚠ Notes

- Only monitors latest incoming transaction
- Designed for simplicity and easy deployment

---

Created with ❤️ for automated crypto alerts.
