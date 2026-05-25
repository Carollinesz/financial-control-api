# CLAUDE.md - financial-api

## Project Overview

This is a microservice to control personal finances, it won't have a frontend, just a API Restful. The core functions is to register transactions, track credit recurrent expenses.  

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

│   └── .env.example
│   └── .gitignore
│   └── alembic.ini
│   └── Claude.md
│   └── README.md
│   ├── .claude/ 
│   │   └── settings.local.json
│   ├── alembic/                             **Migrations**
│   │   └── env.py
│   │   └── script.py.mako
│   │   ├── versions/
│   │   │   └── .gitkeep
│   │   │   └── 4998a5e45af5_initial.py
│   ├── app/                                 **Main application**
│   │   └── main.py                          **Fast API init**
│   │   ├── api/                             **API Routes**
│   │   │   ├── v1/
│   │   │   │   └── router.py
│   │   │   │   ├── routes/
│   │   ├── core/                            **Core deps**
│   │   │   └── config.py
│   │   │   └── database.py
│   │   ├── models/                          **Database Models**
│   │   │   └── models.py
│   │   ├── repositories/
│   │   ├── schemas/                         **Swagger & Pydentic documentation**
│   │   │   └── schemas.py
│   │   ├── services/
│   ├── tests/                               **pytest**
│   │   └── conftest.py