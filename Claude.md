# CLAUDE.md - financial-api

## Project Overview

This is a microservice to control personal finances, it won't have a frontend, just a API Restful.

## Core Functions

- **Control transactions (building)**: It capable to upload the transactions made by the user 
- **Control month expanses (building)**: It capable to register and fixed espanses that must be payed every month
- **Control actually money avaliable in account**: Register how much the user expend in which of their accounts.
- **Register any accounts**: It capable to separe the money from diverses sources  

## Tech Stack

- **Database:** PostgreeSQL 4
- **Backend:** Python 3.13.9, SQLalchemy, swagger, alembic, fastapi

## Code Quality

- **Early Returns**: Use to avoid nested conditions
- **Descriptive Names**: Use clear variable/function names (prefix handlers with "handle")
- **DRY Code**: Don't repeat yourself
- **Functional Style**: Prefer functional, immutable approaches when not verbose
- **Minimal Changes**: Only modify code related to the task at hand
- **Function Ordering**: Define composing functions before their components
- **Simplicity**: Prioritize simplicity and readability over clever solutions
- **Build Iteratively** Start with minimal functionality and verify it works before adding complexity
- **Run Tests**: Test your code frequently with realistic inputs and validate outputs
- **Build Test Environments**: Create testing environments for components that are difficult to validate directly
- **Functional Code**: Use functional and stateless approaches where they improve clarity
- **Clean logic**: Keep core logic clean and push implementation details to the edges
- **File Organsiation**: Balance file organization with simplicity - use an appropriate number of files for the project scale

## project structure

│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── alembic.ini **ignore**
│   ├── Claude.md
│   ├── Extrato Conta Corrente-2026.ofx **ignore**
│   ├── listar.py **ignore**
│   ├── README.md **ignore**
│   └── teste.py **ignore**
│   ├── .claude/
│   │   └── settings.local.json
│   ├── alembic/ **ignore**
│   │   ├── env.py**ignore** 
│   │   └── script.py.mako **ignore**
│   │   ├── versions/ **ignore**
│   │   │   ├── .gitkeep
│   │   │   ├── 0b36188ae3c6_new_table.py
│   │   │   ├── 4998a5e45af5_initial.py
│   │   │   ├── acfb8b4d6b45_relationship_accounts_and_banks.py
│   │   │   ├── c2a2cfad97df_relationship_accounts_and_banks.py
│   │   │   ├── c6132f0deb70_creating_constraints_in_accounts.py
│   │   │   ├── dabfe2d642df_rename_columns_in_bank_account.py
│   │   │   └── ea7e2ca54b1c_big_changes_kekw.py
│   ├── app/ **Main application**
│   │   └── main.py **Fast API init**
│   │   ├── api/ **API Routes**
│   │   │   ├── v1/
│   │   │   │   └── router.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── banks.py **avaliable bank options to register in transactions and bank_accounts**
│   │   │   │   │   ├── bank_accounts.py **users' bank_accounts**
│   │   │   │   │   └── transactions.py **users' transactions**
│   │   ├── constants/ **empty**
│   │   ├── core/ **Core config and database**
│   │   │   ├── config.py **ignore**
│   │   │   └── database.py **database connection**
│   │   ├── models/ **Postgreesql Models**
│   │   │   └── models.py **banks, transactions and bank_accounts models**
│   │   ├── repositories/
│   │   │   ├── banks.py
│   │   │   ├── bank_accounts.py
│   │   │   └── transactions.py
│   │   ├── schemas/ **Swagger & Pydentic documentation**
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── banks.py
│   │   │   ├── bank_accounts.py
│   │   │   └── transactions.py
│   ├── tests/ **pytest**
│   │   └── conftest.py