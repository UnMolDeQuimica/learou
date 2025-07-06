FROM node:23

WORKDIR /node

COPY package*.json ./

RUN npm install

COPY . . 
CMD set xe; npx @tailwindcss/cli -i learou/static/css/learou.css -o learou/static/css/tailwindcss
CMD set xe; npx @tailwindcss/cli -i learou/static/css/learou.css -o learou/static/css/main.css
