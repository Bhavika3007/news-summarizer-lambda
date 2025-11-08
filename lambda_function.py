import json
import requests
import os
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    #  Get URL from POST body
    body = json.loads(event.get("body", "{}"))
    url = body.get("url")
    
    if not url:
        return {"statusCode": 400, "body": json.dumps({"error": "No URL provided"})}

    #  Fetch article content
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.get_text() for p in paragraphs])

        # Optional: truncate long articles to avoid Hugging Face API token limits
        max_chars = 3000
        article_text = article_text[:max_chars]

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    #  Prepare payload for Hugging Face Router API
    try:
        summary_api = "https://router.huggingface.co/hf-inference"
        headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}
        payload = {
            "model": "facebook/bart-large-cnn",
            "inputs": article_text,
            "options": {"wait_for_model": True}  # ensures the model is ready
        }

        #  Call Hugging Face API
        response = requests.post(summary_api, headers=headers, json=payload, timeout=30)

        #  Handle API response safely
        if response.status_code != 200:
            summary = f"Summary API failed: {response.text}"
        else:
            try:
                summary_data = response.json()
                if isinstance(summary_data, list) and "summary_text" in summary_data[0]:
                    summary = summary_data[0]["summary_text"]
                elif isinstance(summary_data, dict) and "error" in summary_data:
                    summary = "Summary API failed: " + summary_data["error"]
                else:
                    summary = "Could not summarize article."
            except Exception as e:
                summary = "Summary API failed: " + str(e)

    except Exception as e:
        summary = "Summary API failed: " + str(e)

    #  Return summary to API Gateway
    return {
        "statusCode": 200,
        "body": json.dumps({"summary": summary})
    }
