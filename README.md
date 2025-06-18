# learou

A Django based platform for tracking learning process


# Tailwind

## Installation

```
npm install tailwindcss @tailwindcss/cli
```

## Setup
```learou/static/css/learou.css
@import "tailwindcss";
```

## Autoupdating
This will update the css automatically during the development process

```
npx @tailwindcss/cli -i learou/static/css/learou.css -o learou/static/css/main.css --watch
```


# DaisyUI

Built on top of Tailwind, will simplify the process by adding base [components](https://daisyui.com/components/)

## Instalation

```
npm install -D daisyui@latest
```

## Setup
Add this
```learou/static/css/learou.css
@plugin "daisyui";
```
