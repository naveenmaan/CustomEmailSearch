# Custom Email Search

## What is ((Custom Email Search))?

The EmailRuleEngine is a Python script that fetches emails from a Gmail account using OAuth authentication, stores them
in a local database, and processes them based on predefined rules. It provides a flexible rule-based system where rules,
including conditions and actions, can be defined in a JSON file. This allows for customization of email handling logic
without modifying the core script.

#### Key Components

- **Email Fetching**: Uses the Google Auth Library and Gmail API to retrieve emails from the specified Gmail account.
- **Database Storage**: Stores fetched emails in a relational database (Postgres, MySQL, or SQLite3) for efficient
  querying and processing.
- **Rule Engine**: Processes emails based on rules defined in a JSON file. Each rule consists of conditions and
  corresponding actions.
- **Action Execution**: Executes specified actions on emails that match the rule con`ditions using REST APIs or other
  methods.

---
## Quick Start
Read ["Installation"] and then ["Usage"] for the project.

["Installation"]: ./docs/documentation/installation.md
["Usage"]: ./docs/documentation/uses.md

## Development Docs
- [Rule] file and its attributes definition
- [Database] design document
- [Flow Chart] for the flow of the script

[Rule]: ./docs/documentation/rule/rule.md
[Database]: ./docs/documentation/database.md
[Flow Chart]: ./docs/documentation/flow_chart.md