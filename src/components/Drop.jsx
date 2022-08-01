import React from "react";
import BackendMethods from "./BackendMethods";

export default class Drop extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      errors: false,
      currentMeeting: this.props.currentMeeting
    };
    this.ITEM = "Meeting/" + this.props.currentMeeting.id + "/Agenda/";
  }

  async componentDidMount() {
    const url = BackendMethods.currentAdminUrl(this.ITEM);
    const response = await fetch(url)
      .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response;
      }).catch(error => {
        this.setState({ errors: true })
      });

    const data = this.state.errors ? null : await response.json();
    this.setState({ data: data});

    this.setState({agenda : this.state.data})
    this.ITEM = "Meeting/" + this.state.currentMeeting.id + "/Minute/"

    const url1 = BackendMethods.currentAdminUrl(this.ITEM);
    const response1 = await fetch(url1)
      .then(function (response1) {
        if (!response1.ok) {
          throw Error(response1.statusText);
        }
        return response1;
      }).catch(error => {
        this.setState({ errors: true })
      });

    const data1 = this.state.errors ? null : await response1.json();
    this.setState({ data: data1, loading: false});

    this.setState({minutes : this.state.data})
  }

  setAgendaDownload() {
    const data = this.state.agenda
    if (data[0]) {
      return <a href={BackendMethods.currentAdminUploadUrl(data[0].id + '.pdf/')} target="_blank" className="sub-nav-text">
        Download Agenda
      </a>
    }

    return <a className="sub-nav-blank">
      Download Agenda
    </a>
  }

  setAgenda() {
    const data = this.state.agenda
    if (data) {
      const filtered = data.filter(minute => minute.meeting === Number(this.state.currentMeeting.id)).map((item) => (item))

      if (!(filtered.length === 0)) {
        return <a href={"agenda/" + this.state.currentMeeting.id} target="_blank" className="sub-nav-text">
          Read Agenda
        </a>
      }
    }

    return <a className="sub-nav-blank">
      Read Agenda
    </a>
  }

  setYouTubeLink() {
    const data = this.state.currentMeeting.recording_link
    if (data) {
      return <a href={this.state.currentMeeting.recording_link} target="_blank" className="sub-nav-text">
        View on Youtube
      </a>
    }

    return <a className="sub-nav-blank">
      View on Youtube
    </a>
  }

  setMinute() {
    const data = this.state.minutes
    if (data) {
      const filtered = data.filter(minute => minute.meeting === Number(this.state.currentMeeting.id)).map((item) => (item))

      if (!(filtered.length === 0)) {
        return <a href={"minute/" + this.state.currentMeeting.id} target="_blank" className="sub-nav-text">
          Read Minutes
        </a>
      }
    }

    return <a className="sub-nav-blank">
      Read Minutes
    </a>
  }

  render() {
    if (this.state.errors) {
      return <div>could not retrieve meeting minutes information</div>
    }

    if (this.state.loading) {
      return <div></div>;
    }

    return <ul className="agenda-minutes-header-right">
      <div>
        <li className="nav-agenda-minute-2">
          {this.setAgenda()}
        </li>
        <li className="nav-agenda-minute-2">
          {this.setAgendaDownload()}
        </li>
      </div>
      <li className="nav-agenda-minute-1">
        {this.setYouTubeLink()}
      </li>
      <li className="nav-agenda-minute-1">
        {this.setMinute()}
      </li>
    </ul>
  }
}
