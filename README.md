Meeting Creator

Creates meetings with the following rules

People are divided into groups as specified in the people.txt file.

People are arranged into meetings of size X (default size=4).

The algorithm avoids placing people from the same group into the same
meeting.

It also avoids placing people who have already been in meetings together.

Each 'meeting cycle' is a set of meetings that includes every person specified
in the people.txt list.  The next meeting cycle should only begin when all
people have met.  Of course, one could rearrange the meetings that compose
a 'meeting cycle' into any order without introducing any constraint violations.

Generating a history generates a N meeting cycles.  

Typically constrain violations occur at the end of a meeting cycle where the algorithm
may be forced to make an arbitrary choice.  These violations can be measured
across an entire meetings history (set of meeting cycles) with the
measure_violations() method.

You should be able to fit several cycles with zero to no violations.

This is not an optimal solution but an algorithm that produces a good first-pass
outcome.  One could easily introduce swaps from the outcome of this algorithm
and iteratively measure total violations.

-- Description of the algorithm
  For each person calculate the number of people who are available to them given
  the current meetings history.  This is equivalent to the number of people for
  whom the person is available.  The 'scarcest' people, ie those available to
  the fewest people, are assigned first to meetings.  Of the people available to
  them, the scarcest of those are then added to the meeting.  After several are
  assigned, only those who are available to all current assignees (in a given
    meeting) are eligible for assignment.

  This way the most difficult people to place are placed first.  This is path dependent and doesn't
  look very far ahead.  It's a close enough solution.

-- To Run

import randomizer as r

people_data = r.people_inputs()

history = r.meetings_trajectory(3)    #for three cycles (meeting_size=4 is default but can be altered)

measure_violations(history, people_data)
