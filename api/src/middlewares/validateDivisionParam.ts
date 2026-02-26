import { type Request, type Response, type NextFunction } from 'express';

export const validateGenderParam = (req: Request, res: Response, next: NextFunction) => {
    if (req.query.division === undefined) return next();

    const div = req.query.division;
    
    if (typeof div != 'string') {
        return res.status(400).json({message: 'Query param needs to be a string - i, or ii, or iii'});
    }

    const divisionInput = div.toLowerCase();
    if (!['i', 'ii', 'iii'].includes(divisionInput)) {
        return res.status(400).json({message: 'Division query needs to be - i, ii, or iii'}); 
    } 

    req.query.division = divisionInput; // Clean up
    next();
}