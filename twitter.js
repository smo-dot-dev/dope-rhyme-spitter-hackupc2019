const Twit = require('twit')
const config = require('./config')
const generator = require('./generator')
const T = new Twit(config)

var stream = T.stream('statuses/filter', {
    track: '@lucavnr'
})

stream.on('tweet', function (tweet) {
    const username = tweet.user.screen_name;
    const id = tweet.id;
    const answer = `Cheers Mate. @${username}`;
    generator().then((line)=>{
        console.log(line)
        T.post('statuses/update', {
            status: answer,
            in_reply_to_status_id: id
        }, function (err, data, response) {
            
        })
    });
})