from flask import Blueprint, jsonify, request, make_response, redirect
from app import db, rq
import os
from uuid import uuid4
from slack_sdk import WebClient
from ..models import Users, CLIAuthState, Usertables
import jwt

client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
signing_secret = os.environ["SLACK_SIGNING_SECRET"]
state = "hackclub-" + str(uuid4())

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


@main.route("/taskstatus/<job_id>")
def task_status(job_id):
    job = rq.fetch_job(job_id)
    if job:
        return jsonify(job_id=job.id, status=job.get_status(), result=job.result)
    else:
        return jsonify(message="Job not found"), 404

@main.route("/begin_auth", methods=["GET"])
def pre_install():
  return f'<a href="https://slack.com/oauth/v2/authorize?user_scope={ oauth_scope }&client_id={ client_id }&state={state}"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>'


@main.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    auth_code = request.args["code"]
    auth_code = request.args["code"]
    received_state = request.args["state"]

    client = WebClient()

    if received_state.startswith("HackClub"):
        response = client.oauth_v2_access(
            client_id=client_id,
            client_secret=client_secret,
            code=auth_code
        )
    elif received_state.startswith("cli_"):
        response = client.oauth_v2_access(
            client_id=client_id,
            client_secret=client_secret,
            code=auth_code
        )
    else:
        return "Invalid State"

    if response.get("ok"):
        access_token = response["authed_user"]["access_token"]

        
        client = WebClient(token=access_token)
        identity_response = client.api_call("users.identity")
        if identity_response.get("ok"):
            user_info = identity_response["user"]
            slack_user_id = user_info["id"]
            username = user_info.get("name", "N/A")
            email = user_info.get("email", None)

            
            user = db.session.query(Users).filter_by(slack_user_id=slack_user_id).first()
            if user is None:
                # Create a new user in the database
                user = Users(
                    slack_user_id=slack_user_id,
                    slack_access_token=access_token,
                    username=username,
                    email=email
                )
                db.session.add(user)
                db.session.commit()

            if received_state.startswith("cli_"):
                instance_id = received_state[len("cli_"):]

                cli_state = db.session.query(CLIAuthState).filter_by(instance_id=instance_id).first()
                if cli_state:
                    cli_state.slack_user_id = slack_user_id
                    cli_state.verified = True
                else:
                    
                    user = db.session.query(Users).filter_by(slack_user_id=slack_user_id).first()
                    if not user:
                        return "Error: User not found"
                    cli_state = CLIAuthState(instance_id=instance_id, slack_user_id=slack_user_id, author_id=user.id, verified=True)
                    db.session.add(cli_state)
                db.session.commit()

                return """
            <html>
            <head>
            <title>Slack Auth Successful</title>
            </head>
            <body>
            <h1>Slack Auth Successful</h1>
            <p>Your Slack account has been successfully authenticated. Please return to the cli</p>
            </body>
            """

            response = make_response()
            jwt_token = jwt.encode({"user_id": str(user.id)}, signing_secret, algorithm="HS256")
            response = make_response(redirect("https://hackdb.hexagonical.ch/home"))
            response.set_cookie("jwt", jwt_token, httponly=True, secure=True, samesite="None")
            if received_state.startswith("cli_"):
                jwt_token =  jwt.encode()
                return
            return response
    else:
        return "Error: Auth Failed"
    
    

                    # valid: jsonData.valid || false,
                    # username: jsonData.username || null,
                    # email: jsonData.email || null,
                    # slack_id: jsonData.slack_id || null

    
@main.route("/api/me", methods=["GET"])
def me():
    token = request.cookies.get("jwt")
    if not token:
        return jsonify(message="Unauthorized"), 401

    try:
        payload = jwt.decode(token, signing_secret, algorithms=["HS256"])
        user_id = payload["user_id"]
        user = db.session.query(Users).filter_by(id=user_id).first()
        if user:
            return jsonify(user={"id": str(user.id), "username": user.username, "email": user.email, "slack_id":user.slack_user_id, "valid": True}), 200
        else:
            return jsonify(message="User not found"), 404
    except jwt.ExpiredSignatureError:
        return jsonify(message="Token expired"), 401
    except jwt.InvalidTokenError:
        return jsonify(message="Invalid token"), 401
    

@main.route("/api/cli/slackauth", methods=["GET"])
def slack_auth():
    instance_id = request.args.get("instanceid")
    if not instance_id:
        return jsonify(message="Instance ID is required"), 400

    # Here you would typically store the instance ID and redirect the user to Slack for authentication
    # For now, we will just return a success message
    return jsonify(message=f"Redirecting to Slack OAUTH for instance {instance_id}..."), 200


@main.route("/api/cli/polllogin", methods=["GET"])
def poll_cli_login():
    instance_id = request.args.get("instanceid")

    # check if user has filled out slack oauth by checking db (instances.hasVerified or .slackID)

    jwt_token = jwt.encode({"instance_id": str(instance_id)}, signing_secret, algorithm="HS256")
    return {"instanceid": instance_id, "token":jwt_token }, 200



@main.route("/api/logout", methods=["POST"])
def logout():
    response = make_response(redirect("https://hackdb.hexagonical.ch/home"))
    response.set_cookie("jwt", "", expires=0)
    return response


@main.route("/api/delete_account", methods=["POST"])
def delete_account():
    token = request.cookies.get("jwt")
    if not token:
        return jsonify(message="Unauthorized"), 401

    try:
        payload = jwt.decode(token, signing_secret, algorithms=["HS256"])
        user_id = payload["user_id"]
        user = db.session.query(Users).filter_by(id=user_id).first()
        if user:
            user_tables = db.session.query(Usertables).filter_by(user_id=user.id).all()
            userdb_engine = db.get_engine(bind='userdb')
            with userdb_engine.connect() as connection:
                for table in user_tables:
                    logical_table_name = f"{table.name}_{str(table.id).replace('-', '_')}"
                    connection.execute(f"DROP TABLE IF EXISTS {logical_table_name} CASCADE")
            db.session.query(Usertables).filter_by(user_id=user.id).delete()
            db.session.query(CLIAuthState).filter_by(slack_user_id=user.slack_user_id).delete()
            db.session.query(Users).filter_by(id=user.id).delete()
            
            
            
                    
                    
                    
                    
            db.session.delete(user)
            db.session.commit()
            return jsonify(message="Account deleted"), 200
        else:
            return jsonify(message="User not found"), 404
    except jwt.ExpiredSignatureError:
        return jsonify(message="Token expired"), 401
    except jwt.InvalidTokenError:
        return jsonify(message="Invalid token"), 401


@main.route("/api/metrics", methods=["GET"])
def metrics():
    """
    Expose application metrics in Prometheus format.
    """
    # Example metrics
    total_requests = 100  # Replace with actual logic to fetch total requests
    active_users = 10  # Replace with actual logic to fetch active users
    db_connections = 5  # Replace with actual logic to fetch DB connections

    metrics_data = f"""
# HELP hackdb_version Version of HackDB
# TYPE hackdb_version gauge
hackdb_version 1.0    

# HELP hackdb_requests_total Total number of requests
# TYPE hackdb_requests_total counter
hackdb_requests_total {total_requests}

# HELP hackdb_active_users Number of active users
# TYPE hackdb_active_users gauge
hackdb_active_users {active_users}

# HELP hackdb_db_connections Number of active database connections
# TYPE hackdb_db_connections gauge
hackdb_db_connections {db_connections}

"""

    return metrics_data, 200, {"Content-Type": "text/plain"}