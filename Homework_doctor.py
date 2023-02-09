"""
Imagine you have a queue of people who are registered to see the doctor.
This queue will not contain a day or time of visit it is purely based on order.
New people are added to the end of this queue and the first person in the queue
is accepted for the visit when doctor calls in next person comes.

Each patient should have sufficient data about them, so it would be possible to find them if needed,
PatientID(5 integer digits), FirstName(String), MiddleName(String/Optional) LastName(String),
Age(Integer), Urgency(1,2 or 3 where 1 is least urgent and 3 most urgent)

The Doctor can be corrupt, considerate and on certain occasions weird, thus he needs to be able to:
- Invite a certain patient in without him waiting in line,
- Since we do not know what is the illness of the patient, after the bribe is received,
we should be able to accept this patient based on any unique data we have about him.
- Re-order the queue based on urgency
- Re-order the queue based on any parameter the patients have.

Common info:
Interaction with the program should be done in a way of user keyboard inputs, given that the doctor is quite chaotic,
the more informative and easy to use console communication will be the better
"""
import os
import bisect
from collections import deque
from time import sleep

idcode = 0
patient = None
user_input = None


class Patient:
    def __init__(self, idcode_, firstname, middlename, lastname, age, urgency):
        self.idcode = int(idcode_)
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.age = int(age)
        self.urgency = int(urgency)

    def __lt__(self, other):  # Default list sorter by urgency.
        return self.urgency < other.urgency


class WaitingList:

    def __init__(self):
        self.waitinglist = deque()

    def enqueue(self):  # Add new patient
        global idcode  # Store as global variable to ensure unique value for each patient.
        global patient  # Object 'patient' is used in method 'bribe()' and needs to be defined globally.
        print("Patient information sheet!\n")
        idcode += 1
        first_name = input("First name: ")
        middle_name = input("Middle name: ")
        last_name = input("Last name: ")
        while True:
            try:
                age = int(input("Age: ") or 0)
                break
            except ValueError:
                print("\nPlease select a number")

        while True:
            try:
                urgency = int(input("Urgency (1- low, 2- medium, 3- high): ") or 1)
                if urgency in range(1, 4):
                    break
            except ValueError:
                print("\nPlease select a number from 1 to 3")
            else:
                print("\nPlease use a number from 1 to 3!")

        patient = Patient(idcode, first_name, middle_name, last_name, age, urgency)
        print(f"\nPatient ID {idcode:05d} has been added to the list!")
        sleep(1)
        return bisect.insort_left(self.waitinglist, patient)

    def dequeue(self):  # Remove next patient from waitinglist
        if len(self.waitinglist) == 0:
            return
        else:
            print(f"\nPatient ID {self.waitinglist[-1].idcode:05d} has been removed from the list!")
            sleep(1)
            return self.waitinglist.pop()

    def bribe(self):
        if len(waitinglist) == 0:  # Check if there are any patients, return to main menu if none.
            main()

        os.system('cls||clear')
        bribe_list = []
        global user_input  # Variable user_input is used in class 'Patient' iterator and has to be globally accessible.

        print(f"You currently have {len(waitinglist)} patients waiting for you.\n")
        waitinglist.__str__()

        user_input = input("\nWho do you wish to accept next, Doctor? ")

        if user_input.isnumeric():
            user_input = int(user_input)  # Redefine numerical inputs as integers.
        elif user_input == '':  # In case of no data input, return to main menu.
            main()

        for element in vars(patient).keys():  # Iterate through waitinglist by attributes and check for user input.
            temp_bribe_list = [patient_ for patient_ in self.waitinglist if user_input == getattr(patient_, element)]
            [bribe_list.append(item) for item in temp_bribe_list if item not in bribe_list]  # Avoid repetitions

        if len(bribe_list) == 1:  # This 'if' block defines output of the bribe() method.
            print(f"Patient {bribe_list[0].idcode:05d} has been removed from the list")
            self.waitinglist.remove(bribe_list[0])
            sleep(2)
        elif len(bribe_list) == 0:
            print("\nThere are no patients with requested identifiers!")
            sleep(2)
            waitinglist.bribe()
        else:
            print(f"\nThere are several patients with this data, be more specific!\n")
            for count, _ in enumerate(bribe_list):
                print(f"ID:{bribe_list[count].idcode:05d}")
            sleep(3)
            waitinglist.bribe()

    def isempty(self):  # Empty the waitinglist.
        print("All the patients were asked to leave, Doctor!")
        sleep(1)
        self.waitinglist.clear()
        main()

    def universal_sorter(self, attribute, reverse):  # Sort the waitinglist.
        self.waitinglist = deque(sorted(self.waitinglist,
                                        key=lambda patient_: getattr(patient_, attribute), reverse=reverse))

    def __str__(self):  # print Patient objects in waitinglist.
        for patient_ in reversed(self.waitinglist):
            print(f"ID:{patient_.idcode:05d}  Urgency: {patient_.urgency}  Age: {patient_.age}  "
                  f"Name: {patient_.firstname} {patient_.middlename} {patient_.lastname}")

    def __len__(self):
        return len(self.waitinglist)


