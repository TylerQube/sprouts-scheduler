from openpyxl import Workbook
from openpyxl.styles import PatternFill
import math


def build_spreadsheet(shifts):
    wb = Workbook()
    ws = wb.active

    cafe_shifts = list(filter(lambda s: s.initiative == "SPROUTS CAFE HELPER", shifts))
    next_row = fill_cafe(cafe_shifts, wb)

    prep_shifts = list(filter(lambda s: s.initiative == "PREP", shifts))
    fill_prep(next_row, prep_shifts, wb)

    wb.save("output.xlsx")


def fill_cell(cell, color):
    cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")


def fill_prep(start_row, prep_shifts, wb):
    ws = wb.active
    row = start_row
    col = 1
    header = ws.cell(row, col)
    header.value = "PREP"
    for i in range(6):
        fill_cell(ws.cell(row, i + 1), "D684FF")
    row += 1

    # sort in grid order
    prep_shifts.sort(key=lambda s: (["mon", "tues", "wed", "thur", "sun"].index(s.day)))

    # fill header
    color = "E2A9FF"
    fill_cell(ws.cell(row, 1), color)
    for i in range(5):
        c = ws.cell(row, i + 2)
        fill_cell(c, color)
        c.value = ["Monday", "Tuesday", "Wednesday", "Thursday", "Sunday"][i]
    row += 1
    ws.cell(row, 1).value = "5pm-8pm"

    # fill in shifts
    color = "EBC3FF"
    for i in range(len(prep_shifts)):
        s = prep_shifts[i]
        print(s)
        print(s.volunteers)
        print()
        ws.cell(row, col).value = s.time
        for iv, v in enumerate(s.volunteers):
            c = ws.cell(row + iv, i + 2)
            c.value = v
            fill_cell(ws.cell(row + iv, i + 1), color)
            fill_cell(c, color)
    max_volunteers_in_row = len(
        max(prep_shifts, key=lambda s: len(s.volunteers)).volunteers
    )
    row += max_volunteers_in_row
    return row


# fill sheet with cafe helper shift assignments
# returns - row at bottom of filled shifts
def fill_cafe(cafe_shifts, wb):
    ws = wb.active
    row = 1
    col = 1
    header = ws.cell(row, col)
    header.value = "SPROUTS CAFE DAYTIME SHIFTS"

    # sort in grid order
    cafe_shifts.sort(
        key=lambda s: (
            ["9am-11am", "11am-1pm", "1-3pm", "3-5pm"].index(s.time),
            ["mon", "tues", "wed", "thur", "fri"].index(s.day),
        )
    )

    for i in range(4):
        ws.cell(2, (i + 1) * 2).value = ["Monday", "Tuesday", "Wednesday", "Thursday"][
            i
        ]
    for i in range(8):
        fill_cell(ws.cell(2, i + 1), "BBFFAC")
        fill_cell(ws.cell(1, i + 1), "9BFF84")

    # widen volunteer columns
    for l in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        ws.column_dimensions[l].width *= 1.5

    # fill in shifts
    colors = ["D8FFD0", "BBFFAC"]
    ci = 0
    row = 3
    for i in range(len(cafe_shifts) + 1):
        if i > 0 and i % 4 == 0 or i >= len(cafe_shifts):
            print(f"{i} moving row")
            max_volunteers_in_row = len(
                max(row_shifts, key=lambda s: len(s.volunteers)).volunteers
            )
            row += max_volunteers_in_row
            ci = (ci + 1) % 2
            if i >= len(cafe_shifts):
                break

        row_shifts = cafe_shifts[math.floor(i / 4) : math.floor(i / 4) + 4]

        s = cafe_shifts[i]
        print(f"[{row}, {col}]")
        print(s)
        print(s.volunteers)
        print()
        ws.cell(row, col).value = s.time
        for iv, v in enumerate(s.volunteers):
            c = ws.cell(row + iv, col + 1)
            c.value = v
            fill_cell(c, colors[ci])
            c = ws.cell(row + iv, col)
            fill_cell(c, colors[ci])

        col += 2
        col = (col - 1) % 8 + 1
    return row
