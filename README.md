# Telegram-Channel-Backup

## ⚠️This is not a bot. Script Work as a normal Telegram User. 
## Features ✅
- Can forward files from a source channel to a backup channel.**The script will not work with channels that have restricted content enabled.**<br>
- Can enable batch mode to prevent account bans for forwarding thousands of files at once.
- You can set the batch size and batch interval. To use this feature, set `BATCH_MODE = "TRUE"` in `config.env.`

More details on `config.env` section.

### 👉 Recommendations
- It is recommended to use batch mode if you are forwarding over 1000 files to another channel.
- Set `BATCH_INTERVAL` to 100 or more for larger forwardings.
- The default `BATCH_SIZE` is `1000`. You can adjust this as needed.

## ⚠️I do not take any responsibilities if your account gets banned.⚠️

## Installation

### Prerequisites
1. [Python 3.11](https://www.python.org/downloads/release/python-3110/) should be intalled in your system and make sure to add it to `PATH`.

#### Running the script.

- Clone this repository:
```
git clone https://github.com/pachax001/Telegram-Channel-Backup && cd Telegram-Channel-Backup
```


- Fill the variables in [config.env](https://github.com/pachax001/Telegram-Channel-Backup/blob/main/config.env)
<br> [Click here](https://github.com/pachax001/Telegram-Channel-Backup/blob/main/README.md#configs) for more info on config. </br>

- After filling the `config.env` open a terminal in the cloned folder and type the following command:


```
pip install -r requirements.txt
```
- Finally, run the script with:
```
python main.py
```

------

## Configs
### config.env file

- `APP_ID`        - From my.telegram.org (or @UseTGXBot)

- `API_HASH`      - From my.telegram.org (or @UseTGXBot)

- `SOURCE_CHANNEL` - The ID of the Channel where the original files are in.
    - **You must be a member of this channel, and the channel must allow file forwarding.**
- `DESTINATION_CHANNEL` - The ID of the backup channel
    - **You must be an admin of the backup channel with the ability to send messages to channel.**
- `WAIT_TIME` - This variable defines the rest time (in seconds) between each message forwarding action. It helps avoid overwhelming the server with too many requests in a short period, preventing potential rate limits or bans from the platform. Adjusting this value controls the delay between sending consecutive messages, allowing the bot to forward messages at a controlled pace.
    - `WAIT_TIME = 5`: The bot will wait 5 seconds between forwarding each message.
- `BATCH_MODE` - This variable controls whether the bot forwards messages in batches or continuously.
    - If `BATCH_MODE` is set to `"TRUE"` (the default value), the bot will forward messages in chunks of a specified size (controlled by the `BATCH_SIZE` variable) and then pause for a certain interval (controlled by the `BATCH_INTERVAL` variable) before resuming.
    - If `BATCH_MODE` is set to `"FALSE"`, the bot will forward messages continuously without pausing between batches.
- `BATCH_SIZE` - This variable defines the number of messages the bot forwards in each batch when `BATCH_MODE` is set to `"TRUE"`. The bot will forward up to this many messages before pausing. The default value is `1000`, meaning the bot will forward 1000 messages in one go before taking a break (based on `BATCH_INTERVAL`).
    - `BATCH_SIZE = 1000` : The bot will forward 1000 messages in a batch, then rest before forwarding the next batch.
- `BATCH_INTERVAL` - This variable defines the rest time (in seconds) between batches when `BATCH_MODE` is set to `"TRUE"`. After forwarding the number of messages defined by `BATCH_SIZE`, the bot will pause for this many seconds before resuming the next batch. The `default value is 10`, meaning the bot will rest for 10 seconds between each batch of messages.
    - `BATCH_INTERVAL = 10` : After forwarding one batch of messages, the bot will wait 10 seconds before starting the next batch.


## 🏅 **Credits**
|<img width="70" src="https://avatars.githubusercontent.com/u/88532565">|

|[`Pyrofork`](https://github.com/Mayuri-Chan/pyrofork)|

