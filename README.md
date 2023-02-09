# The Lott Crawler

A python script to scrape the winning numbers from The Lott website ([www.thelott.com](http://www.thelott.com/)) and analyze the results to select the most likely winning numbers. The selected numbers will then be sent to WeChat. 

Currently, the project is still under development and the following features have been completed: data collection and sending to WeChat. The next feature under development is the analysis and generation of numbers.

## Requirements

- Python 3.x
- Requests library
- PyMySQL library
- WeChat API (optional)

## How to Use

1. Clone or download the repository
2. Install the required libraries by running the following command:

```bash
pip install -r requirements.txt
```

1. Edit your_settings, fill in your database information, and then change the file name to local_settings.py

2. Run the script with the following command:

   ```bash
   python main.py
   ```

   

1. The analyzed results will be sent to your WeChat account (if the WeChat API is configured).

## Note

This script is for educational and research purposes only. Use of the information is at your own risk. The author of this script is not responsible for any misuse of the information.
