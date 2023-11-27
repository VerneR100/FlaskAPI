from app import app, DATA, models
from flask import request, Response
import json


@app.post("/users/create")
def creating_new_users():
    data = request.json
    if not (models.User.is_valid_email(data["email"])):
        return Response(status=400)
    user = models.User(
        data["first_name"], data["last_name"], data["email"], data["sport"]
    )
    DATA["users"].append(user)
    response = Response(user.response(), status=200, mimetype="application/json")
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    for user in DATA["users"]:
        if user.id == user_id:
            return Response(user.response(), status=200, mimetype="application/json")
    return Response(status=400)


@app.post("/contests/create")
def create_new_contest():
    data = request.json
    contest = models.Contest(data["name"], data["sport"], data["participants"])
    users_id = data["participants"][:]
    # У нас есть список участников и нужно у каждого user обновить список contests
    for user in DATA["users"]:
        for user_id in users_id:
            if user.id == user_id:
                user.add_contest(contest.id)
                users_id.remove(user_id)
                break
    DATA["contests"].append(contest)
    return Response(contest.response(), status=200, mimetype="application/json")


@app.get("/contests/<int:contest_id>")
def get_contest(contest_id):
    data = request.json
    for contest in DATA["contests"]:
        if contest.id == contest_id:
            return Response(contest.respons(), status=200, mimetype="application/json")

    return Response(status=400)


@app.post("/contests/<int:contest_id>/finish")
def finish_contest(contest_id):
    winner = request.json["winner"]
    for contest in DATA["contests"]:
        if contest.id == contest_id:
            contest.finish_contest(winner)
            return Response(contest.response(), status=200, mimetype="application/json")
    return Response(status=400)


@app.get("/users/<int:user_id>/contests")
def get_contests_user(user_id):
    contests = list()
    response = {"contests": list()}
    for user in DATA["users"]:
        if user.id == user_id:
            contests = user.contests
            break
    for contest in DATA["contests"]:
        if contest.id in contests:
            response["contests"].append(contest.data())
            contests.remove(contest.id)
    return Response(json.dumps(response), status=200, mimetype="application/json")


@app.get("/users/leaderboard")
def sorted_list_of_users():
    type_response = request.json["type"]
    # ! проверить что будет если не был передан в теле запроса атрибут 'sort'
    type_of_sorting = request.json["sort"]
    result = models.User.leaderboard(DATA["users"], type_of_sorting)
    if type_response == "list":
        return Response(
            json.dumps({"users": [user.data() for user in result]}),
            200,
            mimetype="application/json",
        )
    elif type_response == "graph":
        models.User.creating_graph(result)
        html_form = '<img src="graph.png>'
        return Response(html_form, 200, mimetype="text/html")
    return Response(status=400)
