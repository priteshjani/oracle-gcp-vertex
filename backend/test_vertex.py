import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth

def test_connection():
    PROJECT_ID = "my-service-prj-476616"
    LOCATION = "us-east4"
    
    print(f"Initializing Vertex AI in {LOCATION}...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # We use the versioned model ID to bypass alias issues
    model_id = "gemini-2.5-pro"
    
    try:
        model = GenerativeModel(model_id)
        print(f"Attempting to generate text with {model_id}...")
        
        response = model.generate_content("Say 'Vertex AI is working!'")
        
        print("-" * 30)
        print(f"SUCCESS: {response.text}")
        print("-" * 30)
        
    except Exception as e:
        print("-" * 30)
        print(f"FAILED: {e}")
        print("-" * 30)
        print("Tip: Check if 'aiplatform.googleapis.com' is enabled and ")
        print("the service account has 'Vertex AI User' permissions.")

if __name__ == "__main__":
    test_connection()
