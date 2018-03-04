import heapq


def findMutationDistance(start, end, bank):
    if start == end:
        return 0
    if start != end and len(bank) == 0:
        return -1
    if len(start) != len(end):
        return -1

    mutations_all = bank

    # checks difference between two strings, I need 1 for path
    mutation_distance = lambda l1, l2: len(start) - len([1 for a, b in zip(l1, l2) if a == b])

    if start not in bank:
        mutations_all.insert(0, start)

    distances_form_start = [-1 for i in mutations_all]
    canditate_for_mutation = []
    for i in range(len(mutations_all)):
        if mutations_all[i] == start:
            distances_form_start[i] = 0
            heapq.heappush(canditate_for_mutation, (0, [start, i]))  # nodes to visit requeres: (string, position in the all_strings array)
            break

    while len(canditate_for_mutation) != 0:
        _, next = heapq.heappop(canditate_for_mutation)
        for z in range(len(mutations_all)):
            if mutation_distance(mutations_all[z], next[0]) == 1 and distances_form_start[z] == -1:
                dist = distances_form_start[next[1]] + 1
                distances_form_start[z] = dist  # updates distance to start
                check = mutations_all[z]
                if check == end:
                    return dist  # eventually end is here, otherwise will return -1
                genetic_dist = mutation_distance(check, end)
                heapq.heappush(canditate_for_mutation, (genetic_dist, [check, z]))
    return -1




