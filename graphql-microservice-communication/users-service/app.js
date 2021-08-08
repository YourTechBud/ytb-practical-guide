const http = require('http');

users = [
   {
      "id": "1",
      "name": "Tom",
      "address": "random address",
      "city": "Newyork",
      "age": 40
   },
   {
      "id": "2",
      "name": "Mike",
      "address": "random address",
      "city": "Mumbai",
      "age": 21
   },
   {
      "id": "3",
      "name": "Lee",
      "address": "random address",
      "city": "Bejing",
      "age": 28
   }
]


http.createServer(function (req, res) {
   var url = req.url;

   if (url.startsWith('/list/users')) {

      res.setHeader('Content-Type', 'application/json');
      res.write(JSON.stringify(users)); //write a response
      res.end(); //end the response

   } else if (url.startsWith('/get/users')) {

      arr = url.split('/')
      userId = arr[arr.length - 1]
      for (let i = 0; i < users.length; i++) {
         if (users[i]["id"] == userId) {
            res.setHeader('Content-Type', 'application/json');
            res.write(JSON.stringify(users[i])); //write a response
            res.end(); //end the response
            return
         }
      }

      res.writeHead(404, { 'Content-Type': 'application/json' }); // http header
      res.end(); //end the response

   } else {

      res.writeHead(404, { 'Content-Type': 'text/html' }); // http header
      res.write('<h1>Invalid URL!<h1>'); //write a response
      res.end(); //end the response

   }
}).listen(8081, function () {
   console.log("server start at port 8081"); //the server object listens on port 8081
});