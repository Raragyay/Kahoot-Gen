FROM node:15 AS builder

WORKDIR /usr/src/client

ENV PATH /usr/src/client/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build

# Stage 2
FROM nginx:1.18

WORKDIR /usr/src/client/build

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY --from=builder /usr/src/client/build .