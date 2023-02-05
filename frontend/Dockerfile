FROM node:alpine as builder

WORKDIR /vue

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build


FROM nginx:alpine as production
COPY nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /vue/dist /usr/share/nginx/html

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]