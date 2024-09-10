import file_loader
import volunteer
import sheet_builder
import time
from shift import Shift

shift_path = "shifts.yaml"


MAX_TIME = 5.0
def schedule_volunteers(
    shifts, volunteers, v_index, cur_schedule, best_schedule, start_time
):
    if time.time() - start_time > MAX_TIME:
        return

    if v_index == len(volunteers):
        if len(cur_schedule) > len(best_schedule):
            best_schedule.clear()
            best_schedule.extend(cur_schedule)
        return

    v = volunteers[v_index]

    is_assigned = False
    weight_availability = 0.0
    weight_fillrate = 1.0
    def sort_score(shift):
        num_avail = shift.num_available
        avail_heuristic = num_avail
        fill_heuristic = len(shift.volunteers) / shift.capacity
        return (avail_heuristic * weight_availability) + (fill_heuristic * weight_fillrate)
    sorted_shifts = sorted(range(len(shifts)), key=lambda i: sort_score(shifts[i])) 
    for index in sorted_shifts:
        shift = shifts[index]

        # skip on-call shifts, save for second pass because can be double-booked
        if "on-call" in shift.time.lower() or "on-call" in shift.day.lower() or "on-call" in shift.initiative.lower():
            continue
        match = False
        if shift in v.availability and shift.add_volunteer(v.name):
            match = True
        if not match:
            continue
        cur_schedule.append((v.name, shift))
        schedule_volunteers(
            shifts, volunteers, v_index + 1, cur_schedule, best_schedule, start_time
        )
        shift.remove_volunteer(v.name)
        cur_schedule.pop()
        is_assigned = True

    if not is_assigned:
        schedule_volunteers(
            shifts, volunteers, v_index + 1, cur_schedule, best_schedule, start_time
        )

def schedule_on_call(shifts, volunteers):
    for v in volunteers:
        for s in shifts:
            if "on-call" not in s.time.lower() and "on-call" not in s.initiative.lower():
                continue
            if len(s.volunteers) >= s.capacity:
                continue
            if s in v.availability:
                s.add_volunteer(v.name)


def run_scheduler(shifts, vollies):
    shifts.sort(key=lambda s: s.num_available, reverse=False)

    print("Scheduling volunteers...")
    schedule = []
    start = time.time()
    schedule_volunteers(shifts, vollies, 0, [], schedule, time.time())
    for pair in schedule:
        for s in shifts:
            if s == pair[1]:
                pair[1].add_volunteer(pair[0])
    schedule_on_call(shifts, vollies)

    timed_shift_volunteers = set()
    all_volunteers = set()
    num_timed_filled_positions = 0
    num_all_filled_positions = 0
    num_timed_spaces = 0
    num_total_spaces = 0
    for s in shifts:
        for v in s.volunteers:
            if s not in next((vo for vo in vollies if vo.name == v), None).availability:
                raise Exception("Scheduled volunteer outside of availability")

        on_call = "on-call" in s.initiative.lower() or "on-call" in s.day.lower() or "on-call" in s.time.lower() 
        all_volunteers.update(s.volunteers)
        num_total_spaces += s.capacity
        num_all_filled_positions += len(s.volunteers)
        if not on_call:
            timed_shift_volunteers.update(s.volunteers)
            num_timed_spaces += s.capacity
            num_timed_filled_positions += len(s.volunteers)

    assert len(timed_shift_volunteers) == num_timed_filled_positions


    print(f"Schedule generated in: {time.time() - start}")
    print(f"{len(timed_shift_volunteers)} / {len(vollies)} volunteers scheduled for timed shifts")
    print(f"{len(all_volunteers)} / {len(vollies)} volunteers scheduled for any shift (including on-call)")
    print(f"{num_timed_filled_positions} / {num_timed_spaces} timed positions filled")
    print(f"{num_all_filled_positions} / {num_total_spaces} of all positions filled (including on-call)")
    print()
    
    for v in vollies:
        if v.name not in all_volunteers:
            print(f"{v.name} not scheduled")
    print()



shift_capacity = {
    "SPROUTS CAFE HELPER": {
        "9am-11am": 6,
        "11am-1pm": 6,
        "1pm-3pm": 6,
        "3pm-5pm": 5
    },
    "PREP": 6,
    "COMMUNITY EATS SERVER": 7,
    #MARKET
    "MARKET SET-UP": 2,
    "PRODUCE POSSE": 2,
    #DRIVER
    "DONATION DRIVER": 2,
    # FRIDGE
    "STOCKING SQUAD": 2,
    "CLEANUP CREW": 2,
    "ON-CALL": 20
}
def get_shift_capacity(initiative, day, time):
    if "on-call" in initiative.lower():
        return 50

    if "on-call" in time.lower() or "n/a" in day.lower():
        return shift_capacity["ON-CALL"]
    if "cafe" in initiative.lower():
        return shift_capacity["SPROUTS CAFE HELPER"][time.lower()]
    else:
        return shift_capacity[initiative]

def main():
    with open("sprouts.logo", "r") as logo:
        data = logo.read()
    print("Welcome to the Sprout-o-Matic Shift Scheduler!", "\n")
    form_data = file_loader.get_file()

    vollies = volunteer.load_volunteers(form_data)

    print("Loading shifts...")
    shifts = set()
    for v in vollies:
        for ia, a in enumerate(v.availability):
            job = a["job_name"].strip()
            day = a["day"].strip()
            time = a["time"].strip()
            if " - " in time or " -" in time or "- " in time or " " in time and "(" not in time:
                time = time.replace(" - ", "-")
                time = time.replace(" -", "-")
                time = time.replace("- ", "-")
            s = Shift(
                job,
                day,
                time,
                get_shift_capacity(job, day, time)
            )
            if s in shifts:
                for es in shifts:
                    if s == es:
                        es.num_available += 1
            else:
                s.num_available += 1
                shifts.add(s)
            v.availability[ia] = s
    vollies = list(filter(lambda v: (len(v.availability) > 0), vollies))
    shifts = list(shifts)


    run_scheduler(shifts, vollies)

    # verify unique volunteers

    sheet_builder.build_spreadsheet(shifts)
    print("Spreadsheet generated")
    print("Scheduling complete!")


main()
