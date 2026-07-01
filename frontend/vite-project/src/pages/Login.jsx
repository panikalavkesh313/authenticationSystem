import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api/axios";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const login = async (e) => {
    e.preventDefault();

    try {
      const res = await API.post("/login", {
        email,
        password,
      });
      console.log(res.data.token);
      localStorage.setItem("token", res.data.token);

      navigate("/dashboard");
      // localStorage.setItem("token", res.data.token);
      // navigate("/dashboard");
    } catch (err) {
      alert(err.response.data.message);
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-r from-indigo-600 to-purple-700">

      <form
        onSubmit={login}
        className="bg-white rounded-xl shadow-lg p-8 w-96"
      >
        <h1 className="text-3xl font-bold mb-6 text-center">
          Login
        </h1>

        <input
          placeholder="Email"
          className="border p-3 rounded w-full mb-4"
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Password"
          className="border p-3 rounded w-full mb-4"
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button className="bg-green-600 hover:bg-green-700 text-white py-3 rounded w-full">
          Login
        </button>

        <p className="text-center mt-5">

          Don't have an account?

          <Link
            to="/register"
            className="text-blue-600 ml-2"
          >
            Register
          </Link>

        </p>
      </form>

    </div>
  );
}