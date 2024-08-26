# FastAPI News Application

This FastAPI application allows users to browse news articles, comment on them, and sign up for an account. It also supports anonymous browsing, where users can view news content without registering or logging in.

## Table of Contents
- [Features](#features)
- [Application Structure](#application-structure)
- [How Surfing Anonymously is Served](#1-how-surfing-anonymously-is-served)
- [Handling Anonymous Sessions](#2-handling-anonymous-sessions)
- [Anonymous Surfing Flow](#3-anonymous-surfing-flow)
- [Logout for Anonymous Users](#4-logout-for-anonymous-users)
- [Getting Started](#getting-started)
  - [Clone the Repository](#1-clone-the-repository)
  - [Access the application inside the devcontainer via VScode](#2-access-the-application-inside-the-devcontainer-via-vscode)
  - [Install Dependencies](#3-install-dependencies)
  - [Setup database](#4-setup-database)
  - [Accessing the Application](#5-accessing-the-application)
- [License](#license)

## Features

- **Anonymous Browsing:** Users can view news articles without creating an account.
- **User Registration:** Users can sign up to create an account and be able to comment on the news.
- **Session Management:** Sessions are managed using cookies, allowing users to maintain their state across requests.
- **User Authentication:** Anonymous users will lose all of their data once they logout. Whereas logging out won't delete the registered users sessions. 

## Application Structure

```plaintext
.
├── app
│   ├── core
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── __init__.py
│   │   └── templates.py
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── sessions.py
│   │   └── users.py
│   ├── routers
│   │   ├── auth.py
│   │   ├── __init__.py
│   │   ├── news.py
│   │   └── users.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── users.py
│   ├── services
│   │   ├── dependencies.py
│   │   └── __init__.py
│   └── templates
│       ├── landing_page.html
│       ├── news.html
│       └── signup.html
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── sql_app.db
└── tests
    ├── __init__.py
    ├── test_auth.py
    └── test_users.py
```

### 1. How Surfing Anonymously is Served
Anonymous surfing is facilitated by session management using cookies. When an anonymous user accesses the news page, the application checks for an existing session token in the cookies. If none exists, a new session is created.

### 2. Handling Anonymous Sessions
* <b>Session Token Check:</b> When a user visits the `/news` route, the application checks if a session token exists in the user's cookies.  If not, it creates a new session.

* <b>Anonymous User Identification:</b> If the session token exists but is not associated with a registered user, the user is treated as an anonymous user.

* <b>Session Validation:</b> The session token is validated against the database to ensure it's still valid.

* <b>Session Creation:</b> If the session is not found or is invalid, a new session is created, and a session token is stored in the user's cookies.

### 3. Anonymous Surfing Flow
###### User Accesses News Page: 
* If a session token exists, the application checks if it's valid and retrieves the associated user (if any).

* If no session token exists or the session is invalid, a new session is created, and the user is treated as anonymous.

###### User Logs Out:
* When an anonymous user logs out, the session is deleted from the database, and the session cookie is cleared.

### 4. Logout for Anonymous Users
Anonymous users can log out, which effectively clears their session from the database and deletes their session cookie.

```bash
@auth_router.get("/logout")
async def logout(
    request: Request, 
    response: Response, 
    db: Session = Depends(get_db),
    user_data: dict = Depends(get_current_user)
):
    
    user_session = user_data["user_session"]
        
    # Delete the session from the database only if the user is anonymous
    if not user_session.user_id:
        db.delete(user_session)
        db.commit()

    # Delete the session cookie by setting it to an empty value
    response.set_cookie(
        key="session_token",
        value=""
    )

    return RedirectResponse(url="/", status_code=303)
```

## Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/veyselserifoglu/fastapi-oauth-lazy-registration.git
cd fastapi-oauth-lazy-registration
```

### 2. Access the application inside the devcontainer via VScode

**Follow the instruction [here](access_app_inside_devcontainer.md)**

### 3. Install Dependencies

All requirements will be installed when building the dockerfile. Yet, you can still see that for your self: 

```bash
pip install -r requirements.txt
```

<b>Note:</b> Any library you install inside the DevContainer will be installed only within the container. You will lose these installations after closing the remote connection. If the library or tool you wish to install is important for your future work, make sure to add it to the requirements.txt file to ensure it is included in the environment every time the container is rebuilt.

### 4. Setup database

The application aims to illustrate how anonymous browsing works with FastAPI, it was prefered to use a simple sqllight3 database for simple DB operations. 

If you prefer to use a different database like `MYSQL`, you can still do that. You only need to edit the database URL in the configurations file

```plaintext
1. go to app -> core > config.py
2. modify the DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
3. add any database URL you wish to use.
```

### 5. Accessing the Application

* Once the container is running, you’ll be able to use VSCode as if you were working on your local machine, but all operations will occur inside the Docker container.
* Open a terminal inside VSCode.
* Run your application inside the container:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

* Access the application by navigating to [http://localhost:8000](http://localhost:8000) in your browser.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
