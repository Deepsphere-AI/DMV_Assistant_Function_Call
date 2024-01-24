import streamlit as vAR_st
import os
import time
from openai import OpenAI
from streamlit_chat import message
import json
from DSAI_SourceCode_Implementation.DSAI_BQ_Data import get_config_details

client = OpenAI()


def FunctionWithAssistant():
    
    # get_config_details("TOO7")

    vAR_assistant_id = os.environ["ASSISTANT_ID"]

    if "thread_id" not in vAR_st.session_state:
        vAR_st.session_state.thread_id = None

    if 'generated' not in vAR_st.session_state:
        vAR_st.session_state['generated'] = ["We are delighted to have you here in the DMV's Internal Query Team"]

    if 'history' not in vAR_st.session_state:
        vAR_st.session_state['history'] = ["Hello!"]
        
    thread = client.beta.threads.create()
    vAR_st.session_state.thread_id = thread.id
    vAR_container = vAR_st.container()
    response_container = vAR_st.container()
    with vAR_container:       
        with vAR_st.form(key='my_form ', clear_on_submit=True):
        
            vAR_user_input = vAR_st.text_input("Prompt:", placeholder="How can I help you?", key='input')
            vAR_submit_button = vAR_st.form_submit_button(label='Chat')
    
        if vAR_user_input and vAR_submit_button:
            vAR_response = run_assistant(vAR_user_input,vAR_st.session_state.thread_id,vAR_assistant_id)
            vAR_st.session_state['history'].append(vAR_user_input)
            vAR_st.session_state['generated'].append(str(vAR_response))
        
        
    if vAR_st.session_state['generated']:
        with response_container:
            for i in range(len(vAR_st.session_state['generated'])):
                message(vAR_st.session_state["history"][i], is_user=True, key=str(i) + '_user ', avatar_style="big-smile")
                message(vAR_st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
    
    

def run_assistant(vAR_user_input,thread_id,vAR_assistant_id):
    
    try:
        content = ""
        # Add the user's message to the existing thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=vAR_user_input
        )
        
        # Create a run with additional instructions
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=vAR_assistant_id,
            instructions="Give me the details about the given configuration?")
        
        while True:
            # Wait for 2 seconds
            time.sleep(2)

            # Retrieve the run status
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            print('run status - ',run_status.model_dump_json(indent=4))


            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )

                # Loop through messages and print content based on role
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    print(f"{role.capitalize()}: {content}")

                    return content
            elif run_status.status == 'requires_action':
                print("Function Calling")
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                print('required_actions - ',required_actions)
                tool_outputs = []
                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])
                    print("arguments - ",arguments)
                    
                    if func_name == "get_config_details":
                        output = get_config_details(arguments["vAR_config"])
                        
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": output
                        })
                    else:
                        raise ValueError(f"Unknown function: {func_name}")
                    
                print("Submitting outputs back to the Assistant...")
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            else:
                print("Waiting for the Assistant to process...")
                time.sleep(5)

    except IndexError as e:
        return "Record not found in the bigquery table for given configuration."
    except BaseException as e:
        vAR_st.error("Error - "+str(e))        
        

# Reference Link:https://mer.vin/2023/11/openai-assistants-api-function-calling/