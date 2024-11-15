from groq import Groq


def setup_groq_client():
    client = Groq()


def make_question(prompt):
    completion = client.chat.completions.create(
        model="llama-3.2-90b-text-preview",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")