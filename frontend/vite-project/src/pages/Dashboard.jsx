import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "./Navbar";
export default function Dashboard() {

  const navigate = useNavigate();

  const [user, setUser] = useState(null);

  useEffect(() => {

    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    API.get("/profile", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        console.log(res.data);

        // Save only the user object
        setUser(res.data.user);
      })
      .catch((err) => {
        console.log(err.response);

        localStorage.removeItem("token");
        navigate("/login");
      });

  }, [navigate]);

  if (!user) {
    return (
      <h1 className="text-center mt-10">
        Loading...
      </h1>
    );
  }

  return (
    <>
      <Navbar />

      <div className="p-10">
        <h1 className="text-4xl font-bold">
          Welcome {user.name}
        </h1>

        <p className="mt-4">
          {user.email}
        </p>
      </div>
    </>
  );
}