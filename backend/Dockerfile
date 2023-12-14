FROM node:20.10.0
WORKDIR /backend
COPY package.json index.js /backend/
RUN npm install
RUN npm i -g nodemon
CMD ["nodemon", "index.js"]