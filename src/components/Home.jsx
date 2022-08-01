import React from "react";
import Meetings from "./Meetings";

function Home() {
  return (
    <div className="home">
      <div className="container">
        <div className="align-items-center">
          <div className="main-icon">
            <img src={require('./../img/tpsb_icon.png').default} alt="Toronto Police Services Board Icon"/>
          </div>
          <div className="col-lg-5">
            <p>
              < Meetings/>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
