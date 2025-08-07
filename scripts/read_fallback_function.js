#This Node.js script powers an Azure Function that can read billing records from both Cosmos DB and Blob Storage, acting as a fallback.

// read_fallback_function.js
 
const { CosmosClient } = require("@azure/cosmos");

const { BlobServiceClient } = require("@azure/storage-blob");

const zlib = require("zlib");
 
const cosmosClient = new CosmosClient({ endpoint: process.env.COSMOS_ENDPOINT, key: process.env.COSMOS_KEY });

const blobServiceClient = BlobServiceClient.fromConnectionString(process.env.BLOB_CONNECTION_STRING);
 
module.exports = async function (context, req) {

    const recordId = req.query.id;
 
    try {

        const container = cosmosClient.database(process.env.DATABASE_NAME).container(process.env.CONTAINER_NAME);

        const { resource } = await container.item(recordId, req.query.partitionKey).read();

        if (resource) {

            context.res = { status: 200, body: resource };

            return;

        }

    } catch (err) {

        // Proceed to fallback

    }
 
    try {

        const containerClient = blobServiceClient.getContainerClient("billing-archive");

        const yearMonth = new Date().toISOString().slice(0, 7);

        const blobClient = containerClient.getBlobClient(`${yearMonth}/billing-archive.json.gz`);

        const downloadBlockBlobResponse = await blobClient.download();

        const chunks = [];

        for await (const chunk of downloadBlockBlobResponse.readableStreamBody) {

            chunks.push(chunk);

        }
 
        const buffer = Buffer.concat(chunks);

        const decompressed = zlib.gunzipSync(buffer).toString();

        const records = JSON.parse(decompressed);

        const record = records.find(r => r.id === recordId);
 
        if (record) {

            context.res = { status: 200, body: record };

        } else {

            context.res = { status: 404, body: "Record not found" };

        }

    } catch (error) {

        context.res = { status: 500, body: "Error reading from fallback." };

    }

};

 
