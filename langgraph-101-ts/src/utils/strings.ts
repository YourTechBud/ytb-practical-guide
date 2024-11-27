export const extractJsonFromString = (inputStr: string): Record<string, any> | null => {
    // Regular expression to extract JSON from the string
    const jsonMatch = inputStr.match(/{.*}/s)

    if (jsonMatch) {
        const jsonStr = jsonMatch[0]
        try {
            // Parse the JSON string
            const jsonData = JSON.parse(jsonStr)
            return jsonData
        } catch (error) {
            console.error("Error: Invalid JSON format.")
            return null
        }
    } else {
        console.error("Error: No JSON found in the input string.")
        return null
    }
}