# CodeForge – Online Interview Practice Platform

CodeForge is a full-stack online coding and interview practice platform built with **Flask and PostgreSQL**. It allows users to solve programming problems, submit solutions, receive automated verdicts, and track their submission history.

The platform also includes an **administrator dashboard** for managing users, coding problems, and test cases.

## Features

### 👨‍💻 User Features

- User registration and secure authentication
- Browse and practice coding problems
- Submit solutions in Python
- Automated test-case evaluation
- Accepted / Wrong Answer / Runtime Error verdicts
- Execution time tracking
- Submission history
- Individual submission details
- Progress tracking through previous attempts

### 🛠️ Admin Features

- Dedicated administrator dashboard
- View and manage registered users
- Grant or revoke administrator privileges
- Delete users
- Create coding problems
- Edit existing problems
- Delete problems
- Create and manage test cases
- Support for hidden test cases

### ⚙️ Backend & Database

- Modular Flask application architecture
- SQLAlchemy ORM for database interaction
- PostgreSQL relational database
- Flask-Migrate / Alembic database migrations
- Session-based authentication using Flask-Login
- WTForms for form validation
- Environment-based configuration using `.env`

### 🧪 Code Execution

CodeForge includes an automated submission pipeline that:

1. Receives the user's submitted code.
2. Executes it against predefined test cases.
3. Captures execution results and errors.
4. Determines the submission verdict.
5. Records the result and execution time.
6. Displays detailed feedback to the user.

## Screenshots

### Problem Dashboard
Browse available coding problems by difficulty and topic.

![CodeForge Problems](screenshots/Problems.png)

### Problem Details
View problem descriptions, constraints, examples, and test cases.

![Problem Details](screenshots/Problemdescription.png)



### Code Submission
Write and submit Python solutions directly through the platform.

![Code Submission](screenshots/Solution.png)

### Submission Result
Receive automated verdicts with test case results and execution time.

![Submission Result](screenshots/Result.png)

### Submission History
Track previous attempts, verdicts, test results, and execution times.

![Submission History](screenshots/Submissions.png)

### Admin Dashboard
Monitor platform statistics and manage users, problems, and submissions.

![Admin Dashboard](screenshots/Adminpage.png)

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM |
| Flask-Migrate / Alembic | Database migrations |
| Flask-Login | Authentication |
| Flask-WTF | Form handling and validation |
| HTML / CSS | Frontend |
| Jinja2 | Server-side templating |
| Git / GitHub | Version control |

## Project Structure

```text
CodeForge/
│
├── app.py
├── config.py
├── extensions.py
├── models.py
├── forms.py
├── routes.py
├── admin_routes.py
├── executor.py
├── runner.py
├── seed.py
├── seed_tests.py
├── requirements.txt
│
├── migrations/
│
├── static/
│   └── css/
│
├── templates/
│
├── .env.example
├── .gitignore
└── README.md
```
## Architecture

CodeForge follows a modular Flask architecture:

User
 ↓
Flask Web Application
 ↓
Routes / Authentication
 ↓
SQLAlchemy ORM
 ↓
PostgreSQL

For code submissions:

User submits code
 ↓
Flask submission route
 ↓
Execution sandbox
 ↓
Test case execution
 ↓
Output comparison
 ↓
Submission verdict
 ↓
Submission history

## Database Design

The application uses PostgreSQL to manage the core entities of the platform, including:

- Users
- Problems
- Test Cases
- Submissions

Relationships between these entities allow CodeForge to maintain user submission history, problem metadata, test cases, and evaluation results.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Abhishekh712/CodeForge.git
cd CodeForge
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/codeforge
```

> Never commit your `.env` file or database credentials to GitHub.

### 5. Set up the database

Make sure PostgreSQL is running and the configured database exists.

Then apply the migrations:

```bash
flask db upgrade
```

### 6. Run the application

```bash
python app.py
```

The application will be available locally at:

```text
http://127.0.0.1:5000
```

## Future Improvements

Possible future extensions include:

- Support for additional programming languages
- Improved code execution sandboxing
- More advanced problem filtering
- Leaderboards
- User statistics and analytics
- Difficulty-based recommendations
- Docker-based deployment
- Cloud deployment
- Automated CI/CD testing

## Author

**Abhishekh Priyan Balamurugan**

B.Tech – Computer and Communication Engineering  
Manipal Institute of Technology, Manipal

---

⭐ If you find the project interesting, feel free to explore the repository.
