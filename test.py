import traceroot
from traceroot import Integration
from openai import OpenAI

if __name__ == "__main__":
    traceroot.initialize(integrations=[Integration.OPENAI])
    client = OpenAI()
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
    )
    print(r.choices[0].message.content)