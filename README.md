# learou

A Django based platform for tracking learning process


# Installation
## Using Docker

1. Create an env file at `.envs/.local/` named `.django`. It can be empty
```
mkdir -p .envs/.local
touch .envs/.local/.django
```
2. Build the project:
```
docker compose -f docker-compose-local.yml build
```

3. Run the project:

```
docker compose -f docker-compose-local.yml up
```

## Local installation

### Django app:
1. Install all the dependencies with `pip install -r requirements.txt`
2. Make the migrations with `python manage.py makemigrations`
3. Migrate the database with `python manage.py migrate`
4. Create a super user with `python manage.py createsuperuser`
5. Run the server with `python manage.py runserver`

### Tailwind

#### Installation

```
npm install tailwindcss @tailwindcss/cli
```

#### Setup
```learou/static/css/learou.css
@import "tailwindcss";
```

#### Autoupdating
This will update the css automatically during the development process

```
npx @tailwindcss/cli -i learou/static/css/learou.css -o learou/static/css/main.css --watch
```


### DaisyUI

Built on top of Tailwind, will simplify the process by adding base [components](https://daisyui.com/components/)

#### Instalation

```
npm install -D daisyui@latest
```

#### Setup
Add this
```learou/static/css/learou.css
@plugin "daisyui";
```
