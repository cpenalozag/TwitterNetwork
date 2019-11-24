import React, {Component} from "react";

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.max_chars = 280;
        this.state = {
            text: '',
            media: 'DEFAULT',
            time: 'DEFAULT',
            button_disabled: true,
            chars_left: this.max_chars,
            results: []
        };
        this.handleSearch = this.handleSearch.bind(this);
        this.check_button = this.check_button.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleChangeTime = this.handleChangeTime.bind(this);
        this.handleChangeMedia = this.handleChangeMedia.bind(this);
    }

    handleChange(event) {
        let input = event.target.value;
        this.setState({
            text: event.target.value,
            chars_left: this.max_chars - input.length
        });
    }

    handleSelected(event) {
        const target = event.target;
        const name = target.name;
        Meteor.call("users.changeSelected", name)
    }

    handleChangeTime(event) {
        this.setState({time: event.target.value}, () => {
            this.check_button()
        });
    }

    handleChangeMedia(event) {
        this.setState({media: event.target.value}, () => {
            this.check_button()
        });
    }

    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    renderUsers() {
        return this.state.results.map((res) => {
            const id = res[0];
            const score = res[1]
            const user = this.props.users.find(user => user._id === String(id));
            return (
                <tr key={id}>
                    <td>{user.screen_name}</td>
                    <td>{score}</td>
                    <td className="verified-td">{user.verified ?
                        <img src="images/verified.png" className="verified" alt="Verified icon"/> : "-"}</td>
                    <td>{user.followers}</td>
                    <td>{this.capitalizeFirstLetter(user.type)}</td>
                    <td><input type="checkbox" checked={user.selected ? true : false} onChange={this.handleSelected}
                               name={`${user._id}`}/></td>

                </tr>
            )
        })
    }

    handleSearch() {
        (async () => {
            const rawResponse = await fetch('http://localhost:8080/predict', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({text: this.state.text, media: this.state.media, time: this.state.time})
            });
            const content = await rawResponse.json();

            this.setState({results: content.results});
        })();
    }

    check_button() {
        if (this.state.media != 'DEFAULT' && this.state.time != 'DEFAULT') {
            this.setState({button_disabled: false});
        }
    }

    render() {
        return (
            <div className="container-fluid">
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">Search users for your campaign</h4>
                            <p>Insert the text you want to post to Twitter. The search will find the best users to post
                                it!</p>
                        </div>
                        <hr/>
                        <div className="card-body ">
                            <p>Tweet message:</p>
                            <textarea onChange={this.handleChange.bind(this)} name="tweet-text" cols="40"
                                      className="text-input" rows="4"></textarea>
                            <p className={`chars-left ${this.state.chars_left < 0 ? "red" : ""}`}>Characters
                                Left: {this.state.chars_left}</p>
                        </div>
                        <div className="card-body">
                            <div className="row">
                                <div className="col">
                                    <select className="browser-default custom-select" value={this.state.time}
                                            onChange={this.handleChangeTime}>
                                        <option value="DEFAULT" disabled>Select the time of day the tweet will be
                                            posted
                                        </option>
                                        <option value="early morning">Early morning (12:00 AM – 5:00 AM)</option>
                                        <option value="morning">Morning (5:00 AM – 11:00 AM)</option>
                                        <option value="noon">Noon (11:00 AM – 12:00 PM)</option>
                                        <option value="afternoon">Afternoon (12:00 PM – 7:00 PM)</option>
                                        <option value="night">Night (7:00 PM – 9:00 PM)</option>
                                        <option value="late night">Late night (9:00 PM – 12:00 AM)</option>
                                    </select>
                                </div>
                                <div className="col">
                                    <select className="browser-default custom-select" value={this.state.media}
                                            onChange={this.handleChangeMedia}>
                                        <option value="DEFAULT" disabled>Select the number of media items (images, gifs,
                                            etc) in the tweet
                                        </option>
                                        <option value="0">0</option>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-md-2 mx-auto">
                                <input className={`btn btn-primary`}
                                       disabled={this.state.button_disabled ? true : false} type="submit" value="Search"
                                       onClick={this.handleSearch}/>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">Results</h4>
                        </div>
                        <div className="card-body ">
                            <table className="table table-bordered">
                                <tbody>
                                {this.state.results.length > 0 ?
                                    <tr>
                                        <th>Screen name</th>
                                        <th>Predicted engagement</th>
                                        <th>Verified</th>
                                        <th>Followers</th>
                                        <th>Category</th>
                                        <th>Selected</th>
                                    </tr>
                                    : <tr><th>Search to find the top users to post your message!</th></tr>
                                }
                                {this.renderUsers()}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Dashboard;