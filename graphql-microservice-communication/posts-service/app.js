const http = require('http');

posts = [
   {
      "id":"1",
      "userId": "1",
      "title": "How to make microservices communicate",
      "ts": "Sun Aug  1 09:40:14 IST 2021"
   },
   {
      "id":"2",
      "userId": "1",
      "title": "What is graphql",
      "ts": "Sun May  1 09:40:14 IST 2020"
   },
   {
      "id":"3",
      "userId": "2",
      "title": "What are microservices",
      "ts": "Mon Jun  1 09:40:19 IST 2021"
   },
   {
      "id":"4",
      "userId": "2",
      "title": "What is devops",
      "ts": "Sun May  1 09:40:14 IST 2020"
   },
   {
      "id":"5",
      "userId": "3",
      "title": "How to secure your database",
      "ts": "Mon Jun  1 09:40:19 IST 2021"
   },
   {
      "id":"6",
      "userId": "3",
      "title": "What is terraform & How to use it",
      "ts": "Sun May  1 09:40:14 IST 2020"
   },
]


http.createServer(function (req, res) {
   var url = req.url;

   if (url.startsWith('/list/posts')) {

      res.setHeader('Content-Type', 'application/json');
      res.write(JSON.stringify(posts)); //write a response
      res.end(); //end the response

   } else if (url.startsWith('/get/posts/user')) {      

      arr = url.split('/')
      userId = arr[arr.length - 1]
      temp = []
      for (let i = 0; i < posts.length; i++) {
         if (posts[i]["userId"] == userId) {
            temp.push(posts[i])
         }
      }

      res.setHeader('Content-Type', 'application/json');
      res.write(JSON.stringify(temp)); //write a response
      res.end(); //end the response

   } else if (url.startsWith('/get/posts')) {      

      arr = url.split('/')
      postId = arr[arr.length - 1]

      for (let i = 0; i < posts.length; i++) {
         if (posts[i]["id"] == postId) {
            res.setHeader('Content-Type', 'application/json');
            res.write(JSON.stringify(posts[i])); //write a response
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
}).listen(8082, function () {
   console.log("server start at port 8082"); //the server object listens on port 8082
});