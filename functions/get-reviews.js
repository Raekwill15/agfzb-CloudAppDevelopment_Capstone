const express = require('express');
const app = express();
const port = process.eventNames.PORT || 3100;
const Cloudant = require('@cloudant/cloudant');
// const { CloudantV1 } = require('')

async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant ({
            plugins: {iamauth: { iamApiKey: '2xjf2vp6h2rmFtTc-X7jXC89zsepyqAkpzLaJLkXxkKf'} },
            url: 'https://d64ff724-df11-4f37-bd70-cfa6953bd8c5-bluemix.cloudantnosqldb.appdomain.cloud',
        });

        const db = cloudant.use('reviews');
        console.info('Connect Success! DB Connected!');
        return db
    } catch(err) {
        console.error('Connect Failure; ' + err.message + ' for Cloudant DB')
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

app.post('/review/add' , (req,res) => {
    // const { dealer_id } = req.query;

    // const selector = {}

    // if (dealer_id) {
    //     selector.dealer_id = parseInt(dealer_id);
    // }

    // db.putDocument(req.body.review).then(response => {
    //     console.log(response.result)
    // })
    const response = db.insert(req.body.review)

    console.log(req.body.review);
    res.json("Hello");
});


app.get('/reviews/get' , (req,res) => {
    const { id } = req.query;

    const selector = {}

    if (id) {
        selector.id = parseInt(id);
    }

    const queryOptions = {
        selector, 
        limit: 10,
    };

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching reviews: ', err);
            res.status(500).json({error: 'An error occurred while fetching reviews'});
        } else {
            const reviews = body.docs;
            res.json(reviews);
        }
    });
});


app.listen(port, () => {
    console.log(`Server is runing on port ${port}`);
});