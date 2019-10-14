const exec = require('child_process').exec;

module.exports = (phrase) => {
    return new Promise((resolve, reject) => {
        const py = exec(`python3 /home/luca/batcave/random/hackupc2019/markov-hackup19/run.py "${phrase}"`,(error,stdout,stderr)=>{
            console.log(lines)
            const lines = stdout.split("\n").slice(4,7).join();
            console.log('error:',error);
            console.log('stderr:',stderr);
            resolve(lines);
        });
        let dataString = '';
        py.stdout.on('data', function (data) {
            dataString += data.toString();
        });
        py.stdout.on('end', function () {
            if (dataString) resolve(dataString)
        });
        let error = ''
        py.stderr.on('data', function (data) {
            error += data.toString();
        });
        py.stderr.on('end', function () {
            if (error) {
                reject(error)
            }
        });
    })
}