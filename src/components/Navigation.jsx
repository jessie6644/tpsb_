import React from "react";
import { Link, withRouter } from "react-router-dom";

function Navigation(props) {
  return (
    <div className="navigation">
      <nav className="navbar">
        <ul className="navbar-nav">
          <Link className="menu-item" to="/">
            Toronto Police Services Board
          </Link>
        </ul>
      </nav>
    </div>
  );
}

export default withRouter(Navigation);
