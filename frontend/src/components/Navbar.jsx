import "./../styles/dashboard.css";

export default function Navbar({logout}){

return(

<div className="navbar">

<h1>🛡 AI Security Agent</h1>

<button onClick={logout}>

Logout

</button>

</div>

);

}
