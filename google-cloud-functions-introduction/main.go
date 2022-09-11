package googlecloudfunctionsintroduction

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

var greeting string = "hi"

func init() {
	functions.HTTP("GreeterGet", greetingHandler)
}

func greetingHandler(w http.ResponseWriter, r *http.Request) {
	message := fmt.Sprintf("%s there", greeting)

	// Generate some logs
	log.Println("Received request. Sending Greeting.")

	// Check if PR number is set
	prNumber := os.Getenv("PR_NO")
	if prNumber != "" {
		message = fmt.Sprintf("%s there from #%s", greeting, prNumber)
	}

	// Write response to client
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]string{"greeting": message})
}
