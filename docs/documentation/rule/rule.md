This rule defines a set of conditions for filtering emails in your inbox and applying specific actions to them.

### Rule Name:
### Category:
- **all** (This rule checks all the condition is true)
- **any** (This rule verify any one of the condition is true)
### Conditions:
These conditions are used to define rules for filtering data based on specific criteria.

### Text-based Conditions
- **Contains**: Checks if a text string includes a specific substring.
  - **Example**: "Hello world" contains "world".
- **Does** not contain: Checks if a text string does not include a specific substring.
  - **Example**: "Hello world" does not contain "goodbye".
- **Equal**: Checks if two text strings are exactly the same.
  - **Example**: "hello" equals "hello".
- **Does** not equal: Checks if two text strings are different.
  - **Example**: "hello" does not equal "world".

### Datetime Conditions
- **Less than**: Checks if a number is smaller than another number.
- **Greater than**: Checks if a number is larger than another number.

### Actions:
- **Move**: Move any email from one folder to another.
- **Read**: Mark the email as read.
- **Unread**: Mark the email as unread.

# Sample Rule
Refer ["Sample Rule"] file for an example.

["Sample Rule"]: ../../../config/rule.json