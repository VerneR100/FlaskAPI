import matplotlib.pyplot as plt


def graph(users):
    fix, ax = plt.subplots()
    users = [f"{user.first_name} {user.last_name}" for user in result]
    users_pos = list(range(1, len(users) + 1))
    number_of_contsts = [len(user.contests) for user in result]
    ax.barh(users_pos, number_of_contsts, align="center")
    ax.set_yticks(users_pos, labels=users)
    ax.invert_yaxis()
    ax.set_xlabel("Number of contests")
    ax.set_title("User schedule by number of competitions")

    plt.savefig("graph.png")
