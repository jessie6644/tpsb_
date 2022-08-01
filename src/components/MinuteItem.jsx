import React, { Fragment } from "react";
import DOMPurify from 'dompurify';
import Parser from 'html-react-parser';
import BackendMethods from "./BackendMethods";
import {CSSTransition} from 'react-transition-group';

export default class MinuteItem extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      errors: false
    };

    this.ITEM = "Meeting/" + this.props.minute.meeting + "/Minute/" + this.props.minute.id + "/MinuteItem/"
  }

  async componentDidMount() {
    const data = await BackendMethods.fetchItems(this.ITEM)
    if (!data) {
      this.setState({errors:true});
    }
    this.setState({ data: data, loading: false });
  }

  setCurrentMinuteItem(minuteItem) {
    if (this.state.currentMinuteItem === minuteItem) {
      this.setState({currentMinuteItem: "blah"})
    } else {
        this.setState({currentMinuteItem: minuteItem});
    }
  }

  setCurrentMinuteItemKeyPress(e, minuteItem) {
    if (e.key === 'Enter') {
      this.setCurrentMinuteItem(minuteItem);
    }
  }

  displayResult(result) {
    const POSSIBLE_DECISIONS = {'TBC': 'To be considered', 'CUC': 'Currently under consideration', 'A': 'Approved',
                            'AWM': 'Approved with motion', 'R': 'Rejected'};
    return POSSIBLE_DECISIONS[result].toUpperCase();
  }

  displayMinuteItemDetails(item) {
    return <div>
      <img width="50%" src={require('./../img/tpsb_dropdown_header.png').default} alt="Toronto Police Services Board black and white icon header"/>
      <div>
        <div style={{ textAlign: "Left" }}> {Parser(DOMPurify.sanitize(item.recommendation))}</div>
        <div style={{fontWeight: 'bold'}}>MOVERS: {item.mover}</div>
        <div style={{fontWeight: 'bold'}}>SECONDERS: {item.seconder}</div>
        <div>{Parser(DOMPurify.sanitize(item.notes))}</div>
        {item.file && <a className="download-attach" href={item.file} download>Download Attachments: {item.file ? item.file.split('/').pop() : item.file}</a>}
        <br></br>
      </div>
    </div>
  }

  render() {
    if (this.state.errors) {
      return <div>could not retrieve minute information</div>
    }

    if (this.state.loading) {
      return <div></div>;
    }

    if (!this.state.data) {
      return <div>didn't get an minute item</div>;
    }

    return <table className="minuteItem-table">
      <tbody>
        <tr>
          <th>Number</th>
          <th>Title</th>
        </tr>
        {this.state.data.sort((a,b) => a.number - b.number).map((minuteItem) => {
          return <Fragment>
            <tr key={minuteItem.id} onClick={() => this.setCurrentMinuteItem(minuteItem)} tabIndex="0" onKeyDown={(e) => this.setCurrentMinuteItemKeyPress(e, minuteItem)}>
              <td>{minuteItem.subitem_number}</td>
              <td>{minuteItem.title}</td>
            </tr>
            <tr className="trh">
              <td height="auto" colspan="2" padding="0">
                <CSSTransition in={this.state.currentMinuteItem && this.state.currentMinuteItem === minuteItem}
                                timeout={1000}
                                classNames="dropdown"
                                unmountOnExit>
                  <div height="auto" position="relative">
                    {this.state.currentMinuteItem && this.displayMinuteItemDetails(minuteItem)}
                  </div>
                </CSSTransition>
              </td>
            </tr>
          </Fragment>
        })}
      </tbody>
    </table>

  }
}
