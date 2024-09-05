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



    # TODO - Add support for stocking squad shifts (uses different google form name syntax)
    def load_availability(self, form, shifts):
        for column, value in form.items():
            if type(value) == float or "available" not in column:
                continue

            availables = available_from_form_column(column, value)
            for a in availables:
                times = a["times"]
                job_name = a["job_name"]
                day = a["day"]

                for t in times:
                    t = t.replace(" ", "")
                    for s in shifts:

                        # special syntax handling
                        if "SET-UP SQUAD" in s.initiative and "SET-UPSQUAD" in t:
                            t = t.replace("SET-UPSQUAD", "")

                        print(f"{day.lower()} {s.day}")
                        if (
                            job_name != s.initiative
                            or len(day) > 0
                            and s.day.lower() not in day.lower()
                            or t != s.time
                        ):
                            continue
                        # add to availability
                        s.num_available += 1
                        self.availability.append(id(s))


def load_volunteers(table, shifts):
    vollies = []
    for index, row in table.iterrows():
        # if index != 0:
        #     continue
        vol = Volunteer(
            row["Name"],
            row["Email"],
            row["Phone Number"],
            row["Are you a returning volunteer?"] == "Yeah I am!",
        )

        # if duplicate entry, use most recent form submission
        existing = next(
            (v for v in vollies if v.name == vol.name and v.email == v.email), None
        )
        if existing:
            vollies.remove(existing)

        vol.load_availability(row, shifts)

        vollies.append(vol)

    return vollies

def available_from_form_column(column, value):
    avails = []
    times = value.split(",")
    job_name = column[4 : column.index(",")]
    day = (
        column[column.index(":") + 1 : :]
        .strip()
        .replace("[", "")
        .replace("]", "")
    )

    if "PRODUCE MARKET" in job_name:
        for t in times:
            if "SET-UP" in t:
                job_name = "SET-UP SQUAD"
                t = t.replace("SET-UP SQUAD", "").strip()
            else:
                job_name = "PRODUCE POSSE"
                t = t.replace("PRODUCE POSSE", "").strip()
            avails.append({
                "job_name": job_name,
                "day": day,
                "times": [t]
            })
    elif "DONATION DRIVER" in job_name:
        for t in times:
            t = t.strip()
            if "on-call" in t.lower():
                day = "N/A"
                time = "On-Call"
            else:
                time = t[0:t.index(" ")]
                day = t[t.index(" "):].strip()

            avails.append({
                "job_name": job_name,
                "day": day,
                "times": [time]
            })
    elif "CLEANUP CREW" in job_name or "STOCKING SQUAD" in job_name:
        for t in times:
            if "on-call" in t.lower():
                day = "N/A"
                time = "On-Call"
            else:
                day  = t[0:t.index(" ")-1]
                time = t[t.index(" ")+1:]
            avails.append({
                "job_name": job_name,
                "day": day,
                "times": [time]
            })
    else:
        avails.append({
            "job_name": job_name,
            "day": day,
            "times": times
        })
    return avails
