import React from "react";
import "../styles/Dashboard.css";
import { useLocation } from "react-router-dom";

function Dashboard() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const username = params.get("user");
  const [searchTerm , setSearchTerm] = React.useState("");
  const [activeMenu, setActiveMenu] = React.useState("Dashboard");
  const [showAvatarMenu, setShowAvatarMenu] = React.useState(false);

  React.useEffect(() => {
  const closeMenu = () => setShowAvatarMenu(false);
  window.addEventListener("click", closeMenu);
  return () => window.removeEventListener("click", closeMenu);
}, []);


  const handleSearch = () => {
    if(!searchTerm.trim()) return;
    console.log("Searching for:",searchTerm);
  };

  return (
    <div className="dashboard">

      {/* LEFT FIXED SIDEBAR */}
      <aside className="full-sidebar">
        <div className="sidebar-logo">Atlas</div>
        <p className="sidebar-title">Holdings</p>
        
       <div className="menu-section-title">Main Menu</div>
        <nav className="sidebar-menu">

  <div
    className={`menu-item ${activeMenu === "Dashboard" ? "active" : ""}`}
    onClick={() => setActiveMenu("Dashboard")}
  >
    📊 Dashboard
  </div>

  <div
    className={`menu-item ${activeMenu === "Accounts" ? "active" : ""}`}
    onClick={() => setActiveMenu("Accounts")}
  >
    💼 Accounts
  </div>

  <div
    className={`menu-item ${activeMenu === "Cards" ? "active" : ""}`}
    onClick={() => setActiveMenu("Cards")}
  >
    💳 Cards
  </div>

  <div
    className={`menu-item ${activeMenu === "Analytics" ? "active" : ""}`}
    onClick={() => setActiveMenu("Analytics")}
  >
    📈 Analytics
  </div>

  <div
    className={`menu-item ${activeMenu === "Settings" ? "active" : ""}`}
    onClick={() => setActiveMenu("Settings")}
  >
    ⚙️ Settings
  </div>

</nav>


       <nav className="sidebar-menu">
        <div className="menu-section-title">Sheduled Payments</div>

  <div
    className={`menu-item ${activeMenu === "Monthly Payment" ? "active" : ""}`}
    onClick={() => setActiveMenu("Monthly Payment")}
  >
    📅 Monthly Payment
  </div>

  <div
    className={`menu-item ${activeMenu === "Food Payment" ? "active" : ""}`}
    onClick={() => setActiveMenu("Food Payment")}
  >
    🍽️ Food Payment
  </div>

  <div
    className={`menu-item ${activeMenu === "Utility Bills" ? "active" : ""}`}
    onClick={() => setActiveMenu("Utility Bills")}
  >
    💡 Utility Bills
  </div>

</nav>
  </aside>

      {/* MAIN CONTENT */}
      <div className="main-content">

        {/* HEADER */}
        <div className="header">
          <div className="header-left">
            <h2>
              Welcome,<span className="username-highlight"> {username}</span>
            </h2>
            <p>Manage your banking quickly</p>
          </div>

          
            <form
              className="header-center search-wrapper"
              onSubmit={(e) => {
                e.preventDefault(); // stops page reload
                handleSearch();     // runs search
                 }}
            >

            <input
              type="text"
              placeholder="Search here...."
              className="search-input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button  type ="submit"className="search-btn">🔍</button>
          </form>


          <div className="header-right">
            <div className="notification-icon">🔔</div>
            <div className="avatar"
             onClick={(e)=> {
              e.stopPropagation();
              setShowAvatarMenu(prev => !prev);}}>

             </div>
          </div>
          {showAvatarMenu && (
  <div className="avatar-dropdown">
    <div className="dropdown-item">👤 Profile</div>
    <div className="dropdown-item">📄 Details</div>
    <div className="dropdown-item logout-item">🚪 Logout</div>
  </div>
)}

        </div>

        {/* QUICK ACTIONS */}
        <div className="quick-actions">
          <div className="action-card">Transfer Via Card Number</div>
          <div className="action-card">Transfer to Another Bank</div>
          <div className="action-card">Transfer to Same Bank</div>
          <div className="action-card">Transfer to International Bank</div>
        </div>

        {/* GRID SECTION */}
        <div className="dashboard-grid">

          {/* TOP ROW — 2fr 1.3fr */}
          <div className="grid-row grid-top">
            <div className="card-large">
              <h3>Total Balance</h3>
            </div>
            <div className="card-large">
              <h3>Bills</h3>
            </div>
          </div>

          {/* BOTTOM ROW — 1.3fr 2fr */}
          <div className="grid-row grid-bottom">
            <div className="card-medium">
              <h3>Recent Transactions</h3>
            </div>
            <div className="card-medium">
              <h3>Cards</h3>
            </div>
          </div>

        </div>
      </div>
    </div>
    
  );
}

export default Dashboard;

