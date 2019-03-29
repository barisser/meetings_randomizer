import operator
meetings_history = []
#meeting is just an array of employee strings length 4


def people_inputs():
    f = open('people.txt')
    data = f.readlines()
    peopledata = {}
    newcategory = False
    current_category = data[0].replace('\n', '')
    for i in range(1, len(data)-1):
        if data[i] == '\n' or i == 0:
            newcategory = True
            continue
        elif newcategory:
            newcategory = False
            current_category = data[i].replace('\n', '')
        else:
            person = data[i].replace('\n', '')
            peopledata[person] = current_category

    return peopledata


def compute_availability_once(name, peopledata, meetings_history):
    availability = []
    my_group = peopledata[name]
    for person in peopledata.keys():
        if peopledata[person] != my_group:
            availability.append(person)
    for meeting_cycle in meetings_history:
        for meeting in meeting_cycle:
            if name in meeting:
                for person in meeting:
                    if person in availability: #this is a hash in python
                        availability.remove(person)
    return availability


def compute_availabilities(peopledata, meetings_history):
    availabilities = {}
    availabilities_count = {}
    for person in peopledata.keys():
        availability = compute_availability_once(person, peopledata, meetings_history)
        availabilities[person] = availability
        availabilities_count[person] = len(availability)
    availabilities_count = sorted(availabilities_count.items(), key=operator.itemgetter(1))
    availabilities_dict = {}
    for x in availabilities_count:
        availabilities_dict[x[0]] = x[1]
    return availabilities, availabilities_count, availabilities_dict


def create_meeting(availabilities, availabilities_count, availabilities_dict, meeting_size=4):
    meeting = [availabilities_count[0][0]]
    while len(meeting) < meeting_size:
        meeting = add_to_meeting(availabilities, availabilities_count, availabilities_dict, meeting)
    return meeting


def who_is_eligible_to_join(availabilities, meeting, already_assigned):
    e = availabilities.keys()
    for person in meeting:
        e = [x for x in e if x in availabilities[person] and not x in already_assigned]
    return e


def who_should_join(availabilities_dict, availabilities, meeting, already_assigned):
    e = who_is_eligible_to_join(availabilities, meeting, already_assigned)
    e = [[x, availabilities_dict[x]] for x in e if x not in already_assigned]
    e = sorted(e, key=operator.itemgetter(1))
    e = e[0][0]
    return e


def increment_meeting(availabilities_dict, availabilities, meeting, already_assigned):
    try:
        newperson = who_should_join(availabilities_dict, availabilities, meeting, already_assigned)
    except:
        newperson = availabilities_dict.keys()[0]
        print "STUCK HAD TO CHOOSE ARBITRARY"
    meeting.append(newperson)
    return meeting, newperson


def create_meeting(availabilities_dict, availabilities, already_assigned, meeting_size=4):
    meeting = []
    while len(meeting) < meeting_size and len(availabilities_dict) > 0:
        meeting, newperson = increment_meeting(availabilities_dict, availabilities, meeting, already_assigned)
        already_assigned.append(newperson)
        del availabilities_dict[newperson]

    return meeting, already_assigned, availabilities_dict


def create_meeting_cycle(availabilities_dict, availabilities, meeting_size=4):
    meetings = []
    already_assigned = []
    total_people = len(availabilities_dict.keys())
    while len(already_assigned) < total_people:
        meeting, already_assigned, availabilities_dict = create_meeting(availabilities_dict, availabilities, already_assigned, meeting_size=meeting_size)
        meetings.append(meeting)
    return meetings


def meeting_cycle(meetings_history, people_data, meeting_size=4):
    availabilities, availabilities_count, adict = compute_availabilities(people_data, meetings_history)
    meetings = create_meeting_cycle(adict, availabilities)
    return meetings


def meetings_trajectory(cycles, meeting_size=4):
    people_data = people_inputs()
    meeting_history = []
    for _ in range(0, cycles):
        meetings = meeting_cycle(meeting_history, people_data, meeting_size=meeting_size)
        meeting_history.append(meetings)
    return meeting_history


def measure_violations(history, people_data):
    violations = 0
    previous_partners = {}
    for x in people_data.keys():
        previous_partners[x] = []
    for meeting_cycle in history:
        for meeting in meeting_cycle:
            for i in range(0, len(meeting)):
                persona = meeting[i]
                for j in range(i+1, len(meeting)):
                    personb = meeting[j]
                    if personb in previous_partners[persona]:
                        violations += 1
                        print "VIOLATION: {0} has already met with {1}".format(persona, personb)
                    else:
                        previous_partners[persona] = personb
                        previous_partners[personb] = persona
                    if people_data[persona] == people_data[personb]:
                        violations += 1
                        print "VIOLATION: {0} and {1} are in the same group".format(persona, personb)
    return violations
