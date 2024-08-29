FROM node:20.11-alpine3.19 AS build-stage

RUN npm config set registry https://registry.npmmirror.com

WORKDIR /app
COPY package*.json ./

RUN npm install

COPY . .
RUN npm run build

FROM nginx:stable-alpine

COPY --from=build-stage /app/dist/ /usr/share/nginx/html

EXPOSE 80
