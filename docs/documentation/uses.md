## Script Overview
This script provides functionalities for managing email lists. It offers two main actions:

- **Fetching**: Retrieves emails from a designated Gmail inbox and stores them in a specified database.
- **Filtering**: Applies predefined rules to filter emails from the database and executes corresponding actions based on the rule definitions.

## Prerequisites:
- Python 3.x installed on your system. You can check your version by running python --version in your terminal.
- Mysql 5.x or higher.
- **Powershell with windows os.**
- A Gmail account with necessary permissions.
- **Google Cloud Platform project with Gmail API enabled and OAuth 2.0 credentials created.**
- A virtual environment is highly recommended to isolate project dependencies. Refer to the Installation document ["Installation"] for setting up a virtual environment.

## Usage
The script utilizes command-line arguments to specify the desired action.

### Running the Script:

1. Open your powershell.
2. Navigate to the directory where the script is located.
3. Activate the virtual environment and set the environment variables mention in ["Installation"]
4. Run the script using the following command format:
```shell
python src/script/email_script.py --action [action] --name [name]
```
##### Replace the placeholders with the following:
- `[action]`: Either `fetch` or `filter`.
- `[name]`: Name of the rule need to execute. This variable only required in case of `filter` action.

Here's a simple example demonstrating how to use the core functionality of the project:

#### Available Actions:

1. **Fetching**:
```shell
python src/script/email_script.py --action fetch
```
This retrieves emails from the authorized Gmail inbox and stores them in the specified database.

2. **Filtering**:
```shell
python src/script/email_script.py --action filter --name inbox_move
```
This applies rules defined in the rules.json file to filter emails from the database and executes associated actions.

## Google Gmail API Credentials
To access the user's Gmail account, the script requires the following Google Cloud Platform credentials:

- **Client ID**
- **Client Secret**

These credentials are typically stored in a secure configuration file or environment variables. Refer to the Google Cloud Platform documentation for detailed instructions on creating and managing OAuth 2.0 credentials.

## Additional Notes
- The script requires configuration settings (e.g., Gmail credentials, database path, rule definitions) to function correctly.
- Source `docs/db/communication/schema/communication.sql` into mysql to create `database` and it's `tables`.
- Ensure database connection details is updated in `config/config_dev.yaml`. 
- Ensure the rules.json file path updated in `config/config_dev.yaml`.
- Ensure the `google creditintal` file path updated in `config/config_dev.yaml`.
- Ensure the `access token` file path updated in `config/config_dev.yaml`.
- For troubleshooting or customization, refer to the script's source code and comments.
- Adhere to Google's API usage policies and best practices.
- By effectively utilizing this script and following the necessary steps for Google Gmail API authentication, you can efficiently manage your email data and automate specific tasks based on predefined rules.

Note: This document provides a general overview. Specific implementation details and functionalities may vary based on the script's code.


["Installation"]: ./docs/documentation/installation.md