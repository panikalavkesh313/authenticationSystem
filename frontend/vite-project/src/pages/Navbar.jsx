import { useNavigate } from "react-router-dom";

export default function Navbar() {

  const navigate = useNavigate();

  const logout = () => {

    localStorage.removeItem("token");

    navigate("/login");

  };

  return (

    <div className="bg-blue-700 text-white flex justify-between items-center px-8 py-4">

      <h1 className="text-2xl font-bold">
        Dashboard
      </h1>

      <button
        onClick={logout}
        className="bg-red-500 px-5 py-2 rounded hover:bg-red-600"
      >
        Logout
      </button>

    </div>

  );
}