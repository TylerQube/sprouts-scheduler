import file_loader
import volunteer
import sheet_builder
import time

shift_path = "shifts.yaml"


def schedule_volunteers(
    shifts, volunteers, v_index, cur_schedule, best_schedule, start_time
):
    if time.time() - start_time > 0.3:
        return
    # if len(cur_schedule) + len(volunteers) - v_index <= len(best_schedule):
    #     return
    # print(f'{v_index}: {cur_schedule}')
    if v_index == len(volunteers):
        if len(cur_schedule) > len(best_schedule):
            best_schedule.clear()
            best_schedule.extend(cur_schedule)
        return

    v = volunteers[v_index]

    is_assigned = False
    for index in sorted(range(len(shifts)), key=lambda i: shifts[i].num_available):
        shift = shifts[index]
        if id(shift) not in v.availability or not shift.add_volunteer(v.name):
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


def run_scheduler(shifts, vollies):
    num_spaces = 0
    for shift in shifts:
        num_spaces += shift.capacity
    shifts.sort(key=lambda s: s.num_available, reverse=False)

    print("Scheduling volunteers...")
    schedule = []
    start = time.time()
    schedule_volunteers(shifts, vollies, 0, [], schedule, time.time())
    print(f"{len(schedule)} / {len(vollies)} scheduled")
    print(f"{len(schedule)} / {num_spaces} positions filled")
    print(f"Schedule generated in: {time.time() - start}")

    for pair in schedule:
        # print(f'{pair[0]}: {pair[1]}')
        pair[1].add_volunteer(pair[0])


def main():
    with open("sprouts.logo", "r") as logo:
        data = logo.read()
        print(data)
    print("Welcome to the Sprout-o-Matic Shift Scheduler!", "\n")
    form_data = file_loader.get_file()

    print("Loading shifts...")
    yaml = file_loader.load_yaml(shift_path)
    shifts = file_loader.parse_shifts(yaml)

    vollies = volunteer.load_volunteers(form_data, shifts)

    vollies = list(filter(lambda v: (len(v.availability) > 0), vollies))

    run_scheduler(shifts, vollies)

    unique_volunteers = set()
    for s in shifts:
        for v in s.volunteers:
            unique_volunteers.add(v)

    sheet_builder.build_spreadsheet(shifts)


main()
