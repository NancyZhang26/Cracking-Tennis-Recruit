import express from 'express';
import router from './routes/itemRoutes.js';
import dotenv from 'dotenv';
import { errorHandler } from './middlewares/errorHandler.js';

dotenv.config(); 

const app = express();

// Global body parsing
app.use(
    express.urlencoded({ extended: true }),
    express.json()
)

app.use('/api', router);

app.get('/', (request, response) => {
    response.json({info: 'Helohelohelohaaallllo'})
})

app.use(errorHandler);

export default app;