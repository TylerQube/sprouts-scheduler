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
            times = value.split(",")
            job_name = column[4 : column.index(",")]
            day = (
                column[column.index(":") + 1 : :]
                .strip()
                .replace("[", "")
                .replace("]", "")
            )
            for i, time in enumerate(times):
                times[i] = time.replace(" ", "")

            for t in times:
                for s in shifts:
                    if (
                        job_name != s.initiative
                        or len(day) > 0
                        and s.day not in day.lower()
                        or t != s.time
                    ):
                        continue
                    # add to availability
                    s.num_available += 1
                    self.availability.append(id(s))


def load_volunteers(table, shifts):
    vollies = []
    for index, row in table.iterrows():
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
