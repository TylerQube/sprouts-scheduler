import re

class Volunteer:
    def __init__(self, name, email, phone, returning):
        self.name = name
        self.email = email
        self.phone = phone
        self.returning = returning
        self.availability = []

    def __str__(self):
        return f"{self.name}: {self.availability}"



    def load_availability(self, form):
        for column, value in form.items():
            if type(value) == float or "available" not in column and "interested" not in column:
                continue


            avails = available_from_form_column(column, value) 
            self.availability += avails

def load_volunteers(table):
    vollies = []
    for index, row in table.iterrows():
        # if index != 0:
        #     continue
        vol = Volunteer(
            row["Preferred name "],
            row["Email address"],
            row["Phone number"],
            row["Are you a returning volunteer?"] == "Yeah I am!",
        )

        # if duplicate entry, use most recent form submission
        existing = next(
            (v for v in vollies if v.name == vol.name and v.email == v.email), None
        )
        if existing:
            vollies.remove(existing)

        vol.load_availability(row)

        vollies.append(vol)

    return vollies

jobs = [
    "SPROUTS CAFE HELPER",
    "PREP",
    "COMMUNITY EATS SERVER",
    "PRODUCE MARKET",
    "DONATION DRIVER",
    "FRIDGE"
]

days = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "On-call"
]

def day_from_slot(day):
    for d in days:
        if d.lower() in day.lower():
            return d
    return "n/a"

def available_from_form_column(column, value):
    avails = []
    slots = value.split(",")
    job_name = "n/a"
    for j in jobs:
        if j.lower() in column.lower():
            job_name = j
    
    if "PRODUCE MARKET" in job_name or "FRIDGE" in job_name:
        for s in slots:
            day = s[0:s.index(" ")]
            time = s[s.index(" "):].strip()
            avails.append({
                "job_name": job_name,
                "day": day,
                "time": s
            })
    else:
        for s in slots:
            day = day_from_slot(column)
            if s == "Yes":
                print(job_name)
                job_name = "PREP"
                s = "5pm-8pm"
            elif s == "No":
                continue
            avails.append({
                "job_name": job_name,
                "day": day,
                "time": s
            })
    return avails
