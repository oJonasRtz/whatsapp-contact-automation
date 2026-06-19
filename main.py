from dotenv import load_dotenv
from supabase import create_client
import requests
import os
import sys


def get_db_date(supabase: create_client, table: str, limit: int) -> list[dict]:
	"""Fetches data from the specified table in the Supabase database.
	Parameters:
		supabase (create_client): The Supabase client.
		table (str): The name of the table to fetch data from.
		limit (int): The maximum number of records to fetch.
	Returns:
		list[dict]: A list of contact dictionaries.
	"""
	# Validate the limit parameter
	if not isinstance(limit, int) or limit <= 0:
		raise ValueError("Limit must be a positive integer.")

	# Create a Supabase client and fetch contacts
	res = supabase.table(table).select("*").limit(limit).execute()

	# Error handling for the response
	# if res.status_code != 200:
	# 	raise Exception(f"Error fetching contacts from Supabase: {res.text}")

	return res.data


def send_whatsapp_message(instance_id: str, token: str, to: str, message: str) -> None:
	# Validate input parameters
	if not isinstance(instance_id, str) or not isinstance(token, str) or not isinstance(to, str) or not isinstance(message, str):
		raise ValueError("All parameters must be strings.")
	
	url = f"https://api.z-api.io/instances/{instance_id}/token/{token}/send-text"
	payload = {
		"phone": to,
		"message": message
	}

	res = requests.post(url, json=payload)

	if res.status_code != 200:
		raise Exception(f"Failed to send message: {res.text}")


def main(args: list[str]) -> None:
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
	contacts = get_db_date(supabase, table, limit)

	# Z-API Calls
	for contact in contacts:
		to = contact.get("phone")
		message = f"Olá {contact.get('name')}, tudo bem com voce?"
		send_whatsapp_message(ZAPI_INSTANCE_ID, ZAPI_TOKEN, to, message)


if __name__ == "__main__":
	main(sys.argv[1:])
