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
from functools import wraps

idcode = 0


def singleton(class_):
    instances = {}

    @wraps(class_)
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class Patient:
    def __init__(self, idcode, firstname, middlename, lastname, age, urgency):
        self.idcode = int(idcode)
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.age = int(age)
        self.urgency = int(urgency)

    def __lt__(self, other):
        return self.urgency < other.urgency

    def __iter__(self):
        return self

    def __next__(self):
        if parameter == self.age or self.idcode or self.urgency or self.lastname or self.firstname or self.middlename:
            raise StopIteration
        return parameter


@singleton
class WaitingList:

    def __init__(self):
        self.waitinglist = deque()

    def enqueue(self):
        global idcode
        global patient
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

    def dequeue(self):
        if len(self.waitinglist) == 0:
            return
        else:
            print(f"\nPatient ID {self.waitinglist[-1].idcode:05d} has been removed from the list!")
            sleep(1)
            return self.waitinglist.pop()

    def bribe(self):
        os.system('cls||clear')
        if waitinglist.__len__() == 0:
            main()
        bribe_list = []
        global parameter
        print(f"You currently have {waitinglist.__len__()} patients waiting for you.\n")
        waitinglist.__str__()
        parameter = input("\nWho do you wish to accept next, Doctor? ")

        if parameter.isnumeric():
            parameter = int(parameter)
        elif parameter == '':
            main()

        for element in vars(patient).keys():
            temp_bribe_list = [patient for patient in self.waitinglist if parameter == getattr(patient, element)]
            [bribe_list.append(item) for item in temp_bribe_list if item not in bribe_list]
        if len(bribe_list) == 1:
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

    def isempty(self):
        print("All the patients were asked to leave, Doctor!")
        sleep(1)
        self.waitinglist.clear()
        main()

    def universal_sorter(self, variable, bool):
        self.waitinglist = deque(sorted(self.waitinglist,
                                        key=lambda patient: getattr(patient, variable), reverse=bool))

    def __str__(self):
        for patient in reversed(self.waitinglist):
            print(f"ID:{patient.idcode:05d}  Urgency: {patient.urgency}  Age: {patient.age}  "
                  f"Name: {patient.firstname} {patient.middlename} {patient.lastname}")

    def __len__(self):
        return len(self.waitinglist)


def re_order_menu():
    print(f"You currently have {waitinglist.__len__()} patients waiting for you.\n")
    waitinglist.__str__()
    print("\nHow would you like to re-order the list, Doctor? ")
    print("\n1.Clear the room \n2.Sort by Urgency \n3.Sort by Urgency reversed \n4.Sort by ID \n5.Sort by ID reversed "
          "\n6.Sort by First name \n7.Sort by Middle name \n8.Sort by Last name \n9.Sort by Age youngest first "
          "\n10.Sort by Age oldest first \n11.Back")
    while True:
        try:
            reorder_menu_select = int(input("\nYour choice: "))
            if reorder_menu_select in range(1, 12):
                break
        except ValueError:
            print("\nPlease select a number from 1 to 11")
        else:
            print("\nPlease use a number from 1 to 11!")

    user_options = {
        1: waitinglist.isempty,
        2: ["urgency", False],
        3: ["urgency", True],
        4: ["idcode", True],
        5: ["idcode", False],
        6: ["firstname", True],
        7: ["middlename", True],
        8: ["lastname", True],
        9: ["age", True],
        10: ["age", False],
        11: main
    }
    if reorder_menu_select == 1:
        waitinglist.isempty()

    elif reorder_menu_select == 11:
        main()
    else:
        os.system('cls||clear')
        waitinglist.universal_sorter(user_options[reorder_menu_select][0], user_options[reorder_menu_select][1])
        re_order_menu()


def main():
    os.system('cls||clear')
    print(f"Welcome back, Doctor! \n\nYou currently have {waitinglist.__len__()} patients waiting for you.")
    waitinglist.__str__()
    print("\n\nWhat would you like to do? \n1.Add patient "
          "\n2.Take the next patient in list \n3.Re-order the list \n4.Accept a bribe \n5.Exit")
    while True:
        try:
            main_menu_select = int(input("\nYour choice: "))
            if main_menu_select in range(1, 6):
                break
        except ValueError:
            print("\nPlease use a number from 1 to 5!")
        else:
            print("\nPlease use a number from 1 to 5!")

    user_options = {
        1: waitinglist.enqueue,
        2: waitinglist.dequeue,
        3: re_order_menu,
        4: waitinglist.bribe,
        5: exit
    }
    os.system('cls||clear')
    user_options[main_menu_select]()
    main()


def start_program():
    global waitinglist
    waitinglist = WaitingList()
    main()


if __name__ == '__main__':
    start_program()
