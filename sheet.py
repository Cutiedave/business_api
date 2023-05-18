import gspread

#connect to the service account
gc = gspread.service_account(filename="creds.json")

#connect to your sheet (between "" = the name of your G Sheet, keep it short)
sh = gc.open("Python Connect").sheet1

#get the values from cells a2 and b2
name = sh.acell("a2").value
website = sh.acell("b2").value

print(name)
print(website)

#in our demo, this should print out "Frederick" and "callmefred.com"

#write values in cells a3 and b3
sh.update("a3", "Chat GPT")
sh.update("b3", "openai.com")