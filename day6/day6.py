class Group:
    def __init__(self, text):
        self._persons = [Person(line) for line in text.splitlines() if line.strip()]

    # All questions positively answered by at least member of the group
    def positively_answered_questions(self):
        return {q for p in self._persons for q in p.positively_answered_questions}

    def questions_everyone_answered_positively(self):
        return set.intersection(*[p.positively_answered_questions for p in self._persons])

class Person:
    def __init__(self, text):
        self.positively_answered_questions = {question for question in text.strip()}

qs = Group('''abcx
abcy
abcz''').positively_answered_questions()
assert all(q in qs for q in "abcxyz")
#In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the same question don't count extra; each question counts at most once.)

def get_groups(text):
    return [Group(group_text) for group_text in text.split('\n\n')]

groups = get_groups('''abc

a
b
c

ab
ac

a
a
a
a

b''')
# This list represents answers from five groups:
assert len(groups) == 5
# The first group contains one person who answered "yes" to 3 questions: a, b, and c.
assert all(q in groups[0].positively_answered_questions() for q in "abc")
# The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
assert all(q in groups[1].positively_answered_questions() for q in "abc")
# The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
assert all(q in groups[2].positively_answered_questions() for q in "abc")
# The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
assert all(q in groups[3].positively_answered_questions() for q in "a")
# The last group contains one person who answered "yes" to only 1 question, b.
assert all(q in groups[4].positively_answered_questions() for q in "b")

def puzzle1(text):
    return sum([len(group.positively_answered_questions()) for group in get_groups(text)])

# In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.
assert puzzle1('''abc

a
b
c

ab
ac

a
a
a
a

b''') == 11

input = open('input.txt').read()
print(f'The solution to puzzle 1 is {puzzle1(input)}')

def puzzle2(text):
    return sum([len(group.questions_everyone_answered_positively()) for group in get_groups(text)])

print(f'The solution to puzzle 2 is {puzzle2(input)}')