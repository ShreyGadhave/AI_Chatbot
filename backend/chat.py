import subprocess

def query_ollama(prompt: str):
    """ Optimized function to send queries to Ollama with UTF-8 decoding, ignoring errors """
    process = subprocess.Popen(
        ["ollama", "run", "mistral:latest", prompt],  # Using mistral:latest
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Ensure text mode for output
        encoding='utf-8',  # Force UTF-8 encoding for output
        errors='ignore'  # Ignore any decoding errors
    )
    output, error = process.communicate()
    if error:
        print(f"Error: {error}")
    return output.strip() if output else "No output"
