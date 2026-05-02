import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI assistant for Jeblio Corporation.

Jeblio:
- Services: Software Development, Digital Marketing, Business Development
- Internships: Multiple domains (Web, Mobile, Data Science, UI/UX, Marketing)
- Duration: 25 days
- Features: Certificate, mentorship, real projects

Contact:
- Phone: +91 9952877911, 8344536200
- Email: jeblioinfo@gmail.com

Rules:
- Answer only about Jeblio
- Keep answers short (max 3–5 lines)
- Be professional
- If unrelated → redirect to Jeblio services
- Do not give fake information
"""

def generate_ai_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return str(e)