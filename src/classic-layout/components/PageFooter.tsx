import React from 'react';

export class PageFooter extends React.PureComponent {
  private handleClick = (evt: React.SyntheticEvent) => {
    evt.preventDefault();
    window.close();
  };

  render() {
    return (
      <div className="pageFooter">
        <a className="closePage" href="#" onClick={this.handleClick}>
          戻る
        </a>
      </div>
    );
  }
}
