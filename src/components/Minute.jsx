import React from "react";
import DOMPurify from 'dompurify';
import Parser from 'html-react-parser';
import MinuteItem from "./MinuteItem.jsx"
import BackendMethods from "./BackendMethods";

export default class Minute extends React.Component {
  constructor(props, match) {
    super(props);

    this.state = {
      loading: true,
      errors: false
    };
    this.ITEM = "Meeting/" + this.props.match.params.meetingId + "/Minute/"
  }

  async componentDidMount() {
    const data = await BackendMethods.fetchItems(this.ITEM)
    if (!data) {
      this.setState({errors:true});
    }
    this.setState({ data: data[0]});

    const meetingData = await BackendMethods.fetchItems("Meeting/" + this.props.match.params.meetingId + "/");
    if (!meetingData) {
      this.setState({errors:true});
    }
    this.setState({ meetingData: meetingData, loading: false });
  }

  isPublic(type) {
    const MEETING_TYPES = {'PUB': 'Public', 'SPEC': 'Special', 'CONF': 'Confidential'};
    return MEETING_TYPES[type].toUpperCase();
  }

  render() {
    if (this.state.errors) {
      return <div>could not retrieve meeting minutes information</div>
    }

    if (this.state.loading) {
      return <div></div>;
    }

    if (!this.state.data) {
      return <div>didn't get a meeting</div>;
    }

    return <div>
        <div className="minute-title">
          <div className="flex"><img src={require('./../img/tpsb_icon.png').default} alt="Toronto Police Services Board Icon" /></div>
          <br></br>
          <h1 style={{ textAlign: "Center" }}>Online Virtual Meeting</h1>
          <h1 style={{ textAlign: "Center" }}>{this.state.meetingData.date.substring(0, this.state.meetingData.date.indexOf('T')).split('/').reverse()}</h1>
          <h1 style={{ textAlign: "Center" }}>At {this.state.meetingData.date.substring(this.state.meetingData.date.indexOf('T') + 1, this.state.meetingData.date.length).split('-')[0]}</h1>
          <br></br>
          <div className="meetingDescription" style={{ textAlign: "Center" }}> {Parser(DOMPurify.sanitize(this.state.meetingData.description))}</div>
          <h2 style={{ textAlign: "Center" }}>{this.isPublic(this.state.data.minute_type)} MEETING MINUTES</h2>
          <h3 style={{ textAlign: "Center" }}>{this.state.data.minute_date}</h3>
        </div>
        <div>

          <MinuteItem minute={this.state.data}/>
        </div>
        <br></br>
      </div>
  }
}
