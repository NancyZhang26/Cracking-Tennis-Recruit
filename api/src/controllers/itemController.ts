import type { Request, Response, NextFunction } from 'express';
import { Pool } from 'pg';
import type { Player, College, CollegeTemp } from '../models/models.ts';
import dotenv from 'dotenv';
dotenv.config();

const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DATABASE,
    port: Number(process.env.DB_PORT),
})

export const getColleges = async (req: Request, res: Response, next: NextFunction) => {
    try {
        const division = req.query.division;
        const gender = req.query.gender

        let result;       
        let command;
        
        if (typeof division === 'string' && typeof gender === 'string') {
            command = 'SELECT * FROM colleges_temp WHERE division=$1 AND gender=$2;'
            result = await pool.query(command, [division, gender]);
        } else if (typeof division === 'string' && typeof gender === 'undefined') {
            command = 'SELECT * FROM colleges_temp WHERE division=$1;'
            result = await pool.query(command, [division]);
        } else if (typeof division === 'undefined' && typeof gender === 'string') {
            command = 'SELECT * FROM colleges_temp WHERE gender=$1;'
            result = await pool.query(command, [gender]);
        } else {
            command = 'SELECT * FROM colleges_temp;'
            result = await pool.query(command);
        }

        res.status(200).json(result.rows);
    } catch(error) {
        next(error);
    }
}
