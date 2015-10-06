
var React = require('react');
var classNames = require('classnames');
var moment = require('moment');
var jquery = require('jquery');
var _ = require('underscore');


var ENTER_KEY = 13;
var TIME_FMT = 'HH:mm';

var DoneItem = React.createClass({
    getInitialState: function() {
        return {
            editing: false,
            timeText: moment(this.props.item.when).format(TIME_FMT),
            text: this.props.item.what
        };
    },
    handleTimeChange: function (event) {
        var val = event.target.value.trim();
        this.setState({timeText: val});
    },
    handleTextChange: function (event) {
        var val = event.target.value.trim();
        this.setState({text: val});
    },
    handleKeyDown: function (event) {
        if (event.which !== ENTER_KEY) {
            return;
        }
        this.handleSave();
        event.preventDefault();
    },
    handleSave: function() {
        if (
            !this.state.timeText
            || this.isTimeValid()
            || !this.state.text
        ) return;
        var timeParts = this.state.timeText.split(':');
        var when = moment(this.props.item.when)
            .hours(timeParts[0])
            .minutes(timeParts[1])
            .format('YYYY-MM-DDTHH:mm:ss');
        var item = this.props.item;
        item.what = this.state.text;
        item.when = when;
        jquery.ajax({
            url: window.config.urls.update_item,
            data: {
                uid: item.uid,
                tz_offset: (new Date()).getTimezoneOffset(),
                what: item.what,
                when: item.when,
            },
            dataType: 'json',
            success: function(data) {
                console.log('update item success: ', data);

                this.setState({editing: false});
                this.props.onUpdate(item);
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(status, err.toString());
            }.bind(this)
        });
    },
    handleDelete: function() {
        jquery.ajax({
            url: window.config.urls.delete_item,
            data: {
                uid: this.props.item.uid
            },
            dataType: 'json',
            cache: false,
            success: function(data) {
                console.log('delete item success: ', data)
                this.props.onDelete(this.props.item.uid);
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(status, err.toString());
            }.bind(this)
        });
    },
    isTimeValid: function() {
        return moment(this.state.time, TIME_FMT, true).isValid();
    },
    setEditing: function() {
        this.setState({editing: true});
    },
    render: function(){

        var item = this.props.item;
        var doneItem = this.state.editing ? (
            <li className={'done-item font-' + this.props.rank}>
                <div className='item-edit-form'>
                    <input
                        tabIndex={(this.props.idx + 1) * 100 + 1}
                        type='text'
                        maxLength='5'
                        onChange={this.handleTimeChange}
                        onKeyDown={this.handleKeyDown}
                        value={this.state.timeText}
                        className={classNames('time-input', 'font-l', {invalid: this.isTimeValid()})}
                    />
                    <input
                        tabIndex={(this.props.idx + 1) * 100}
                        type='text'
                        onChange={this.handleTextChange}
                        onKeyDown={this.handleKeyDown}
                        value={this.state.text}
                        className={classNames('what-input', 'font-l', {invalid: !this.state.text})}
                    />
                    <button
                        className="save-item icon-button glyphicons glyphicons-check"
                        onClick={this.handleSave}
                    ></button>
                </div>
            </li>
        ) : (
            <li className={'done-item font-' + this.props.rank}>
                <span className='item-time'>
                    {this.props.durationMode ? this.props.diff : this.state.timeText}
                </span>
                <span className='item-what'>
                    {item.what}
                </span>
                <button
                    className="edit-item icon-button glyphicons glyphicons-pencil"
                    onClick={this.setEditing}
                ></button>
                <button
                    className="delete-item icon-button glyphicons glyphicons-bin"
                    onClick={this.handleDelete}
                ></button>
            </li>
        );
        return doneItem;
    }
});
module.exports = DoneItem;
