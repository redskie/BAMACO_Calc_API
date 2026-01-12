import React from 'react';

interface DateAndPlaceProps {
  date: string;
  actualPlace: string;
  isDxMode: boolean;
  toggleDxMode: () => void;
}
export class DateAndPlace extends React.PureComponent<DateAndPlaceProps> {
  render() {
    const {actualPlace, date, isDxMode} = this.props;
    const place = isDxMode ? actualPlace : 'CAFE MiLK';
    return (
      <div className="dateAndPlace">
        <div className="date">{date}</div>
        <button className="place" onClick={this.props.toggleDxMode}>
          {place}
        </button>
      </div>
    );
  }
}
