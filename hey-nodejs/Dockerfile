FROM node:18-slim
WORKDIR /hey-nodejs-app
COPY . /hey-nodejs-app
# Below RUN command to install node module directories -
RUN npm install
EXPOSE 3000
CMD ["node", "index.js"]