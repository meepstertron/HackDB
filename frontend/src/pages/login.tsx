function LoginPage() {

    const oauth_scopes = [
        "identity.basic",
        "identity.email",
    ]
    const oauth_scope = oauth_scopes.join(",");
    const client_id = "2210535565.8853049172611";
    const state = "HackClub!";
    return ( 
        <div>
            <p>Please Login with your slack :)</p>
            <a href={`https://slack.com/oauth/v2/authorize?user_scope=${oauth_scope}&client_id=${client_id}&state=${state}`}><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
        </div>
     );
}

export default LoginPage;