# Auth-Service

## Features

API-Users can:
- register a new account
- verify their mail with token
- log into existing accounts
- logout, invalidate token
- refresh their token
- delete their account
- update their password

CLI-Users can:
- view a report of registered users
- create permissions
- delete permissions
- create roles
- set a default role for new users
- delete roles
- group permissions into roles
- set roles on other accounts

The Service is protected against CRSF and XSS Attacks by duplicated token authorization