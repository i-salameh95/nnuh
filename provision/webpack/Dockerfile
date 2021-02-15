FROM node:latest

WORKDIR /app/theme

#RUN yarn install

EXPOSE 3000/tcp

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

RUN chmod +x /entrypoint.sh

CMD ["npm", "run", "hot"]
