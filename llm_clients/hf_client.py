import os
import requests
import logging
from typing import Dict, Any, List, Optional
from tenacity import retry, stop_after_attempt, wait_random_exponential

logger = logging.getLogger(__name__)

class HFClient:
    """
    Client for interacting with the Hugging Face Serverless Inference API.
    """
    def __init__(self, model_id: Optional[str] = None, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("HF_TOKEN")
        self.model_id = model_id or os.getenv("HF_MODEL_ID", "meta-llama/Meta-Llama-3-8B-Instruct") # Default model

        if not self.api_token:
            raise ValueError("Hugging Face API token not found. Set HF_TOKEN environment variable.")
        if not self.model_id:
            raise ValueError("Hugging Face Model ID not found. Set HF_MODEL_ID environment variable or provide.")

        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        logger.info(f"HFClient initialized for model: {self.model_id}")

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Makes a request to the HF Inference API with retries."""
        logger.debug(f"Sending request to {self.api_url} with payload: {payload.get('inputs', 'payload too large to log')[:200]}...") # Log snippet
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=180) # Increased timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            logger.debug(f"Received response (status {response.status_code}).")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}. Response content: {e.response.text if e.response else 'No response'}")
             # Specific handling for model loading/availability errors if needed
            if e.response and e.response.status_code == 503: # Service Unavailable (often means model is loading)
                logger.warning("Model may be loading, retrying...")
                # Could add specific longer waits here if desired
            raise # Re-raise after logging to trigger tenacity retry

    def generate(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sends a generation request to the HF Inference API.

        Args:
            prompt: The input prompt for the model.
            params: Optional dictionary of generation parameters (e.g., max_new_tokens).

        Returns:
            A dictionary containing the model's response. The structure might vary,
            often like [{'generated_text': '...'}]. Returns raw response dict.
        """
        payload = {
            "inputs": prompt,
            # Add default or user-provided parameters
            "parameters": params or {
                "max_new_tokens": 1024, # Adjust default as needed
                "return_full_text": False, # Often needed to get only the completion
                "temperature": 0.7, # Example parameters, adjust as needed
                # Add other relevant parameters supported by the model/API
            },
            # Add options if needed, e.g., to wait for model loading
            "options": {
                "wait_for_model": True # Recommended for reliability
            }
        }
        response_data = self._make_request(payload)
        return response_data # Return the entire response structure

    def extract_generated_text(self, response: Dict[str, Any]) -> Optional[str]:
         """
         Extracts the primary generated text from a typical HF API response.
         Handles responses like [{'generated_text': '...'}]
         """
         if isinstance(response, list) and len(response) > 0 and isinstance(response[0], dict):
             return response[0].get("generated_text")
         elif isinstance(response, dict) and 'generated_text' in response: # Some models might return dict directly
            return response.get("generated_text")
         logger.warning(f"Could not extract 'generated_text' from response structure: {response}")
         return None
