
var React = require('react');
var jquery = require('jquery');

var ENTER_KEY = 13;

var ItemInput = React.createClass({
    getInitialState: function () {
        return {what: ''};
    },
    handleChange: function (event) {
        this.setState({what: event.target.value});
    },
    handleKeyDown: function (event) {
        if (event.which !== ENTER_KEY) {
            return;
        }
        console.log(this.state.what)
        var val = this.state.what.trim();
        if (val) {

            jquery.ajax({
                url: window.config.urls.save_item,
                data: {
                    what: val,
                    tz_offset: (new Date()).getTimezoneOffset()
                },
                dataType: 'json',
                cache: false,
                success: function(data) {
                    console.log('save item success: ', data);
                    this.setState(this.getInitialState());
                    this.props.onAdd(data.result.item);
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error(status, err.toString());
                }.bind(this)
            });
        }
        event.preventDefault();
    },
    render: function(){
        return (
            <input
                ref="newAction"
                className="new-action"
                placeholder=""
                onChange={this.handleChange}
                onKeyDown={this.handleKeyDown}
                autoFocus={true}
                value={this.state.what}
            />
        );
    }
});

module.exports = ItemInput;
