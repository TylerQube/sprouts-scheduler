import file_loader        

shift_path = "shifts.yaml"
def main():
    # with open('sprouts.logo', 'r') as logo:
    #     data = logo.read()
    #     print(data)
    # print("Welcome to the Sprout-o-Matic Shift Scheduler!", "\n")
    # file = file_loader.get_file()
    # print("File loaded!") 
    
    print("Loading shifts...")
    yaml = file_loader.load_yaml(shift_path) 
    print(yaml)
    shifts = file_loader.parse_shifts(yaml)
    for shift in shifts:
        print(shift, "\n")

main()