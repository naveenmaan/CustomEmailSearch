## Flowchart Documentation for the project

**Purpose**: This script automates email fetching and filtering based on predefined rules.

### Components:

- **email_script.py**: Main script handling user input and delegating actions.
- **mail_process_manager.py**: Core class for email processing and interaction with databases and email services.
- **communication_dao.py**: Core class to interact with database.
- Supporting libraries for database access, email access, custom exceptions, configurations, and utilities.

### Data Flow:

1. **User Input**: Script accepts arguments (--action and optional --name) through argparse.
2. **Action Selection**: Based on --action argument:
   - **fetch**:
     - Fetch emails from mailbox using `GMailManager.get_unread_email()`.
     - Store emails in database using `MailProcessManager.store_email_details()`.
   - **filter**:
     - Validate `--name` argument is provided (`script_parser.error`).
     - Retrieve rule details by name using `RuleEngineManager.get_rule_by_name()`.
     - Extract filter criteria from the rule.
       - Filter emails based on criteria using `MailProcessManager.get_filtered_email_list_by_rule_detail()`.
     - Perform actions on filtered emails using `MailProcessManager.messages_action_perforation()`.

### Error Handling:
- Exceptions are caught and logged throughout the process.
- Specific actions are taken depending on the exception type:
  - `ValidationException`: Script exits with an error message.
  - Database exceptions (`DBConnectionError`, `DBQueryError`, `DBException`): Database connection is rolled back and script continues with remaining emails.
  - Other exceptions: Failure status and reason are updated in the action history table and script continues.


### Process Descriptions:

1. **Start**: Script execution begins. 
2. **Parse Arguments:** Script arguments are parsed using `argparse`. 
3. **Select Action:**
   - Decision: Check if `--action` is provided.
   - If yes, proceed to action selection based on its value.
   - If no, display error message and exit.
4. **Fetch Emails:** (if action is 'fetch')
   - Fetch unread emails from mailbox.
   - Store email details in the database.
   - Handle potential exceptions.
5. **Validate Filter Name:** (if action is 'filter')
   - Decision: Check if `--name` is provided.
   - If no, display error message and exit.
   - If yes, proceed with rule retrieval.
6. **Get Rule Details:**
   - Retrieve rule details by name from the rules list.
   - Handle potential exceptions.
7. **Extract Filter Criteria:**
   - Extract filter criteria (conditions) from the retrieved rule object.
8. **Filter Emails:**
   - Filter emails based on the extracted criteria using database queries.
9. **Perform Actions:**
   - Loop through filtered emails.
   - For each email:
     - Determine updated labels based on the rule's actions.
     - Update email labels in the email service (e.g., move to a specific folder).
     - Update email details in the database (e.g., mark as read).
     - Handle potential exceptions during action execution.
10. **End**: Script execution finishes.