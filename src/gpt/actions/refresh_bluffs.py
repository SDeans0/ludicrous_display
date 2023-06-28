import openai
import gpt.prompts.bluffball as bluffball

def generate_from_prompt(prompt=bluffball.prompt):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"content": prompt, "role": "system"}, {
    "role": "assistant",
    "content": "{\n  \"headline\": \"Manchester United signs new striker\",\n  \"player\": \"Gareth Bale\",\n  \"club\": \"Real Madrid\",\n  \"fee\": \"$100 million\",\n  \"contract\": \"5-year deal\"\n}"
  }],
        max_tokens=1000,
    )

    return response.values()

if __name__ == "__main__":
    b=1
    print(generate_from_prompt())