import React, { Fragment } from "react";
import Drop from "./Drop"
import BackendMethods from "./BackendMethods";
import {CSSTransition} from 'react-transition-group';

class Meetings extends React.Component {
  ITEM = "Meeting/"

  constructor(props) {
    super(props);

    this.state = {
      data: {},
      loading: true
    };
  }

  async componentDidMount() {
    const data = await BackendMethods.fetchItems(this.ITEM)
    if (!data) {
      this.setState({errors:true});
    }
    this.setState({ data: data, loading: false });
  }

  meetingLabel() {
    return this.state.currentMeeting.title;
  }

  setCurrentMeeting(meeting) {
    if (this.state.currentMeeting === meeting) {
      this.setState({currentMeeting: "blah"})
    } else {
      this.setState({currentMeeting: meeting});
    }
  }

  setCurrentMeetingKeyPress(e, meeting) {
    if (e.key === 'Enter') {
      this.setCurrentMeeting(meeting);
    }
  }

  displayMeetingDetails(thisMeeting) {
    return <div className="meeting-details">
      <div className="agenda-minutes-header-left">
        <h1>{thisMeeting.title}</h1>
      </div>
      <Drop currentMeeting={thisMeeting} />
    </div>
  }

  isPublic(type) {
    const MEETING_TYPES = {'PUB': 'Public', 'SPEC': 'Special', 'CONF': 'Confidential'};
    return MEETING_TYPES[type].toUpperCase();
  }

  render() {
    if (this.state.errors) {
      return <div>could not retrieve meeting information</div>
    }

    if (this.state.loading) {
      return <div></div>;
    }

    if (!this.state.data) {
      return <div>didn't get a meeting</div>;
    }

    return (
      <div className="meeting-info">
        <div className="meeting-table">
          <table border="1">
            <tbody>
              <tr>
                <th>Date</th>
                <th>Title</th>
                <th>Type</th>
              </tr>
              {this.state.data.sort((a, b) =>
                new Date(...b.date.substring(0, b.date.indexOf('T')).split('/').reverse()) -
                new Date(...a.date.substring(0, a.date.indexOf('T')).split('/').reverse())).map((meeting) => {
                return <Fragment>
                  <tr key={meeting.id} onClick={() => this.setCurrentMeeting(meeting)} tabIndex="0" onKeyDown={(e) => this.setCurrentMeetingKeyPress(e, meeting)}>
                    <td>{meeting.date.substring(0, meeting.date.indexOf('T'))}</td>
                    <td>{meeting.title}</td>
                    <td>{this.isPublic(meeting.meeting_type)}</td>
                  </tr>
                  <tr className="trh">
                  <td height="auto" colspan="3" padding="0">
                  <CSSTransition in={this.state.currentMeeting && this.state.currentMeeting === meeting}
                                  timeout={1000}
                                  classNames="dropdown"
                                  unmountOnExit>
                    <div height="auto" position="relative">
                      {this.state.currentMeeting && this.displayMeetingDetails(meeting)}
                    </div>
                  </CSSTransition>
                  </td>
                  </tr>
                </Fragment>
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

export default Meetings;
