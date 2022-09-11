package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gorilla/mux"
)

var greeting string = "hi"
var delay int = 10

func main() {
	// Load the greeting from the environment variable
	g := os.Getenv("GREETING")
	if g != "" {
		log.Println("Loading greeting:", g)
		greeting = g
	}

	// Load the port from the environment variable
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	d := os.Getenv(("DELAY"))
	if n, err := strconv.Atoi(d); err == nil {
		log.Println("Loading delay:", n)
		delay = n
	}
	// Set up the routes
	r := mux.NewRouter()
	r.HandleFunc("/greeting/{name}", greetingHandler)

	// Start the server
	log.Printf("Starting server on port %s\n", port)
	if err := http.ListenAndServe(fmt.Sprintf(":%s", port), r); err != nil {
		log.Fatal("Error while starting server:", err)
	}
}

func greetingHandler(w http.ResponseWriter, r *http.Request) {
	// Get the name to greet
	vars := mux.Vars(r)
	name := vars["name"]

	// Introduce a delay in response
	time.Sleep(time.Duration(delay) * time.Millisecond)

	// Generate some logs
	log.Printf("Received name '%s'. Sending Greeting.", name)

	// Write response to client
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]string{"greeting": fmt.Sprintf("%s %s", greeting, name)})
}
