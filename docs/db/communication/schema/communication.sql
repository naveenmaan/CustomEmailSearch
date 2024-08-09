CREATE DATABASE IF NOT EXISTS `communication`;

USE communication;

DROP TABLE IF EXISTS email;

CREATE TABLE email (
  email_id INT AUTO_INCREMENT PRIMARY KEY,
  message_id VARCHAR(255) UNIQUE,
  thread_id VARCHAR(255),
  subject TEXT,
  from_address VARCHAR(255),
  to_addresses TEXT,
  cc_addresses TEXT,
  bcc_addresses TEXT,
  reply_address TEXT,
  received_date DATETIME,
  labels TEXT,
  body LONGTEXT,
  created_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
  created_by VARCHAR(50),
  modified_datetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  modified_by VARCHAR(50)
);

DROP TABLE IF EXISTS action_history;

CREATE TABLE action_history (
  action_history_id INT AUTO_INCREMENT PRIMARY KEY,
  email_id INT,
  action_type enum('MOVE','READ','UNREAD'),
  additional_details JSON,
  is_valid INT DEFAULT 1,
  status enum('NEW','SUCCESS','FAILURE') DEFAULT 'NEW',
  failure_reason varchar(500),

  created_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
  created_by VARCHAR(50),
  modified_datetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  modified_by VARCHAR(50),
  FOREIGN KEY (email_id) REFERENCES email(email_id)
);