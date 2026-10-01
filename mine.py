import time
from adapter import Solver, cost_of


SAFETY_S = 0.25


def improve_by_insertion(instance, order, end_time):
    order = list(order)
    best_cost = cost_of(instance, order)

    improved = True

    while improved and time.perf_counter() < end_time:
        improved = False

        for i in range(len(order)):

            if time.perf_counter() >= end_time:
                break

            batch = order.pop(i)

            best_position = i
            local_best = best_cost

            for j in range(len(order) + 1):

                order.insert(j, batch)

                cost = cost_of(instance, order)

                if cost < local_best:
                    local_best = cost
                    best_position = j

                order.pop(j)

                if time.perf_counter() >= end_time:
                    break

            order.insert(best_position, batch)

            if local_best < best_cost:
                best_cost = local_best
                improved = True

        if not improved:
            break

    return order, best_cost


class MySolver(Solver):

    def solve(self, instance, submit_candidate):

        start_time = time.perf_counter()

        # Initial solution: earliest due date
        order = sorted(
            range(instance.size),
            key=lambda b: (instance.due[b], b)
        )

        end_time = start_time + 4.5

        # Improve using insertion moves
        order, best_cost = improve_by_insertion(
            instance,
            order,
            end_time
        )

        submit_candidate({"order": order})

        return {"order": order}
