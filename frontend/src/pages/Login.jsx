import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      localStorage.setItem("token", response.data.access_token);

      alert("Login Successful!");

      navigate("/dashboard");
    } catch (err) {
      console.error(err);

      if (err.response) {
        alert(err.response.data.detail);
      } else {
        alert("Server not reachable.");
      }
    }
  };

  return (
    <div style={{ width: "400px", margin: "100px auto" }}>
      <h1>AI Security Agent</h1>

      <form onSubmit={login}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ width: "100%", padding: 10, marginBottom: 15 }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: "100%", padding: 10, marginBottom: 15 }}
        />

        <button
          type="submit"
          style={{ width: "100%", padding: 12 }}
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;