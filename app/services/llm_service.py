import json
import uuid

from app.databases.mongo import get_database
from app.helpers.exceptions import SessionInactiveError
from app.models.llm_conversation import LlmConversationRequest, LlmConversationResponse, LlmStaticConversationRequest
from app.models.llm_request import LLMRequest
from fastapi.encoders import jsonable_encoder
from openai import OpenAI
from datetime import datetime
from app.core.config import settings

llm_metadata_collection = "kiosk_llm_session_metadata"
llm_conversation_collection = "kiosk_llm_conversation_history"
menu_collection = "menu"


async def load_menu(db) -> dict:
    try:
        cursor = db[menu_collection].find({})
        documents = await cursor.to_list(length=1)
        if not documents:
            raise ValueError("Menu not found in the database.")
        menu = documents[0]

        if not menu:
            raise ValueError("Menu not found in the database.")

        # Remove MongoDB internal ID field (_id) if necessary
        menu.pop("_id", None)
        return menu
    except Exception as e:
        print(f"Error fetching menu from database: {e}")
        return None


async def save_metadata(data: LLMRequest) -> dict:
    db = get_database()
    result = await db[llm_metadata_collection].insert_one(jsonable_encoder(data))
    return {"data": "metadata saved", "inserted_id": str(result.inserted_id)}


async def get_entries() -> list:
    db = get_database()
    entries = await db[llm_metadata_collection].find().to_list(length=None)
    for entry in entries:
        entry['id'] = str(entry['_id'])
    return entries


async def validate_conversation_request(request: LlmConversationRequest):
    db = get_database()
    if not request.session_id:
        raise ValueError("Session ID is required.")
    if not request.messages:
        raise ValueError("messages is required.")
    if not request.timezone:
        raise ValueError("Timezone is required.")

    query = {
        'session_id': request.session_id
    }
    result = await db[llm_metadata_collection].find_one(query)
    if result:
        if result.get('status') != 'active':
            raise SessionInactiveError(request.session_id)
    else:
        raise SessionInactiveError(request.session_id)


def parse_llm_response(response_text):
    try:
        response_json = json.loads(response_text)
        intent = response_json.get("intent")
        item_name = response_json.get("item_name")
        reply = response_json.get("reply")
        return intent, item_name, reply
    except json.JSONDecodeError:
        print("Error parsing LLM response.")
        return None, None


def find_item_by_name(item_name, menu):
    for category, items in menu['categories'].items():
        for item in items:
            if item['name'].lower() == item_name.lower():
                return item
    return None


async def get_agent_response(conversation_history, menu, client):
    system_prompt = """
    You are a helpful restaurant ordering assistant. Classify the user's intent into one of the following categories:
    - `add_item`: The user wants to add an item to their order. If this is the intent, extract the item name.
    - `finalize_order`: The user wants to complete their order.
    - `general`: The user is asking a general question or chatting.

    Provide your response in JSON format:
    {
      "reply": "Your response to the user",
      "intent": "add_item | finalize_order | general",
      "item_name": "The name of the item to add, if applicable"
    }

    Here is the menu:
    """
    for category, items in menu['categories'].items():
        system_prompt += f"{category.capitalize()}:\n"
        for item in items:
            system_prompt += f" - {item['name']} (${item['price']})\n"

    # Corrected `content` key
    messages = [{"role": "system", "content": system_prompt}]
    for turn in conversation_history:
        messages.append({"role": turn['role'], "content": turn['content']})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=750,
            temperature=0.2,
            n=1,
            stop=None
        )
        response_text = response.choices[0].message.content.strip()

        intent, item_name, llm_reply = parse_llm_response(response_text)
        action = 0
        reply = ""

        if intent == "add_item":
            if item_name:
                item = find_item_by_name(item_name, menu)
                if item:
                    reply = f"I've added the {item['name']} to your order.\n"
                    reply += llm_reply
                    action = {"add_item_id": item['id']}
                else:
                    reply = "Sorry, I couldn't find that item on the menu."
            else:
                reply = "Could you please specify the item you'd like to order?"

        elif intent == "finalize_order":
            reply = "Your order has been finalized. Enjoy your meal!"
            action = {"finalize_order": 1}

        elif intent == "general":
            reply = llm_reply
            action = {"general": 1}

        return {"reply": reply, "action": action}

    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return {
            "reply": "I'm sorry, I'm having trouble processing your request right now.",
            "action": 0
        }


async def save_conversation_history(session_id: str, messages: list):
    """
    Save conversation history to MongoDB.
    """
    db = get_database()
    data = {
        "session_id": session_id,
        "messages": messages
    }
    result = await db[llm_conversation_collection].update_one(
        {"session_id": session_id},
        {"$set": data},
        upsert=True
    )
    return {"data": "conversation history saved"}


async def get_conversation_history(session_id: str) -> list:
    """
    Retrieve conversation history from MongoDB.
    """
    db = get_database()
    query = {"session_id": session_id}
    result = await db[llm_conversation_collection].find_one(query)
    if result:
        return result.get("messages", [])
    return []


async def validate_static_conversation_request(request: LlmStaticConversationRequest):
    if not request.session_id:
        raise ValueError("Session ID is required.")
    if not request.message:
        raise ValueError("messages is required.")


async def make_conversation(request: LlmStaticConversationRequest) -> LlmConversationResponse:
    """
    Processes a conversation request, validates it, fetches or updates conversation history,
    and generates a response using an LLM.
    """
    # Step 1: Validate the request
    await validate_static_conversation_request(request)

    db = get_database()

    # Step 2: Check if it's the start of a new conversation
    if request.start_conversation:
        # Generate a new session ID
        new_session_id = request.session_id

        try:
            # Save the new session ID in the conversation history
            initial_message = {
                "session_id": new_session_id,
                "messages": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            db_response = await db[llm_conversation_collection].insert_one(initial_message)
            print(f"New conversation session created with ID: {db_response.inserted_id}")
        except Exception as e:
            print(f"Error inserting new conversation session: {e}")
            raise ValueError("Failed to start a new conversation. Please try again later.")

    # Step 3: Retrieve the menu (assumes the menu is loaded into your application context)
    menu = await load_menu(db)
    if not menu:
        raise ValueError("Menu not found. Please ensure the menu is available.")

    # Step 4: Fetch conversation history for the session
    conversation_history = await get_conversation_history(request.session_id)

    # Step 5: Append the new user message to the conversation history
    conversation_history.append({"role": "user", "content": request.message})

    openai_api_key = settings.OPENAI_API_KEY
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in the .env file.")
    client = OpenAI(api_key=openai_api_key)

    # Step 6: Generate LLM response
    user_order = []  # Initialize or load user's order from a persistent source if required
    try:
        llm_response = await get_agent_response(conversation_history, menu, client)
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        llm_response = {
            "reply": "I'm sorry, but I encountered an issue while processing your request. Please try again.",
            "action": 0
        }

    # Step 7: Append the LLM's response to the conversation history
    conversation_history.append({"role": "assistant", "content": llm_response["reply"]})
    await save_conversation_history(request.session_id, conversation_history)

    # Step 8: Build and return the response
    return LlmConversationResponse(
        session_id=request.session_id,
        prompt_response=llm_response["reply"],
        action=llm_response["action"]
    )
