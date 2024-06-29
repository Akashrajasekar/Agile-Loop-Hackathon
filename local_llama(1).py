# import subprocess

# def generate_event_details(prompt):
#     process = subprocess.Popen(
#         ["ollama", "run", "llama-3b", prompt],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#     stdout, stderr = process.communicate()
    
#     if process.returncode != 0:
#         raise Exception(f"Error: {stderr}")
    
#     return stdout

# if __name__ == "__main__":
#     prompt = "Create a new event titled 'Project Meeting' on 2024-06-28 at 10:00 AM"
#     response = generate_event_details(prompt)
#     print(response)

from langchain_community.llms import Ollama
# llm = Ollama(model="llama3")
# print(llm.invoke("Hi", stop=['<|eot_id|>']))

def generate_event_details(prompt, emails):
    llm = Ollama(model="llama3")
    refined_prompt = f"""Generate event details for Google Calendar in the following JSON format. Keep the attendees part as it is. Only give the JSON format and don't type 
    any other text:
        {{
            'summary': 'Meeting with John',
            'location': '123 Main St, Anytown, USA',
            'description': 'Discuss project updates',
            'start_time': '2024-07-01T10:00:00-07:00',
            'end_time': '2024-07-01T11:00:00-07:00',
            'time_zone': 'America/Los_Angeles',
            'attendees': {emails}
        }}
    Event = "{prompt}"
    """
    # print(refined_prompt)
    response = llm.invoke(refined_prompt, stop=['<|eot_id|>'])
    return response

if __name__ == "__main__":
    prompt = "Meeting with Kaaka at the office on 2024-07-03 from 10:00 AM to 11:00 AM, Pacific Time"
    emails = ['f20210183@dubai.bits-pilani.ac.in','f20210007@dubai.bits-pilani.ac.in']
    response = generate_event_details(prompt, emails)
    print(response)
    # generate_event_details(prompt, emails)