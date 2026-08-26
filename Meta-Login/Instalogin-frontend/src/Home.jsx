export default function Home() {
  return (
    <>
      <a href="https://www.instagram.com/oauth/authorize?force_reauth=true&client_id=859133170533640&redirect_uri=https://api.adonreel.com/api/users/instagram-auth&response_type=code&scope=instagram_business_basic%2Cinstagram_business_manage_messages%2Cinstagram_business_manage_comments%2Cinstagram_business_content_publish%2Cinstagram_business_manage_insights">
        <button>Login with INSTA</button>
      </a>
    </>
  );
}