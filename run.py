from helper import *
import mysql.connector
from googleapiclient.discovery import build
from local_llama import generate_event_details
from langchain_community.llms import Ollama
logger = logging.getLogger()


def main():
    config = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
    # os.environ["OPENAI_API_KEY"] = config["openai_key"]
    # ☝️ To be replaced with Llama or any other way tp retreive API key
    
    logging.basicConfig(
        format="%(message)s",
        handlers=[logging.StreamHandler(ColorPrint())],
    )
    logger.setLevel(logging.INFO)
    api_spec, headers = None, None

    # database connection details
    db_config = {
        'host': 'localhost',
        'database': 'synapse-copilot',
        'user': 'root',
        'password': '*****',
    }

    # Connect to the MySQL server
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    user_id = int(input("Enter the user id: "))

    api_key = config["google_calendar"]["api_key"]
    creds_path = config["google_calendar"]["creds_path"]
    token_path = config["google_calendar"]["token_path"]

    # Get Google Calendar service
    service = get_google_calendar_service(creds_path, token_path)

    # Example query for event details
    prompt = "Setup a meeting called 'Envent' at the location Dubai on 2024-07-02 from 12:49 PM to 1:49 PM, Asia/Dubai time"
    email_list = ["akashrajasekar03@gmail.com","saadhanaashreeelango@gmail.com"]
    
    # Generate event details using Llama model
    changed_prompt = generate_event_details(prompt,email_list)

    #Format the event
    event_details = format_event_response(changed_prompt)
    print(event_details)
    # Create the event
    create_google_calendar_event(service, event_details, False)      
    query_example = "Setup a meet with John at 10:00 AM"

    populate_api_selector_icl_examples()
    populate_planner_icl_examples()

    requests_wrapper = Requests(headers=headers)

    llm = Ollama(model="llama3", temperature=0.0)

    print(f"Example instruction: {query_example}")
    query = input(
        "Please input an instruction (Press ENTER to use the example instruction): "
    )
    if query == "":
        query = query_example

    logger.info(f"Query: {query}")

    start_time = time.time()
    # api_llm.run(query)
    logger.info(f"Execution Time: {time.time() - start_time}")

if __name__ == "__main__":
    main()
    
