var React = require('react');
var LocalStorageMixin = require('react-localstorage');

var Router = require('react-router');
var RouteHandler = Router.RouteHandler;

var DoneItem = require('./done-item.jsx');
var DtView = require('./dt.jsx');
var ItemInput = require('./item-input.jsx');
var moment = require('moment');
var jquery = require('jquery');
var _ = require('underscore');


var DailyActions = React.createClass({
    mixins: [LocalStorageMixin],
    contextTypes: {
        router: React.PropTypes.func
    },
    getInitialState: function () {
        return {
            actions: [],
            inputText: '',
            durationMode: false,
            ranksEnabled: false
        };
    },
    getStateFilterKeys: function() {
        // state keys which saved to local storage
        return ['durationMode', 'ranksEnabled'];
    },
    getCurrentDt: function() {
        return moment().format('YYYY-MM-DDTHH:mm:ss');
    },
    componentDidMount: function() {
        var day = this.context.router.getCurrentQuery().day
            || moment().format('YYYY-MM-DD');
        jquery.ajax({
            url: window.config.urls.item_list,
            dataType: 'json',
            data: {
                day: day,
                tz_offset: (new Date()).getTimezoneOffset()
            },
            cache: false,
            success: function(data) {
                data = this._sortItems(data.result);
                this.setState({actions: data})
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    _setState: function(doneItem) {
        this.setState(function(previousState, currentProps) {
            previousState.actions.unshift(doneItem);
            console.log('new DA state', previousState);
            return previousState;
        });
        return this.state;
    },
    _sortItems: function(items) {
        return _.sortBy(items, 'when').reverse();
    },
    handleItemDelete: function(uid) {
        var actions = this.state.actions;
        actions = _.reject(
            actions,
            function(item) {
                return item.uid == uid;
            }
        );
        this.setState({actions: actions});
    },
    handleItemUpdate: function(data) {
        var items = _.map(
            this.state.actions,
            function(i) {return i.uid == data.uid ? data : i}
        );
        items = this._sortItems(items);
        this.setState({actions: items});
    },
    handleNewItemAdd: function (item) {
        this._setState(item);
    },
    onDurationModeChange: function () {
        this.setState({durationMode: !this.state.durationMode})
    },
    onRanksEnabledChange: function () {
        this.setState({ranksEnabled: !this.state.ranksEnabled})
    },
    render: function(){

        var doneActions = this.state.actions.slice()
            .map(function (item, i, actions) {
                var ms, minutes, rank;
                if (i == actions.length - 1) {
                    ms = moment(item.when).diff(moment().startOf('day'));
                } else {
                    ms = moment(item.when).diff(actions[i+1].when);
                }
                minutes = ms / 1000 / 60;
                // console.log(ms, minutes);
                if (minutes < 15) {
                    rank = 's';
                } else if (minutes < 30) {
                    rank = 'm';
                } else if (minutes < 60) {
                    rank = 'l';
                } else if (minutes < 120) {
                    rank = 'xl';
                } else {
                    rank = 'xxl';
                }

                if (!this.state.ranksEnabled) rank = 'm';

                return (
                    <DoneItem
                        key={item.uid}
                        idx={i}
                        item={item}
                        rank={rank}
                        diff={moment.utc(ms).format('H:mm')}
                        durationMode={this.state.durationMode}
                        onDelete={this.handleItemDelete}
                        onUpdate={this.handleItemUpdate}
                    />
                );
            }.bind(this));
        return (
          <div className='daily-actions'>
            <DtView getCurrentDt={this.getCurrentDt}/>
            <div className='new-action-container'>
                <ItemInput onAdd={this.handleNewItemAdd} />
            </div>
            <div className='settings'>
                <div className='duration-mode'>
                    <input
                        className="toggle"
                        type="checkbox"
                        checked={this.state.durationMode}
                        onChange={this.onDurationModeChange}
                    />
                    <label>Show duration?</label>
                </div>
                <div className='ranks-enabled'>
                    <input
                        className="toggle"
                        type="checkbox"
                        checked={this.state.ranksEnabled}
                        onChange={this.onRanksEnabledChange}
                    />
                    <label>Enable ranks?</label>
                </div>
            </div>
            <ul className='done-items-list-container'>
                {doneActions}
            </ul>
            <RouteHandler/>
          </div>
        );
    }
});
module.exports = DailyActions;
