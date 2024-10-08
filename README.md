# Sprout-o-Matic Shift Scheduler

## Usage

The Sprout-o-matic scheduler receives a CSV file of volunteer availability, schedules volunteers according to availability, and outputs a formatted Excel spreadsheet containing shift assignments.

Please contact Tyler with any issues, program is a bit finicky at the moment

## Functionality
- Volunteers priority is given in order of form submission
- Volunteers cannot be double-booked for timed shifts (e.g. cafe, produce market)
- Volunteers can be double booked for "On-Call" positions (e.g. donation driver, fridge)
- If there aren't enough volunteers to fill all shifts, the scheduler attempts to evenly distribute volunteers as much as possible


## Run Locally

Clone the project

```bash
  git clone https://github.com/TylerQube/sprouts-scheduler.git
```

Go to the project directory

```bash
  cd sprouts-scheduler
```

Install dependencies (optionally in a virtual environment)

```bash
  python -m venv venv
  pip install -r requirements.txt
```

Run the program

```bash
  python schedule.py
```

## To-Do
- Provide executable files to run on various platforms without project setup
- Overhaul availability system to remove need for shift YAML file
