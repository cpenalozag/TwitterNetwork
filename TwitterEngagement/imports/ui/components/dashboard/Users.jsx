import React, {Component} from "react";

class Users extends Component {

    constructor(props) {
        super(props);
        this.state = {};

        this.pColors = [
            "#FF0000",
            "#FF6600",
            "#FFDA00",
            "#00cd00",
            "#00A4E4",
            "#6A737B",
            "#FF0065",
            "#800080",
            "#2E282A"
        ];

        this.pSizes = [
            190, 385, 428, 442, 35, 295, 6, 6, 2
        ]

        this.renderSelected = this.renderSelected.bind(this);
        this.renderUnselected = this.renderUnselected.bind(this);
    }

    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    handleSelected(event) {
        const target = event.target;
        const name = target.name;
        Meteor.call("users.changeSelected", name)
    }

    renderSelected() {
        const filtered = this.props.users.filter((user)=>user.selected==true);
        return filtered.map((user) => {
            return (
                <tr key={user._id}>
                    <td style={{backgroundColor: this.pColors[user.partition], opacity:0.9}}></td>
                    <td>{user.screen_name}</td>
                    <td>{user.followers}</td>
                    <td>{this.capitalizeFirstLetter(user.type)}</td>
                    <td><input type="checkbox" onChange={this.handleSelected} name={`${user._id}`} checked/></td>
                </tr>
            )
        })
    }

    renderUnselected() {
        const filtered = this.props.users.filter((user)=>user.selected==false);
        return filtered.map((user) => {
            return (
                <tr key={user._id}>
                    <td style={{backgroundColor: this.pColors[user.partition], opacity:0.9}}></td>
                    <td>{user.screen_name}</td>
                    <td>{user.followers}</td>
                    <td>{this.capitalizeFirstLetter(user.type)}</td>
                    <td><input type="checkbox" onChange={this.handleSelected} name={`${user._id}`}/></td>
                </tr>
            )
        })
    }

    renderClasses() {
        const classes = [0,1,2,3,4,5,6,7,8]
        return classes.map((c) => {
            return (
                <tr key={c}>
                    <td style={{backgroundColor: this.pColors[c], opacity:0.9}}></td>
                    <td>{this.pSizes[c]}</td>
                </tr>
            )
        })
    }

    render() {
        return (
            <div className="container-fluid">
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">Selected Users</h4>
                            <p>This list contains the information of the users that you have picked for your campaigns:</p>
                        </div>
                        <div className="card-body ">
                            <table className="table table-bordered">
                                <tbody>
                                <tr>
                                    <th>Class</th>
                                    <th>Screen name</th>
                                    <th>Followers</th>
                                    <th>Category</th>
                                    <th>Selected</th>
                                </tr>
                                {this.renderSelected()}
                                </tbody>
                            </table>
                            <hr/>
                            <p>Size of the different classes:</p>
                            <div className="row">
                                <div className="col-md-3 mx-auto">
                                    <table className="table table-bordered">
                                        <tbody>
                                        <tr>
                                            <th>Class</th>
                                            <th>Size</th>
                                        </tr>
                                        {this.renderClasses()}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">Other Users</h4>
                            <p>This list shows all the other users in the database:</p>
                        </div>
                        <div className="card-body ">
                            <table className="table table-bordered">
                                <tbody>
                                <tr>
                                    <th>Class</th>
                                    <th>Screen name</th>
                                    <th>Followers</th>
                                    <th>Category</th>
                                    <th>Selected</th>
                                </tr>
                                {this.renderUnselected()}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Users;