const express = require('express');
const cors = require('cors');
const app = express();

// const { Kafka } = require('kafkajs');

// use HDFS bucket to store files



// create a duplicate cluster of backend project to additionally handle traffic
// ctrl + i

app.use(cors(
    {
        methods: ['GET', 'POST'],
        origin: '*',
    }
));

// app.use()
// ------------------------------ mongoose ------------------------------
const mongoose = require('mongoose');

mongoose.connect(process.env.MONGO_URL || 'mongodb://localhost:27018/file-upload')
.then(() =>{
    console.log('Connected to database');
}).catch((err) => {
    console.log('Error connecting to database', err);
});



const fileSchema = new mongoose.Schema({
    name: String,
    path: String,
    size: Number,
    type: String,
});
const File = mongoose.model('File', fileSchema);

// x----------------------------- mongoose -----------------------------x


// ------------------------------ multer ------------------------------
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// ------------------------------ diskStorage ------------------------------
const multerDiskStorage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
        // cb(null,process.env.UPLOAD_PATH);
    },
    filename: function(req, file, cb) {
        // cb(null, file.originalname);
        cb(null, file.fieldname + '-' + Date.now() + '-' + file.originalname);
    }
});
const uploadDisk = multer({ storage: multerDiskStorage });
// x------------------------------ diskStorage ------------------------------x

// x----------------------------- multer -----------------------------x

// ------------------------------ kafkajs ------------------------------
// const kafka = new Kafka({
//     clientId: 'my-app',
//     brokers: ['localhost:9092']
// });

// const producer = kafka.producer();

// async function sendFileMessage(file) {
//     try {
//         await producer.connect();
//         await producer.send({
//             topic: 'file-topic',
//             messages: [
//                 { value: JSON.stringify(file) }
//             ]
//         });
//     } catch (err) {
//         console.log('Error sending file message', err);
//     } finally {
//         await producer.disconnect();
//     }
// }

// ------------------------------ apis ------------------------------
app.post('/upload-local', uploadDisk.single('file'), async (req, res) => {
    const file = new File({
        name: req.file.originalname,
        path: req.file.path,
        size: req.file.size,
        type: req.file.mimetype
    });

    console.log('req.file :>> ', req.file);

    const maxSize = 5 * 1024 * 1024; // 5 MB in bytes

    if (req.file.size > maxSize) {
        res.status(400).send('File size exceeds the maximum limit of 5 MB');
        return;
    }

    file.save().then((result) => {
        res.send(result);
    }).catch((err) => {
        console.log(err);
        res.status(500).send('Error saving file');
    });

    // try {
    //     await file.save();
    //     await sendFileMessage(file); // Send file message using kafkajs
    //     res.send(file);
    // } catch (err) {
    //     console.log(err);
    //     res.status(500).send('Error saving file');
    // }
});


app.post('/upload-local-multiple', uploadDisk.array('files'), async (req, res) => {
    const files = req.files.map((file) => {
        return {
            name: file.originalname,
            path: file.path,
            size: file.size,
            type: file.mimetype
        };
    });

    const maxSize = 5 * 1024 * 1024; // 5 MB in bytes

    for (let i = 0; i < files.length; i++) {
        if (files[i].size > maxSize) {
            res.status(400).send('File size exceeds the maximum limit of 5 MB');
            return;
        }
    }

    File.insertMany(files).then((result) => {
        res.send(result);
    }).catch((err) => {
        console.log(err);
        res.status(500).send('Error saving file');
    });
});



app.get('/download/:file', (req,res) => {
    const file = req.params.file;
    const fileLocation = path.join(__dirname, 'uploads',file);

    if (fs.existsSync(fileLocation)) {
        res.download(fileLocation, file);
    } else {
        res.status(404).send('File not found');
    }
});


app.get('/files', (req, res) => {
    File.find().then((result) => {
        res.send(result).json();
    }).catch((err) => {
        console.log(err);
    });
});
// x----------------------------- apis -----------------------------x


app.listen(process.env.PORT, () => {
    console.log(`Server started on port ${process.env.PORT}`)
});