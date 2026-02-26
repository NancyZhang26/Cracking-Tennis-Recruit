import { type Request, type Response, type NextFunction } from 'express';

export const validateDivisionParam = (req: Request, res: Response, next: NextFunction) => {
    if (req.query.gender === undefined) return next();

    const gender = req.query.gender;
    
    if (typeof gender != 'string') {
        return res.status(400).json({message: 'Query param needs to be a string - f / m'});
    }

    const genderInput = gender.toLowerCase();
    if (!['m', 'f'].includes(genderInput)) {
        return res.status(400).json({message: 'Gender query needs to be - f / m'}); 
    } 

    req.query.gender = genderInput; // Clean up
    next();
}