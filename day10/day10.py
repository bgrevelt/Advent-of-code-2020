from collections import defaultdict
import datetime
def puzzle1(adapters):
     adapters = [0] + sorted(adapters)
     adapters.append(max(adapters) + 3)

     diffs = defaultdict(int)

     for i in range(1, len(adapters)):
         adapter_in = adapters[i - 1]
         adapter_out = adapters[i]

         diffs[adapter_out - adapter_in] += 1

     return diffs

# In this example, when using every adapter, there are 7 differences of 1 jolt and 5 differences of 3 jolts.
jolt_diffs = puzzle1([16,10,15,5,1,11,7,19,6,12,4])
assert jolt_diffs[1] == 7
assert jolt_diffs[3] == 5

example_input = [int(n) for n in '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
'''.splitlines()]
jolt_diffs = puzzle1(example_input)
#In this larger example, in a chain that uses all of the adapters, there are 22 differences of 1 jolt and 10 differences of 3 jolts.
assert jolt_diffs[1] == 22
assert jolt_diffs[3] == 10

jolt_diffs = puzzle1([int(n) for n in open('input.txt').readlines()])
print(f'The solution to puzzle 1 is {jolt_diffs[1] * jolt_diffs[3]}')



def possible_combinations(adapters, tail = 0):
    options = [adapter for adapter in adapters if adapter > tail and adapter <= tail +3]
    if len(options) == 0:
        # tail was a leaf
        return [[tail]]
    else:
        # we are at a branch
        r = []
        for option in options:
            new_adapters = [n for n in adapters]
            new_adapters.remove(option)

            for end in possible_combinations(new_adapters, option):
                r.append([tail] + end)

        return r


combinations = possible_combinations([16,10,15,5,1,11,7,19,6,12,4,22])
# The first example above (the one that starts with 16, 10, 15) supports the following arrangements:
# (0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
assert [0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22] in combinations
# (0), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
assert [0, 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, 22] in combinations
# (0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
assert [0, 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, 22] in combinations
# (0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
assert [0, 1, 4, 5, 7, 10, 12, 15, 16, 19, 22] in combinations
# (0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
assert [0, 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, 22] in combinations
# (0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
assert [0, 1, 4, 6, 7, 10, 12, 15, 16, 19, 22] in combinations
# (0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
assert [0, 1, 4, 7, 10, 11, 12, 15, 16, 19, 22] in combinations
# (0), 1, 4, 7, 10, 12, 15, 16, 19, (22)
assert [0, 1, 4, 7, 10, 12, 15, 16, 19, 22] in combinations

# Well that was nice... But that doesn't scale well it seems. So let's stick to counting

leafs_per_node = {}

def get_leafs(node, graph):
    # use cache to speed things up considerably
    global leafs_per_node

    if node in leafs_per_node:
        return leafs_per_node[node]
    elif len(graph[node]) == 0:
        return 1
    else:
        leafs = sum([get_leafs(n,graph) for n in graph[node]])
        leafs_per_node[node] = leafs
        return leafs



def puzzle2(adapters):
    #clear cache
    global leafs_per_node
    leafs_per_node = {}

    adapters = [0] + adapters + [max(adapters)+3]
    graph = {adapter: [a for a in adapters if a > adapter and a <= adapter + 3] for adapter in adapters}
    return get_leafs(0, graph)

#In total, this set of adapters can connect the charging outlet to your device in 19208 distinct arrangements.
assert puzzle2(example_input) == 19208

print(f"The solution to puzzle 2 is {puzzle2([int(n) for n in open('input.txt').readlines()])}")