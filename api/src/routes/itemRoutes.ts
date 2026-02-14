import { Router } from 'express';
import { getColleges } from '../controllers/itemController.js';
import { validateDivisionParam } from '../middlewares/validateDivisionParam.js';
import { validateGenderParam } from '../middlewares/validateGenderParam.js';

const router = Router();

router.get('/colleges', validateDivisionParam, validateGenderParam, getColleges); // Middleware comes b4 controller

export default router;