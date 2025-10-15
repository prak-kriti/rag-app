import openai
from app.core.config import settings

# Use your Grok API key
openai.api_key = settings.OPENAI_API_KEY

class LLMClient:
    def generate(self, query, context_chunks):
        prompt = "Use the following context to answer the question:\n\n"
        prompt += "\n".join(context_chunks)
        prompt += f"\n\nQuestion: {query}\nAnswer:"

        # New API call using chat/completion endpoint
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Grok-supported model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()



