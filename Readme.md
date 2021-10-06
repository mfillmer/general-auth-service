# Auth-Service

## Features

API-Users can:
- register a new account
- verify their mail with token
- log into existing accounts
- refresh their token
- logout, invalidate token
- delete their account
- update their password

CLI-Users can:
- view a report of registered users (json/csv)
- create permissions
- list permissions
- delete permissions
- create roles
- list roles
- delete roles
- set a default role for new users
- group permissions into roles
- set roles on user

tests only cover user-facing functions like api and cli