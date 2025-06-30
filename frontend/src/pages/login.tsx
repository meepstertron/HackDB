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


            <footer style={{ position: "fixed", bottom: "0", width: "100%", textAlign: "center", backgroundColor: "#f9f9f9", padding: "10px" }}>
                <p>HackDB is part of the <a href="https://hexagonical.ch" className="underline">Hexagonical</a> Suite. We are not affiliated with Slack. By signing up, you agree to Hexagonical's <a href="https://hexagonical.ch/legal/tos" className="underline">Terms of Service</a> and <a href="https://hexagonical.ch/legal/privacy" className="underline">Privacy Policy</a>.</p>
            </footer>
        </div>
     );
}

export default LoginPage;