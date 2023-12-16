from openai import OpenAI
client = OpenAI()

messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]
  
while True:
    message = input("User : ")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = OpenAI.ChatCompletion.create(
            model="gpt-3.5-turbo-1106", messages=messages
        )
    
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})