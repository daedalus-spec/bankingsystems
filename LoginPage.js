import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  //password validation rules
  const isPasswordValid =() => {
    const hasUpper =/[A-Z]/.test(password);
    const hasNumber=/[0-9]/.test(password);
    const hasSpecial=/[^A-Za-z0-9]/.test(password);
    const hasLength=password.length >= 8;
  
         return hasUpper && hasNumber && hasSpecial && hasLength;
  }

    const handleLogin = async () => {
  // TEMP TEST
  localStorage.setItem("token", "dummy-token");
  navigate("/dashboard?user=" + username);
};



  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Bank Login</h2>

    {/* Username*/}

      <input
        type="text"
        placeholder="Enter Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={{ padding: "10px", margin: "10px", width: "250px" }}
      />

      <br />
    {/* Password*/}
    <div style = {{ position: "relative", display : "inline-block"}}>
      <input
        type={showPassword ? "text" : "password"}
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ padding: "10px", margin: "10px", width: "250px" }}
      />


      {/* TOGGLE SHOW AND HIDE */}
      <span
        onClick={() => setShowPassword(!showPassword)}
        style={{
            position : "absolute",
            right: "20px",
            top: "50%",
            transform: "translateY(-50%)",
            cursor: "pointer",
            color: "20px"
        }}
    >
        {showPassword ? "🙈" : "👁️"}
    </span>

    {/* tick in green when valid */}
    {isPasswordValid() && (
         <span
          style={{
              position: "absolute",
              right: "-25px",
              top: "50%",
              transform: "translateY(-50%)",
              color: "greenyellow",
              fontSize: "24px"
          }}>
            ✓
         </span>
    )}
    </div>


{/*password rules show only after typing */}
{password.length >0 && (
    <div style={{ fontsize: "14px",marginTop:"10px"}}>
        <p> Password must contain:</p>

         <p style ={{ color:password.length >=8 ? "greenyellow": "red"}}>
             • At Least 8 Characters
         </p>

         <p style={{ color:/[A-Z]/.test(password)? "greenyellow":"red"}}>
            • One Upper Password
         </p>

         <p style={{color: /[0-9]/.test(password)?"greenyellow" : "red"}}>
            • One Number
         </p>

         <p style={{ color :/[^A-Za-z0-9]/.test(password)? "greenyellow" :"red"}}>
            • One special Character
        </p>
    </div>
)}

{/* Disabled Button Until Valid */}
<button
    disabled ={!isPasswordValid()}
    onClick={handleLogin}
    style={{
        padding: "10px 30px",
        marginTop: "15px",
        backgroundColor: isPasswordValid() ? "blue" : "grey",
        color: "white",
        border:"none",
        borderRadius:"5px",
         cursor:isPasswordValid() ? "pointer" : "not-allowed"
        }}>
        Login
      </button>
    </div>
  );
}

export default LoginPage;
