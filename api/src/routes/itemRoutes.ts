import { Router } from 'express';
import { getColleges } from '../controllers/itemController.js';
import { validateDivisionParam } from '../middlewares/validateGenderParam.js';
import { validateGenderParam } from '../middlewares/validateDivisionParam.js';

const router = Router();

router.get('/colleges', validateDivisionParam, validateGenderParam, getColleges); // Middleware comes b4 controller

export default router;