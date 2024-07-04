# MissedConfirmationAlarm

MissedConfirmationAlarm is a Tkinter-based GUI application that monitors CrossFi blocks and sends notifications to Telegram in case of a failed block.

## Features
- Monitors CrossFi blocks for success and failure.
- Plays an error sound on a failed block.
- Sends a notification to a specified Telegram chat on a failed block.

## Requirements
- Python 3.x
- The required Python libraries can be found in the `requirements.txt` file.

## Installation
1. Clone this repository:
    ```sh
    git clone https://github.com/YOUR_USERNAME/MissedConfirmationAlarm.git
    cd MissedConfirmationAlarm
    ```
2. Install the required Python libraries:
    ```sh
    pip install -r requirements.txt
    ```
3. Run the application:
    ```sh
    python main.py
    ```

## Usage
1. Enter the CrossFi address you want to monitor.
2. Enter your Telegram chat ID.
3. Click "Submit" to start monitoring.
4. To find your chat ID, start a conversation with [@userinfobot](https://t.me/userinfobot) on Telegram and send `/start`. The bot will reply with your chat ID.

## License
This project is licensed under the MIT License.
