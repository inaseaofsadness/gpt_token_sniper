import ollama
import sys_msgs
import asyncio

async def prompt(tweets):
    model = 'gemma2:2b'
    messages = []
    messages.append(sys_msgs.main_llm)
    
    tweets = "".join(tweets)

    greer = f"Here is a list of tweets for analysis: {tweets}"
    
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
        
        ai_analysis = res['message']['content']
        
        if "pump" in ai_analysis.lower():
            return "pump"
        else:
            return "dump"
        

    except Exception as e:
        print(f"Error sending message to LLM: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(prompt(tweets=0))
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting")