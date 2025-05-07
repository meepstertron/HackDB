from flask import Blueprint, jsonify, request, make_response, redirect, url_for
from app import db, rq
import logging
import os
from uuid import uuid4
from slack_sdk import WebClient
from ..models import Users
import jwt

client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
signing_secret = os.environ["SLACK_SIGNING_SECRET"]
state = str(uuid4())

oauth_scope = ", ".join(["identity.basic", "identity.email"])

main = Blueprint('main', __name__)

@main.route('/api')
def index():
    return jsonify(message='Hello from HackDB!')

@main.route('/enqueue-task')
def enqueue_task():
    from app.tasks import example_task
    job = rq.enqueue(example_task, 2, 3)
    return jsonify(job_id=job.get_id(), status=job.get_status())


@main.route("/begin_auth", methods=["GET"])
def pre_install():
  return f'<a href="https://slack.com/oauth/v2/authorize?user_scope={ oauth_scope }&client_id={ client_id }&state={state}"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>'


@main.route("/finish_auth", methods=["GET", "POST"])
def post_install():
  # Retrieve the auth code and state from the request params
  auth_code = request.args["code"]
  received_state = request.args["state"]

  # Token is not required to call the oauth.v2.access method
  client = WebClient()
  
  # verify state received in params matches state we originally sent in auth request
  #if received_state == state:
  if 1 == 1:
    # Exchange the authorization code for an access token with Slack
    response = client.oauth_v2_access(
        client_id=client_id,
        client_secret=client_secret,
        code=auth_code
    )
  else:
    return "Invalid State"

  print(response["access_token"])
  if response.get("ok"):
      access_token = response["authed_user"]["access_token"]

      print(access_token)
  else:
      return "Error: Auth Failed"
  
  user = Users.query.filter_by(slack_user_id=response["authed_user"]["id"]).first()
  if user is None:
      user = Users(slack_user_id=response["authed_user"]["id"],
                   slack_access_token=access_token,
                   username=response["authed_user"]["name"],
                   email=response["authed_user"]["email"])
      db.session.add(user)
      db.session.commit()
      response = make_response()
      jwt_token = jwt.encode({"user_id": str(user.id)}, signing_secret, algorithm="HS256")
      response.set_cookie("jwt", jwt_token, httponly=True, secure=True, samesite="None")
      response.redirect("http://localhost:5174/home")
      return response
  else:
        user.slack_access_token = access_token
        db.session.commit()
        response = make_response()
        jwt_token = jwt.encode({"user_id": str(user.id)}, signing_secret, algorithm="HS256")
        response.set_cookie("jwt", jwt_token, httponly=True, secure=True, samesite="None")
        response.redirect("http://localhost:5174/home")
        return response