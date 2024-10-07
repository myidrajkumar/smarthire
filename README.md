# SmartHire

## Intelligent Recruitment Solutions

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![GenAI](https://img.shields.io/badge/GenAI-enabled-green.svg)](https://github.com/myidrajkumar/smarthire)

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Technical Requirements](#technical-requirements)
6. [Configuration](#configuration)
7. [Contributing](#contributing)
8. [License](#license)
9. [FAQ](#faq)

## Overview

SmartHire is an innovative GenAI-powered recruitment platform designed to streamline and optimize the hiring process. This project leverages AI-driven technologies to provide efficient talent acquisition solutions, reducing time-to-hire and improving candidate quality.

## Features

### Recruitment Automation

* **Job Description (JD) Creation**: Generate tailored JDs with specific experience and skill requirements.
* **JD Updates**: Easily modify generated JDs to suit evolving HR needs.
* **Candidate Sourcing**: Automate candidate profile sourcing from leading job sites.
* **Candidate Screening**: Evaluate candidates with scored assessments and rankings.

### Interview Process Optimization

* **Preliminary Interview Questions Generation**: Create relevant interview questions based on JD requirements.
* **Automated Candidate Invites**: Send personalized interview invitations with question links.
* **Candidate Answer Evaluation**: Assess candidate responses with AI-driven insights.

### Data-Driven Insights

* **Recruitment Dashboard**: Monitor key statistics and metrics on recruitment performance.
* **Real-time Analytics**: Gain actionable insights to refine recruitment strategies.

### Additional Features

* **User Management**: Manage user roles and permissions.
* **Candidate Profile Management**: Store and manage candidate profiles.
* **Communication Templates**: Use customizable email and message templates.

## Installation

To install and run SmartHire, follow these steps:

### Prerequisites

* Python 3.12+
* GenAI library (refer to `requirements.txt`)
* Database (PostgreSQL)

### Steps

1. Clone the repository: `git clone https://github.com/myidrajkumar/smarthire`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables (refer to `.env.example`)
4. Run database migrations (if applicable)
5. Run the application: `python app.py`

## Usage

1. Access the web interface at `http://localhost:5000`
2. Explore features and functionalities

## Technical Requirements

* Python 3.12+
* GenAI library
* Database (PostgreSQL)
* Web framework (FastAPI)

## Configuration

### Environment Variables

* `SMART_HIRE_DB_URL`: Database URL
* `SMART_HIRE_GENAI_API_KEY`: GenAI API key
* `SMART_HIRE_EMAIL_USERNAME`: Email username
* `SMART_HIRE_EMAIL_PASSWORD`: Email password

### Database Setup

* Create a database and configure database settings in `.env`
* Run database migrations (if applicable)

## Contributing

Contributions are welcome! Submit issues, feature requests, or pull requests.

### Code Style

* Follow PEP 8 guidelines
* Use consistent naming conventions

### Commit Messages

* Follow the Conventional Commits specification

## License

This project is licensed under the MIT License.

## FAQ

### What is GenAI?

GenAI is a cutting-edge AI technology used for natural language processing and generation.

### How do I configure the database?

Refer to the `.env.example` file and configure database settings accordingly.

### Can I customize the email templates?

Yes, email templates can be customized in the `communication_templates` directory.
