FROM node

WORKDIR /code/frontend

COPY . /code/frontend
RUN npm install --legacy-peer-deps


EXPOSE 3000

CMD ["npm", "start"]