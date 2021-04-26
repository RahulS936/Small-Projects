import time
from datetime import datetime as dt

host_temp = r".\Website-Blocker\hosts"
host_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"
website_blocklist = ["www.facebook.com", "facebook.com", "www.fb.com", "fb.com", "www.instagram.com", "instagram.com"]
working_hr_start = 9
working_hr_end = 18

while True:
    if working_hr_start < dt.now().hour < working_hr_end:
        print("Working Hours...")
        with open(host_temp, 'r+') as file:
            content = file.read()
            for website in website_blocklist:
                if website in content:
                    pass
                else:
                    file.write(redirect+"\t"+website+"\n")
    else:
        print("Fun Time...")
        with open(host_temp, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if not any(website in line for website in website_blocklist):
                    file.write(line)
            file.truncate() 
    time.sleep(5)