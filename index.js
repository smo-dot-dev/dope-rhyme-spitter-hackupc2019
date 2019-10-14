<<<<<<< HEAD
const Twit = require('twit')
const config = require('./config')
const T = new Twit(config)

var stream = T.stream('statuses/filter', {
    track: '@lucavnr'
})

stream.on('tweet', function (tweet) {
    const username = tweet.user.screen_name;
    const id = tweet.id;
    const answer = `Cheers Mate. @${username}`;

    T.post('statuses/update', {
        status: answer,
        in_reply_to_status_id: id
    }, function (err, data, response) {
        console.log(data)
    })
})
=======
const axios = require('axios');
const config = require('./conf')
const generator = require('./generator')

const express = require('express');
const app = express()
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const path = require('path');

const _ = require('lodash');

const storage = require('node-persist');

let locked = false;

storage.init({
    logging: true
}).then(() => {
    setInterval(() => {
        if (!locked) loop()
    }, 10000)
    io.on('connection', function (socket) {
        console.log('a user connected');
        socket.on("vote", async data => {
            lock = true;
            console.log('read io');
            rhymes = await storage.getItem('rhymes') || [];
            rhymes.forEach(rhyme => {
                console.log(rhyme.id, data.id)
                if (rhyme.id === data.id) rhyme.score += data.value
            })
            //    console.log(rhymes);
            console.log('write io');

            await storage.setItem('rhymes', rhymes);
            lock = false;
            io.emit('update', rhymes)
        });
    });
})
axios.defaults.headers.common['Authorization'] = `Bearer ${config.token}`;

let lock = false;

loop = async () => {
    console.log('read loop');

    rhymes = await storage.getItem('rhymes') || [];

    response = await axios.get('https://api.videoask.it/questions/5d231a45-6b74-452f-b9c1-58f13ca72309/answers')

    let filtered = response.data.map(answer => {
        return {
            id: answer.answer_id,
            name: answer.contact_name,
            transcript: answer.transcription,
            timestamp: answer.created_at || new Date()
        }
    })

    const all = _.uniqBy([...rhymes, ...filtered], 'id')
        .filter(el => el.transcript && el.name)
        .map(el => {
            if (el.score) {
                return el;
            } else {
                return {
                    ...el,
                    score: 0
                }
            }
        });
    locked = true;
    const res = await Promise.all(all.map(entry => {
        if (!entry.answer) {

            //new ones

            //1. Clean the entry
            const sentences = entry.transcript.split('.');
            sentences.forEach(sentence => {
                sentence = sentence.charAt(0).toUpperCase() + sentence.slice(1)
            });
            entry.transcript = sentences.slice(-3).join();
            //2. Run the AI
            console.log('bbb');
            return generator(entry.transcript).then(answer => {
                console.log('aaa');

                return {
                    ...entry,
                    answer: answer
                }
            });
        } else {
            return entry
        }
    }))
    locked = false;
    console.log('all', res);

    if (!lock) await storage.setItem('rhymes', res);

    console.log(res.length);
    io.emit('update', res)
}

app.use(express.static(path.join(__dirname, 'public')));

http.listen(80, function () {
    console.log('HTTP Server started.');
});
>>>>>>> 3da9ebf77d3b4c34a170671a5f64794191328cfb
