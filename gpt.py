import openai
import time

# Set your OpenAI API key
openai.api_key = "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"

# Prepare your data for analysis
data = ["Your data goes here", "And here", "And here"]

# Define the model to use
model_engine = "text-davinci-002"

# Define the prompt for the OpenAI API call
prompt = f"Please analyze the sentiment of the following text:\n\n" + "\n\n".join(data) + "\n\n"

# Call the OpenAI API to analyze the sentiment of each piece of data
start_time = time.time()

results = openai.Completion.create (
                                    prompt=prompt,
                                    max_tokens=1024,
                                    n=len(data),
                                    stop=None,
                                    temperature=0.5,
                                    frequency_penalty=0,
                                    presence_penalty=0,
                                    timeout=60,
                                    model="davinci",
                                    stream=False,

                                    )


end_time = time.time()

# # Check if the API request was successful
# if results["code"] == 200:
#     # Parse the response JSON to extract the sentiment of each piece of data
#     for idx, choice in enumerate(results["choices"]):
#         sentiment = choice["text"].strip().replace("Sentiment:", "")
#         print(f"Sentiment of data point {idx + 1}: {sentiment}")
# else:
#     # If the API request failed, print the error message
#     print(f"Error: {results['message']}")
#
# print(f"Elapsed time: {end_time - start_time} seconds")