def re_order_menu():
    if len(waitinglist) == 0:  # Check if there are any patients, return to main menu if none.
        main()

    print(f"You currently have {len(waitinglist)} patients waiting for you.\n")  # Reorder menu prints.
    waitinglist.__str__()
    print("\nHow would you like to re-order the list, Doctor? ")
    print("\n1.Clear the room \n2.Sort by Urgency \n3.Sort by Urgency reversed \n4.Sort by ID \n5.Sort by ID reversed "
          "\n6.Sort by First name \n7.Sort by Middle name \n8.Sort by Last name \n9.Sort by Age youngest first "
          "\n10.Sort by Age oldest first \n11.Back")

    while True:  # Safenet for execution integrity in case of invalid input data.
        try:
            value = int(input("\nYour choice: "))
            if value in range(1, 12):
                break
        except ValueError:
            print("\nPlease select a number from 1 to 11")
        else:
            print("\nPlease select a number from 1 to 11")

    user_command = {  # Dictionary of user commands.
        2: ["urgency", False],
        3: ["urgency", True],
        4: ["idcode", True],
        5: ["idcode", False],
        6: ["firstname", True],
        7: ["middlename", True],
        8: ["lastname", True],
        9: ["age", True],
        10: ["age", False]
    }
    if value == 1:  # This 'if' block is to execute user command
        waitinglist.isempty()

    elif value == 11:
        main()
    else:
        os.system('cls||clear')  # Call: object.method(arg1, arg2) where arg1 and arg2 are defined in dictionary.
        waitinglist.universal_sorter(user_command[value][0], user_command[value][1])
        re_order_menu()  # Update prints and reset value, only way out of menu is by user command.


def main():
    os.system('cls||clear')  # Main menu prints
    print(f"Welcome back, Doctor! \n\nYou currently have {len(waitinglist)} patients waiting for you.")
    waitinglist.__str__()
    print("\n\nWhat would you like to do? \n1.Add patient "
          "\n2.Take the next patient in list \n3.Re-order the list \n4.Accept a bribe \n5.Exit")

    while True:  # Safenet for execution integrity in case of invalid input data.
        try:
            value = int(input("\nYour choice: "))
            if value in range(1, 6):
                break
        except ValueError:
            print("\nPlease use a number from 1 to 5!")
        else:
            print("\nPlease use a number from 1 to 5!")

    user_command = {  # Dictionary of user commands.
        1: waitinglist.enqueue,
        2: waitinglist.dequeue,
        3: re_order_menu,
        4: waitinglist.bribe,
        5: exit
    }
    os.system('cls||clear')
    user_command[value]()  # Execute user command
    main()  # Update prints and reset value, only way out of code execution is by exit command


if __name__ == '__main__':
    waitinglist = WaitingList()
    main()
