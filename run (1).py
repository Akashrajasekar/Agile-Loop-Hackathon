from helper import *
import mysql.connector
import random
import os
import requests
import datetime
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

    scenario = input(
        "Please select a scenario (gcalendar/gmail/twitter): "
    )

    scenario = scenario.lower()
    api_spec, headers = None, None

    # database connection details
    db_config = {
        'host': 'localhost',
        'database': 'synapse-copilot',
        'user': 'root',
        'password': '2021A7PS0183U',
    }

    # Connect to the MySQL server
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    user_id = int(input("Enter the user id: "))

    if scenario == "tmdb":
        os.environ["TMDB_ACCESS_TOKEN"] = config["tmdb_access_token"]
        api_spec, headers = process_spec_file(
            file_path="specs/tmdb_oas.json", token=os.environ["TMDB_ACCESS_TOKEN"]
        )
        query_example = "Give me the number of movies directed by Sofia Coppola"

    elif scenario == "spotify":
        os.environ["SPOTIPY_CLIENT_ID"] = config["spotipy_client_id"]
        os.environ["SPOTIPY_CLIENT_SECRET"] = config["spotipy_client_secret"]
        os.environ["SPOTIPY_REDIRECT_URI"] = config["spotipy_redirect_uri"]

        api_spec, headers = process_spec_file(file_path="specs/spotify_oas.json")

        query_example = "Add Summertime Sadness by Lana Del Rey in my first playlist"

    elif scenario == "discord":
        os.environ["DISCORD_CLIENT_ID"] = config["discord_client_id"]

        api_spec, headers = process_spec_file(
            file_path="specs/discord_oas.json", token=os.environ["DISCORD_CLIENT_ID"]
        )
        query_example = "List all of my connections"

    elif scenario == "stable":
        api_spec, headers = process_spec_file(
            file_path="specs/stablediffiusion_oas.json", token=os.environ["API_KEY"]
        )
        query_example = "Create cat image"

    elif scenario == "calendar":
        if user_id is not None:
            try:
                ser_qu = f"SELECT * FROM credentials WHERE user_id = {user_id};"
                cursor.execute(ser_qu)
                res = cursor.fetchone()
                res_t = res[2]
                print(f"your token {res_t}")
                os.environ["GOOGLE_TOKEN"] = res_t
                dic = {
                    "user_id": user_id,
                    "your_token": res_t
                }
                print(dic)
            except:
                print("Key is not present in the database")
                return ""

        else:
            print("Your id is incorrect.")

        api_spec, headers = process_spec_file(
            file_path="specs/calendar_oas.json", token=os.environ["GOOGLE_TOKEN"]
        )
        query_example = "What events do I have today?"

    elif scenario == "sheets":
        os.environ["GOOGLE_TOKEN"] = config["google_token"]

        api_spec, headers = process_spec_file(
            file_path="specs/sheets_oas.json", token=os.environ["GOOGLE_TOKEN"]
        )
        query_example = 'Create a new Spreadsheet with title: "Exercise Logs". Print the complete api response result as it is.'

    elif scenario == "notion":
        os.environ["NOTION_KEY"] = config["NOTION_KEY"]
        query_example = "Get me my page on notion"

    elif scenario == "upclick":
        os.environ["UPCLICK_KEY"] = config["UPCLICK_KEY"]

        api_spec, headers = process_spec_file(
            file_path="specs/upclick_oas.json", token=os.environ["UPCLICK_KEY"]
        )

        headers["Content-Type"] = "application/json"
        query_example = "Get me my spaces of team on upclick"

    elif scenario == "jira":
        if user_id is not None:
            try:
                ser_qu = f"SELECT * FROM jira_credentials WHERE user_id = {user_id};"
                cursor.execute(ser_qu)
                res = cursor.fetchone()
                token = res[2]
                host = res[3]
                username = res[3]

                print(f"Fetched Jira token: {token}")
                print(f"Fetched Jira host: {host}")
                print(f"Fetched Jira username: {username}")

                os.environ["JIRA_TOKEN"] = token
                os.environ["jira_HOST"] = host

                dic = {
                    "user_id": user_id,
                    "user_token": token,
                    "user_host": host,
                    "user_name": username
                }
                print(dic)

                replace_api_credentials(
                    model="api_selector",
                    scenario=scenario,
                    actual_key=username,
                    actual_token=token
                )
                replace_api_credentials(
                    model="planner",
                    scenario=scenario,
                    actual_key=username,
                    actual_token=token
                )
            except Exception as e:
                print(f"key is not present in the database due to: {e}")
                return ""

            # Call the jira specific method to change the host and token with actual values
            replace_api_credentials_in_jira_json(
                scenario=scenario,
                actual_token=token,
                actual_host=host,
                actual_username=username
            )
            api_spec, headers = process_spec_file(
                ### to make the specs file minify or smaller for better processing
                file_path="specs/jira_oas.json",
                token=token,
                username=username
            )
        query_example = "Create a new Project with name 'abc_project'"

    elif scenario == "gcalendar":
        api_key = config["google_calendar"]["api_key"]
        creds_path = config["google_calendar"]["creds_path"]
        token_path = config["google_calendar"]["token_path"]
    
        # Get Google Calendar service
        service = get_google_calendar_service(creds_path, token_path)

        # Example query for event details
        prompt = "Setup a meeting called 'Envent' at the location Dubai on 2024-06-29 from 12:49 PM to 1:49 PM, Asia/Dubai time"
        email_list = ['f20210183@dubai.bits-pilani.ac.in','f20210007@dubai.bits-pilani.ac.in']
        
        # Generate event details using Llama model
        changed_prompt = generate_event_details(prompt, email_list)
        
        # Example event details
        # event_details = {
        #     'summary': 'Meeting with John Yolo',
        #     'location': '123 Main St, Anytown, USA',
        #     'description': 'Discuss project updates',
        #     'start_time': '2024-07-04T10:00:00-07:00',
        #     'end_time': '2024-07-04T11:00:00-07:00',
        #     'time_zone': 'America/Los_Angeles',
        #     'attendees': ['f20210183@dubai.bits-pilani.ac.in','f20210007@dubai.bits-pilani.ac.in']
        # }
        #Format the event
        event_details = format_event_response(changed_prompt)
        # Create the event
        create_google_calendar_event(service, event_details, False)      
        query_example = "Setup a meet with John at 10:00 AM"
        
    elif scenario == "trello":
        os.environ["TRELLO_API_KEY"] = config["trello_key"]
        os.environ["TRELLO_TOKEN"] = config["trello_token"]

        key = os.environ["TRELLO_API_KEY"]
        token = os.environ["TRELLO_TOKEN"]

        replace_api_credentials_in_json(
            scenario=scenario,
            actual_key=key,
            actual_token=token,
        )
        api_spec, headers = process_spec_file(
            file_path="specs/trello_oas.json",
            token=token,
            key=key,
        )

        replace_api_credentials(
            model="api_selector",
            scenario=scenario,
            actual_key=key,
            actual_token=token,
        )
        replace_api_credentials(
            model="planner",
            scenario=scenario,
            actual_key=key,
            actual_token=token,
        )

        query_example = "Create a new board with name 'abc_board'"

    elif scenario == "salesforce":
        credentials_fetch_query = f"SELECT * FROM salesforce_credentials WHERE user_id = {user_id};"
        cursor.execute(credentials_fetch_query)
        query_result = cursor.fetchone()

        domain = query_result[1]
        version = query_result[2]
        client_id = query_result[3]
        client_secret = query_result[4]
        access_token = query_result[5]

        print(f"Salesforce Domain: {domain}")
        print(f"Salesforce Version: {version}")
        print(f"Salesforce Client ID: {client_id}")
        print(f"Salesforce Client Secret: {client_secret}")
        print(f"Salesforce Access Token: {access_token}")

        replace_credentials_salesforce_json(
            scenario=scenario,
            actual_domain=domain,
            actual_version=version,
            actual_client_id=client_id,
            actual_client_secret=client_secret,
            actual_access_token=access_token
        )

        api_spec, headers = process_spec_file(
            file_path="specs/salesforce_oas.json",
            token=access_token,
        )
        query_example = "Create a new folder with name 'abc_folder'"
    else:
        raise ValueError(f"Unsupported scenario: {scenario}")

    populate_api_selector_icl_examples(scenario=scenario)
    populate_planner_icl_examples(scenario=scenario)

    requests_wrapper = Requests(headers=headers)

    # text-davinci-003

    llm = Ollama(model="llama3", temperature=0.0)

    # Instantiate the ApiLLM with the Llama model
    # api_llm = ApiLLM(
    #     llm,
    #     api_spec=api_spec,
    #     scenario=scenario,
    #     requests_wrapper=requests_wrapper,
    #     simple_parser=False,
    # )

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
    