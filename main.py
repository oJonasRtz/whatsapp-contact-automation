from dotenv import load_dotenv
from supabase import create_client
import requests
import os


def main():
	load_dotenv()

	# Connect to Supabase
	URL = os.getenv("SUPABASE_URL")
	KEY = os.getenv("SUPABASE_KEY")
	supabase = create_client(URL,KEY)


	#test connection
	res = supabase.table("contacts").select("*").execute()
	print(res.data)


if __name__ == "__main__":
	main()
