from langchain_community.llms import Ollama
# llm = Ollama(model="llama3")
# print(llm.invoke("Hi", stop=['<|eot_id|>']))

def generate_event_details(prompt,emails):
    llm = Ollama(model="llama3")
    refined_prompt = f"""Generate event details for Google Calendar in the following JSON format. Keep the attendees part as it is. Only give the JSON format and don't type any other text:
        {{
            "summary": 'Meeting with John',
            "location": '123 Main St, Anytown, USA',
            "description": 'Discuss project updates',
            "start_time": '2024-07-01T10:00:00-07:00',
            "end_time": '2024-07-01T11:00:00-07:00',
            "time_zone": 'America/Los_Angeles',
            "attendees": {emails}
        }}
    Event = "{prompt}"
    """
    
    response = llm.invoke(refined_prompt, stop=['<|eot_id|>'])
    print("response=",response)
    return response

# if __name__ == "__main__":
#     prompt = "Meeting with Jane at the office on 2024-06-29 from 2:00 PM to 3:00 PM, Pacific Time"
#     response = generate_event_details(prompt)
#     print(response)
#     generate_event_details(prompt)