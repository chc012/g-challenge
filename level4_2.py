import math
# a point should be a tuple (x, y), where x is the x coord and
# y the y coord.

def dist(a, b):
    # calculate the distance between two points
    return abs(a[0] - b[0])**2 + abs(a[1] - b[1])**2

def isclose(a, b, tol=1e-7):
    return abs(a - b) < tol

def create_bounds(dimensions):
    # create the walls based on the the dimension of the room
    # a bound should be a list of 2 points
    right_limit = dimensions[0]
    top_limit = dimensions[1]
    # get all 4 walls
    bottom = [(0, 0), (right_limit, 0)]
    top = [(0, top_limit), (right_limit, top_limit)]
    left = [(0, 0), (0, top_limit)]
    right = [(right_limit, 0), (right_limit, top_limit)]
    return [bottom, top, left, right]

def reflect_points(orig_source, orig_target, bounds, base_source, max_dist):
    # find reflections of point on all bounds
    reflections = set()
    for bound in bounds:
        if bound[0][0] == bound[1][0]:
            # a column wall
            new_source = (2*bound[0][0] - orig_source[0], orig_source[1])
            new_target = (2*bound[0][0] - orig_target[0], orig_target[1])
        else:
            # a row wall
            new_source = (orig_source[0], 2*bound[0][1] - orig_source[1])
            new_target = (orig_target[0], 2*bound[0][1] - orig_target[1])
        if dist(new_target, base_source) <= max_dist:
            reflections.add((new_source, new_target))
    return reflections

def find_reflections(dimensions, source, target, max_dist):
    # a bound should be a list of 2 points
    # bottom, top, left, right
    bounds = create_bounds(dimensions)
    reflection_pairs = { target: source }
    base_source = source
    # a stepwise creations of reflections, reflections of
    # reflections, etc.
    # each element in queue should be a pair of reflected
    # source and target
    queue = [ (source, target, distance) ]
    # If all reflections found in the last update exceed the
    # distance limit, we are ready to exit
    while queue:
        orig_source, orig_target = queue.pop(0)
        refl_pairs = reflect_points(orig_source, orig_target, bounds, base_source, max_dist)
        # discard if seen before
        refl_pairs = [[s, t] for [s, t] in refl_pairs
                      if t not in reflection_pairs]
        # check that reflections do not exceed distance
        refl_pairs = [
            [s, t] for [s, t] in refl_pairs
            if dist(source, t) <= max_dist
        ]
        # update queue and target-source dict
        if refl_pairs:
            new_queue += refl_pairs
            for [s, t] in refl_pairs:
                # this ensures that duplicates get merged
                reflection_pairs[t] = s

    # return the target-source dict
    return reflection_pairs

def on_beam_extension(source, close_target, far_target):
    angle1 = math.atan2(close_target[1] - source[1], close_target[0] - source[0])
    angle2 = math.atan2(far_target[1] - source[1], far_target[0] - source[0])
    if isclose(angle1, angle2) and dist(source, close_target) < dist(source, far_target):
        return True
    return False

def no_overlap(source, idx, reflected_targets):
    # if target at index idx in reflect_targets does not
    # form an line with source which pass any other point,
    # return True
    # else return False
    for i in range(len(reflected_targets)):
        if idx == i:
            continue
        if on_beam_extension(source,
                             reflected_targets[i],
                             reflected_targets[idx]):
            return False
    return True

def cannot_hit_self(source, reflected_source, reflected_target):
    # if reflected_source is not on the line between the
    # reflected_target and source, then return True
    # else return False
    if source == reflected_source:
        return True
    return not on_beam_extension(
        source, reflected_source, reflected_target)

def solution(dimensions, your_position, trainer_position, distance):
    source = tuple(your_position)
    target = tuple(trainer_position)
    max_dist = distance**2
    # if it is impossible to hit target directly, this means
    # our beam is too short, so we return 0.
    if dist(source, target) > max_dist:
        return 0
    # reflection_pairs: { reflected_target: reflected_source }
    # reflected_targets should be a set of the reflected trainer
    # point and
    # reflected points that satisfy the constraints that:
    # the distance between each point and my position should not
    # exceed max_distance.
    # reflected_sources should be their corresponding source
    # reflections for calculating if we will hit ourselves
    reflection_pairs = find_reflections(
        dimensions, source, target, max_dist)
    reflected_sources = list(reflection_pairs.values())
    reflected_targets = list(reflection_pairs.keys())
    # Check:
    # 1. the beam path to the point cannot hit another point
    # 2. the beam path to the point cannot hit myself
    targets = [
        i for i in range(len(reflected_targets))
        if no_overlap(source, i, reflected_targets)
    ]
    targets = [
        i for i in targets
        if cannot_hit_self(
            source,
            reflected_sources[i],
            reflected_targets[i]
        )
    ]
    # return the number of points that satisfies these constraints
    return len(targets)

if __name__ == "__main__":
    print(solution([3,2], [1,1], [2,1], 4)) # 7
    print(solution([300,275], [150,150], [185,100], 500)) # 9

    print(solution([2, 5], [1, 2], [1, 4], 11)) # 27
    print(solution([23, 10], [6, 4], [3, 2], 23)) # 8
    print(solution([1250, 1250], [1000, 1000], [500, 400], 10000)) # 196
    # print(solution([10, 10], [4, 4], [3, 3], 5000)) # 739323

    print(solution([3, 2], [1, 1], [2, 1], 7)) # 19
    print(solution([2, 3], [1, 1], [1, 2], 4)) # 7
    print(solution([3, 4], [1, 2], [2, 1], 7)) # 10
    print(solution([4, 4], [2, 2], [3, 1], 6)) # 7
    #print(solution([3, 4], [1, 1], [2, 2], 500)) # 54243
