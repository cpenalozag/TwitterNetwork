import React, {Component} from "react";
import {BrowserRouter as Router, Switch, Route, NavLink} from 'react-router-dom';

import Dashboard from "../dashboard/Dashboard";
import Footer from "./Footer";
import About from "../dashboard/About";
import Users from "../dashboard/Users";


class Navbar extends Component {

    constructor(props) {
        super(props);
    }

    componentDidUpdate() {
        if (this.props.dataReady){
            if (!this.props.users[0]){
                Meteor.call("users.initialInsert")
            }
        }
    }

    render() {
        return (
            <Router>
                <div className="wrapper">
                    <div className="sidebar">
                        <div className="sidebar-wrapper">
                            <div className="text-center">
                                <img className="logo" src="images/logo.png" alt="Logo"/>

                            </div>
                            <ul className="nav">
                                <li>
                                    <NavLink activeClassName="active-link" exact className="nav-link" to="/">
                                        <i className="fas fa-search"></i>
                                        <p>Search</p>
                                    </NavLink>
                                </li>
                                <li>
                                    <NavLink activeClassName="active-link" exact className="nav-link" to="/users">
                                        <i className="fas fa-user"></i>
                                        <p>Users</p>
                                    </NavLink>
                                </li>
                                <li>
                                    <NavLink activeClassName="active-link" exact className="nav-link" to="/about">
                                        <i className="fas fa-info"></i>
                                        <p>About</p>
                                    </NavLink>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div className="main-panel">
                        <nav className="navbar navbar-expand-lg " color-on-scroll="500">
                            <div className=" container-fluid">
                                <h4 className="card-category dark-blue"><strong>Influencer Selection</strong></h4>
                                <button className="navbar-toggler navbar-toggler-right" type="button"
                                        data-toggle="collapse" data-target="#navbarNav" aria-controls="navigation-index"
                                        aria-expanded="false"
                                        aria-label="Toggle navigation">
                                    <span className="navbar-toggler-bar burger-lines"></span>
                                    <span className="navbar-toggler-bar burger-lines"></span>
                                    <span className="navbar-toggler-bar burger-lines"></span>
                                </button>
                                <div className="collapse navbar-collapse" id="navbarNav">
                                    <ul className="navbar-nav">
                                        <li className="nav-item active">
                                            <NavLink activeClassName="active-link" exact className="nav-link"
                                                     to="/">
                                                <p>Search</p>
                                            </NavLink>
                                        </li>
                                        <li className="nav-item active">
                                            <NavLink activeClassName="active-link" exact className="nav-link"
                                                     to="/users">
                                                <p>Users</p>
                                            </NavLink>
                                        </li>
                                        <li className="nav-item active">
                                            <NavLink activeClassName="active-link" exact className="nav-link"
                                                     to="/about">
                                                <p>About</p>
                                            </NavLink>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </nav>
                        <div className="content">
                            <Switch>
                                <Route exact path="/"
                                       render={(props) => <Dashboard {...props}/>}/>
                                <Route exact path="/users"
                                       render={(props) => <Users users={this.props.users} {...props}/>}/>
                                <Route exact path="/about"
                                       render={(props) => <About {...props}/>}/>
                            </Switch>
                        </div>
                        <Footer/>
                    </div>

                </div>
            </Router>
        );
    }
}

export default Navbar;