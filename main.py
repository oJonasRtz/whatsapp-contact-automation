from dotenv import load_dotenv
from supabase import create_client, Client
import requests
import os


def get_db_data(supabase: Client, table: str, limit: int) -> list[dict]:
	"""Fetches data from the specified table in the Supabase database.
	Parameters:
		supabase (Client): The Supabase client.
		table (str): The name of the table to fetch data from.
		limit (int): The maximum number of records to fetch.
	Returns:
		list[dict]: A list of contact dictionaries.
	Raises:
		ValueError: If the parameters are invalid.
		Exception: If the API call fails.
	"""

	# Validate parameters
	if (
		not isinstance(table, str) or not table.strip() or
		not isinstance(limit, int) or limit <= 0 or
		not isinstance(supabase, Client) or not supabase
	):
		raise ValueError("Invalid parameters: Check table name, limit, and Supabase client.")

	# Create a Supabase client and fetch contacts
	res = supabase.table(table.strip()).select("*").limit(limit).execute()

	# Error handling for the response
	if hasattr(res, "error") and res.error:
		raise Exception(f"Error fetching contacts from Supabase: {res.error}")

	return res.data or []


def send_whatsapp_message(instance_id: str, token: str, to: str, message: str) -> None:
	"""Sends a WhatsApp message using the Z-API.
	Parameters:
		instance_id (str): The Z-API instance ID.
		token (str): The Z-API token.
		to (str): The recipient's phone number.
		message (str): The message to send.
	Returns:
		None
	Raises:
		ValueError: If any of the parameters are not strings.
		Exception: If the API call fails.
	"""

	# Validate input parameters
	for param in [instance_id, token, to, message]:
		if not isinstance(param, str) or not param.strip():
			raise ValueError("All parameters must be strings and cannot be empty.")

	url = f"https://api.z-api.io/instances/{instance_id.strip()}/token/{token.strip()}/send-text"
	payload = {
		"phone": to.strip(),
		"message": message.strip()
	}

	res = requests.post(url, json=payload, timeout=10)

	if res.status_code != 200:
		raise Exception(res.text)


def main() -> None:
	limit = 3
	table = "contacts"

	# Load environment variables
	load_dotenv()
	SUPABASE_URL = os.getenv("SUPABASE_URL")
	SUPABASE_KEY = os.getenv("SUPABASE_KEY")
	ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
	ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
	if not SUPABASE_URL or not SUPABASE_KEY or not ZAPI_INSTANCE_ID or not ZAPI_TOKEN:
		raise ValueError("All environment variables must be set.")

	# Connect to Supabase and fetch contacts
	supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
	contacts = get_db_data(supabase, table, limit)

	# Z-API Calls
	for contact in contacts:
		phone = contact.get("phone")
		name = contact.get("name")
		if not phone or not name:
			print(f"Skipping contact with missing phone or name: {contact}")
			continue
		try:
			message = f"Olá, {name} tudo bem com você?"
			send_whatsapp_message(ZAPI_INSTANCE_ID, ZAPI_TOKEN, phone, message)
		except Exception as e:
			print(f"Error sending message to {phone}: {e}")

if __name__ == "__main__":
	main()
