# syntax=docker/dockerfile:1.7-labs

FROM node:20-alpine as build
WORKDIR /app

ARG apiURI, apiURL
ENV NUXT_PUBLIC_API_URI $apiURI
ENV NUXT_PUBLIC_API_URL $apiURL

COPY ./package.json .
COPY ./yarn.lock .
RUN yarn install

COPY --exclude=./nginx . .
RUN yarn nuxi generate

RUN cp -r ./.output/public /static

FROM nginx:1.25-alpine as serve
RUN mkdir /var/www
COPY --from=build /static /var/www

RUN rm -rf /etc/nginx
COPY ./nginx/conf /etc/nginx