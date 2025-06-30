From node:20  as  build

WORKDIR /app

COPY  package.json package-lock.json ./

COPY  . .

RUN npm run build


FROM nginx:stable-alpine

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /app/build/ /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx","-g","daemon off;"]