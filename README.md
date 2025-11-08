# Serverless News Summarizer

This project is a serverless function using AWS Lambda and API Gateway that:

- Accepts a POST request with a news article URL
- Fetches the article content
- Summarizes the article using Hugging Face Inference API
- Returns the summary in JSON

## How to Deploy

1. Install dependencies:
   ```bash
   pip install -r requirements.txt -t .
2. Package Lambda function with dependencies:
    ```bash
    zip -r lambda_package.zip .


Make sure the zip contains lambda_function.py and the requests and bs4 libraries.

3. Upload the zip to AWS Lambda.

4. Set up API Gateway to expose a POST endpoint.

5. Replace YOUR_HUGGINGFACE_TOKEN in lambda_function.py with your Hugging Face token.

Example POST request

Send a POST request to your API Gateway endpoint, e.g.:

{
  "url": "https://www.bbc.com/news/world-60525350"
}

Example Response
{
  "summary": "Short summarized version of the article..."
}