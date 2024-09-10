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
            if type(value) == float or "available" not in column and "on-call volunteer" not in column:
                continue


            self.availability += available_from_form_column(column, value)

def load_volunteers(table):
    vollies = []
    for index, row in table.iterrows():
        # if index != 0:
        #     continue
        vol = Volunteer(
            row["First and last name"],
            row["Email"],
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
def available_from_form_column(column, value):
    avails = []
    times = value.split(",")
    job_name = "n/a"
    for j in jobs:
        if j.lower() in column.lower():
            job_name = j
    
    day = "n/a"
    for d in days:
        if d.lower() in value.lower():
            day = d
            break
        if d.lower() in column.lower():
            day = d
            break
    
    if "on-call volunteer" in column:
        if "no" in value.lower():
            return avails
        avails.append({
            "job_name": "ON-CALL",
            "day": "N/A",
            "time": "N/A"
        })
        return avails
    elif "PRODUCE MARKET" in job_name:
        for t in times:
            if "Morning" in t:
                job_name = "MARKET SET-UP"
                t = t.replace("MARKET SET-UP", "").strip()
            else:
                job_name = "PRODUCE POSSE"
                t = t.replace("PRODUCE POSSE", "").strip()
            avails.append({
                "job_name": job_name,
                "day": day,
                "time": t
            })
    elif "DONATION DRIVER" in job_name:
        for t in times:
            t = t.strip()
            if "on-call" in t.lower():
                day = "N/A"
                time = "On-Call"
            else:
                day = t[0:t.index(" ")]
                time = t[t.index(" "):].strip()

            avails.append({
                "job_name": job_name,
                "day": day,
                "time": time
            })

    # TODO - fix parsing logic
    elif "FRIDGE" in job_name:
        for t in times:
            t = t.strip()
            if "clean" in t:
                job_name = "STOCKING SQUAD"
                day  = t[0:t.index(" ")]
                time = t[t.index(" ")+1:]
            elif "on-call" in t.lower():
                job_name = "FRIDGE ON-CALL"
                day = "N/A"
                time = "On-Call"
            else:
                job_name = "CLEANUP CREW"
                day  = t[0:t.index(" ")]
                time = t[t.index(" ")+1:]

            avails.append({
                "job_name": job_name,
                "day": day,
                "time": time
            })
    else:
        for t in times:
            avails.append({
                "job_name": job_name,
                "day": day,
                "time": t
            })
    return avails
