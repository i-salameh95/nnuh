FROM node:10

WORKDIR /app/theme

#RUN yarn install

EXPOSE 3000/tcp

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["npm", "run", "hot"]
