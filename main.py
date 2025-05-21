import ollama
import sys_msgs

model = 'gemma2:2b'
messages = []
messages.append(sys_msgs.main_llm)




global greer
greer = input("User: ")
messages.append(
    {
        'role':'user',
        'content':greer
    },
)



try:
    res = ollama.chat(
        model=model,
        messages=messages
    )
    print(res['message']['content'])

except Exception as e:
    print(f"Error sending message to LLM: {e}")

