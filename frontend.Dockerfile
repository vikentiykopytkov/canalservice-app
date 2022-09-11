FROM node:14-slim

WORKDIR /usr/src/app

COPY frontend/package.json ./

COPY frontend/yarn.lock ./

RUN npm install

COPY frontend .

EXPOSE 3000

CMD ["npm", "start"]