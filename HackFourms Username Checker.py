# imports needed librarys
from bs4 import BeautifulSoup
import requests
import time

# this is the header requests will be using
user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0"}

# will prompt the user for the name of the username list
list_name = input("Please enter the name of your username list: ")

# this will import the usernames and convert them to a list
with open(list_name, "r") as f:
	username_list = f.read().split("\n")

# for every username in the list this will check if it's available
for username in username_list:

	# this will remove any spaces before and after the username to prevent confusion
	# if there is any spaces other than between words it will return the username as available no matter what
	clean_username = " ".join(x for x in username.split() if x != " ")

	# usernames with a length less than 4 cannot be used to sign up
	if len(clean_username) >= 4:

		# a list of all found usernames
		# sets it to empty at the start of the loop
		found_usernames = []

		# adds the username to url parameters
		username_params = {"action":"get_users", "query":clean_username}

		# pulls the html of the results
		r = requests.get("https://hackforums.net/xmlhttp.php?", params=username_params, headers=user_agent)

		# checks if the returned status code is anything but 200
		if str(r.status_code) != "200":
			time.sleep(0.8) # waits 800 miliseconds
			continue # starts from the top of the loop

		# finds all usernames on page and adds them to a list for comparing
		soup = BeautifulSoup(r.content, "html.parser")
		samples = soup.find_all("span", {"class":"username"})
		for i in samples:
			found_usernames.append(i.text.lower())

		# if the username is not in the list then it's available
		if clean_username.lower() not in found_usernames:
			print("{} is available".format(username)) # prints available username

		# waits to go
		time.sleep(0.8) # 800 miliseconds is the sweetspot in which HackForums does not block the IP and return a 503 error